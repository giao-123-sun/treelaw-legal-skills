"""Index actual SKILL.md and plugin manifests. Never run upstream content.

Run manually after reviewing source versions. CI only builds checked-in metadata.
"""
import hashlib
import io
import json
import re
import urllib.request
import zipfile
from collections import Counter
from pathlib import Path
from urllib.parse import quote
import yaml

ROOT=Path(__file__).resolve().parents[1]
DATE='2026-11-02'
def read(path):return json.loads((ROOT/path).read_text(encoding='utf-8'))
def save(path,value):(ROOT/path).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
labels=dict(line.split('|',1) for line in (ROOT/'data/task-labels.txt').read_text(encoding='utf-8').splitlines() if line and not line.startswith('#'))
mirror={x['path']:x for x in read('data/mirrors.json')}
old={x['id']:x for x in read('data/source-base.json')}
sources=[
 dict(id='panrui',base=old['panrui'],repo='pa1nrui1/legal-skills',mirror='China/panrui'),
 dict(id='anthropic',base=old['anthropic-legal'],repo='anthropics/claude-for-legal',mirror='US/anthropic-legal'),
 dict(id='l0cka',base=dict(id='l0cka',name='l0cka · Legal Skills',group='Others',publisher='个人',author='l0cka',kind='插件',tasks=['诉讼','非诉','合规'],summary='澳大利亚法律工作流及通用证据、推理技能。',url='https://github.com/l0cka/legal-skills',evidence='https://github.com/l0cka/legal-skills',identity='具名GitHub账号；本轮未独立核实律师执业身份。',published=None,updated='2026-10-28',created='2026-08-13',license='MIT',languages=['English'],jurisdictions=['澳大利亚'],systems=['普通法系'],materials=[],dependencies='Claude/Codex插件宿主；部分任务需要官方法源联网访问、机构规则或文书工具。',access='仓库快照',keywords='Australian law contract research'),repo='l0cka/legal-skills',mirror='Others/l0cka-legal'),
 dict(id='thu',base=old['legal-skills-chinese'],repo='THUYRan/Legal-Skills-Chinese',commit='c31ef1f022be6bcb3e31c1a2374d1d8240ffa61f'),
]
plugin_names={'ai-governance-legal':'AI 治理','commercial-legal':'商业合同','corporate-legal':'公司与并购','employment-legal':'劳动与用工','ip-legal':'知识产权','law-student':'法律学习','legal-clinic':'法律诊所','litigation-legal':'诉讼','privacy-legal':'隐私与数据','product-legal':'产品法务','regulatory-legal':'监管合规'}
items=[];excluded=[];evidence=[];seen_hashes={};source_docs={};counts={}
def frontmatter(text):
    text=text.lstrip('\ufeff')
    if not text.startswith('---'):raise ValueError('Missing frontmatter')
    fm=yaml.safe_load(text.split('---',2)[1])
    assert fm.get('name') and fm.get('description'),fm
    return fm
def plain(s):return re.sub(r'\s+',' ',str(s)).strip()
def tasks_for(text,plugin=''):
    s=text.lower();out=[]
    if re.search(r'litig|case|court|claim|evidence|judg|trial|dispute|deposition|subpoena|诉讼|辩护|庭|证据|案件|裁判|仲裁|审理|判决|法条|法律解释|推理|论证',s):out.append('诉讼')
    if re.search(r'contract|agreement|commercial|corporat|nda|draft|board|estate|diligence|merger|合同|公司|破产|清算|重整|债权|尽调|法律文书|法律咨询',s):out.append('非诉')
    if re.search(r'compliance|privacy|regulat|governance|fair.work|aml|consumer|policy|employment|合规|监管|劳动|广告|食品|风险',s):out.append('合规')
    if re.search(r'international|cross.border|跨境|涉外|境外',s):out.append('涉外')
    if plugin=='law-student':out=['学习与培训']
    return out or ['非诉']
def material_for(text):
    s=text.lower();out=[]
    if re.search(r'legislation|statut|法条|法规|规范效力|法律解释',s):out.append('法条')
    if '司法解释' in s:out.append('司法解释')
    if re.search(r'judgment|citation|case.retriev|case.brief|类案|案例|裁判|判例',s):out.append('案例')
    return out
def location(source,slug,description,body,plugin):
    if source['id'] in ['panrui','thu']:return 'China',['中国大陆'],['中国社会主义法律体系']
    if source['id']=='l0cka':
        neutral=('source-linked' in description.lower() and not 'australian' in description.lower()) or 'jurisdiction-neutral' in description.lower() or 'jurisdiction-agnostic' in description.lower() or slug in ['clarify-burden-and-standard','find-blind-spots','map-assumptions','oppose-as-counsel','pressure-test-argument','pressure-test-strategy','red-team-evidence','role-play-decision-maker','simplify-without-losing-precision','steelman-then-attack','test-understanding','drill-oral-advocacy']
        return ('Others',['通用方法；使用时指定法域'],[]) if neutral else ('Others',['澳大利亚'],['普通法系'])
    # General commercial / corporate methods do not imply US governing law.
    if 'eu ai act' in description.lower():return 'Others',['欧盟'],[]
    if plugin in ['litigation-legal','law-student','legal-clinic']:return 'US',['美国法律工作；州与法院规则按事项确认'],['普通法系']
    if plugin=='employment-legal' and slug not in ['international-expansion','expansion-kickoff','expansion-update']:
        return 'US',['美国用工及机构所在地规则；按配置确认'],['普通法系']
    return 'Others',['通用工作流；按项目指定适用法'],[]
def skip(source,path):
    bits=path.split('/');slug=bits[-2] if len(bits)>1 else ''
    if source['id']=='anthropic':
        if bits[0] in ['legal-builder-hub','external_plugins']:return '技能管理工具或外部供应商插件，不计入本次法律任务条目'
        if slug in ['cold-start-interview','customize','matter-workspace','session','ai-tool-handoff']:return '初始化、配置、工作区或宿主交接辅助项'
    if source['id']=='panrui' and (path=='SKILL.md' or slug in ['法律工作总控','刑事辩护总调度','微信文章转换为markdown','法律文章quai味道']):return '总入口、调度或通用编辑辅助项'
    if source['id']=='l0cka' and slug.startswith('configure-'):return '机构规则初始化；保留在完整插件包内'
    return None

for source in sources:
    if source.get('mirror'):
        m=mirror[source['mirror']];source['commit']=m['commit']
        with zipfile.ZipFile(ROOT/source['mirror']/'upstream.zip') as z:
            source_docs[source['id']]={n.split('/',1)[1]:z.read(n) for n in z.namelist() if not n.endswith('/')}
    else:
        cache=ROOT/'.local/thu-skills.json'
        if cache.exists(): docs={d['path']:d['content'].encode('utf-8') for d in json.loads(cache.read_text(encoding='utf-8'))}
        else:
            # Private research cache. Restricted source prose is never published.
            url=f'https://codeload.github.com/{source["repo"]}/zip/{source["commit"]}'
            with urllib.request.urlopen(url,timeout=60) as r:raw=r.read()
            with zipfile.ZipFile(io.BytesIO(raw)) as z:docs={n.split('/',1)[1]:z.read(n) for n in z.namelist() if '/skills/' in n and '/English/' not in n and n.endswith('/SKILL.md')}
        source_docs[source['id']]=docs
    docs=source_docs[source['id']]
    accepted=[]
    for path,raw in sorted(docs.items()):
        if not (path=='SKILL.md' or path.endswith('/SKILL.md')):continue
        reason=skip(source,path)
        if reason:excluded.append(dict(source=source['id'],path=path,reason=reason));continue
        text=raw.decode('utf-8-sig')
        try:fm=frontmatter(text)
        except (yaml.YAMLError,ValueError,AssertionError) as error:
            excluded.append(dict(source=source['id'],path=path,reason='上游frontmatter格式未通过解析，暂不收录',detail=str(error)[:350]));continue
        slug=str(fm['name']);description=plain(fm['description']);sha=hashlib.sha256(raw).hexdigest()
        if sha in seen_hashes:excluded.append(dict(source=source['id'],path=path,reason='文件内容重复',sameAs=seen_hashes[sha]));continue
        plugin=path.split('/')[0] if source['id']=='anthropic' else 'legal-skills'
        unique=f'{source["id"]}-{hashlib.sha256(path.encode()).hexdigest()[:12]}'
        seen_hashes[sha]=unique
        title=labels.get(slug,slug)
        assert re.search('[\u4e00-\u9fff]',title),f'Missing editorial title: {source["id"]} {slug}'
        b=dict(source['base']);b.pop('mirror',None);b.pop('parent',None)
        group,jurisdictions,systems=location(source,slug,description,text,plugin)
        # Keep restricted-source cards to original names and our editorial task labels.
        desc=description if source['id']!='thu' else f'处理“{title}”这一法律任务。步骤及输入输出规范见原始技能文件。'
        card_summary=desc[:200]+('…' if len(desc)>200 else '')
        suite_id=f'{source["id"]}-{plugin}'
        b.update(id=unique,name=title,originalName=slug,englishName=slug.replace('-',' ').title(),kind='Skill',group=group,
                 tasks=tasks_for(title+' '+slug+' '+plugin,plugin),summary=card_summary,description=desc,
                 url=f'https://github.com/{source["repo"]}/blob/{source["commit"]}/{quote(path)}',
                 upstreamDirectory=f'https://github.com/{source["repo"]}/tree/{source["commit"]}/{quote(str(Path(path).parent).replace(chr(92),"/"))}',
                 sourceRepo=source['repo'],sourceId=source['id'],sourcePath=path,sourceCommit=source['commit'],sourceSha256=sha,
                 suiteId=suite_id,suiteName=plugin_names.get(plugin,source['base']['name']),
                 jurisdictions=jurisdictions,systems=systems,materials=material_for(title+' '+description),
                 keywords=' '.join([title,slug,description,plugin]),published=None,checked=DATE,tested=False,
                 invocation='经主工作流调用' if fm.get('user-invocable') is False else '按宿主规则调用',
                 entryEvidence='已读取原始SKILL.md并校验name、description和文件哈希；未执行',
                 editorial='中文名称与任务分类为Treelaw编辑整理；原始指令见来源')
        if source.get('mirror'):b['mirror']=source['mirror'];b['access']='仓库快照'
        else:b['access']='原站获取'
        items.append(b);accepted.append(unique)
        evidence.append(dict(id=unique,source=source['id'],path=path,sha256=sha,commit=source['commit'],checked=DATE))
    counts[source['id']]=dict(repo=source['repo'],commit=source['commit'],skills=len(accepted),scanned=sum(p=='SKILL.md' or p.endswith('/SKILL.md') for p in docs))
    plugin_seen=set()
    for path,raw in sorted(docs.items()):
        if not path.endswith('/plugin.json') or not any(v in path for v in ['.claude-plugin/','.codex-plugin/']):continue
        parent=path.rsplit('/',2)[0] if path.count('/')>=2 else '.'
        if parent in plugin_seen:continue
        plugin_seen.add(parent)
        if source['id']=='anthropic' and parent not in plugin_names:continue
        fm=json.loads(raw);pname=fm['name'];members=[x['id'] for x in items if x.get('sourceId')==source['id'] and x['kind']=='Skill' and (source['id']!='anthropic' or x['sourcePath'].startswith(parent+'/'))]
        if not members:continue
        b=dict(source['base']);b.pop('parent',None)
        b.update(id=f'{source["id"]}-plugin-{pname}',name=plugin_names.get(pname,b['name'])+' · 插件',englishName=pname+' plugin',originalName=pname,kind='插件',
                 summary=plain(fm['description'])[:200],description=plain(fm['description']),url=f'https://github.com/{source["repo"]}/blob/{source["commit"]}/{quote(path)}',
                 sourceRepo=source['repo'],sourceId=source['id'],sourcePath=path,sourceCommit=source['commit'],sourceSha256=hashlib.sha256(raw).hexdigest(),
                 suiteId=f'{source["id"]}-{pname}',suiteName=plugin_names.get(pname,source['base']['name']),members=members,
                 group='China' if source['id']=='panrui' else 'US' if pname in ['litigation-legal','law-student','legal-clinic','employment-legal'] else 'Others',
                 systems=['中国社会主义法律体系'] if source['id']=='panrui' else [],
                 jurisdictions=['中国大陆'] if source['id']=='panrui' else ['澳大利亚及通用工作流'] if source['id']=='l0cka' else ['按插件及机构配置确认'],
                 materials=[],tasks=tasks_for(pname+' '+b['summary'],pname),mirror=source['mirror'],checked=DATE,published=None,tested=False,
                 version=fm.get('version'),access='仓库快照',invocation='按原仓库插件说明加载',entryEvidence='已读取插件清单；同一插件的Claude与Codex入口合并',keywords=pname+' '+b['summary'])
        items.append(b);evidence.append(dict(id=b['id'],source=source['id'],path=path,sha256=b['sourceSha256'],commit=source['commit'],checked=DATE))
    counts[source['id']]['plugins']=sum(x['kind']=='插件' and x['sourceId']==source['id'] for x in items)

# Stable relationship: a task card can link directly to its containing plugin.
for x in items:
    if x['kind']=='Skill':
        x['pluginId']=next((p['id'] for p in items if p['kind']=='插件' and x['id'] in p['members']),None)
save('data/catalog.json',items)
save('data/source-evidence.json',evidence)
save('data/import-audit.json',dict(date=DATE,total=len(items),skills=sum(x['kind']=='Skill' for x in items),plugins=sum(x['kind']=='插件' for x in items),groups=dict(Counter(x['group'] for x in items)),sources=counts,excluded=excluded,translationCopiesExcluded=38,referenceItems=len(read('data/reference-library.json')),method='原始文件为单位；按文件哈希去重；同一插件的宿主入口合并；参考资料不计入技能数量'))
save('data/sources.json',[dict(id=s['id'],repo=s['repo'],commit=s['commit'],publisher=s['base']['publisher'],author=s['base']['author'],identity=s['base']['identity'],evidence=s['base']['evidence'],license=s['base']['license'],name=s['base']['name'],counts=counts[s['id']]) for s in sources])
print(json.dumps({k:v for k,v in read('data/import-audit.json').items() if k!='excluded'},ensure_ascii=False))
