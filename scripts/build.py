"""Build the static directory from checked-in metadata. No network calls."""
import html
import json
import os
import re
import shutil
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'site'
BASE=os.environ.get('SITE_URL','https://giao-123-sun.github.io/treelaw-legal-skills').rstrip('/')
REPO='https://github.com/giao-123-sun/treelaw-legal-skills'
def read(path):return json.loads((ROOT/path).read_text(encoding='utf-8'))
DATA=read('data/catalog.json');REFS=read('data/reference-library.json');SOURCES=read('data/sources.json');AUDIT=read('data/import-audit.json')
ORDER=['协会','专业律师','法律教师','厂商','个人']
EN={'协会':'Association','专业律师':'Legal practitioner','法律教师':'Legal educator','厂商':'Vendor','个人':'Individual / community','诉讼':'Litigation','非诉':'Transactional','涉外':'Cross-border','合规':'Compliance','学习与培训':'Legal education','普通法系':'Common law','大陆法系':'Civil law','混合法系':'Mixed system','中国社会主义法律体系':'Chinese socialist legal system','法条':'Statutes','司法解释':'Judicial interpretations','案例':'Case law','插件':'Plugin','仓库快照':'Repository archive','原站获取':'Get at source'}
TASKS=[
 ('contract-review','中国合同审查 Skills',False,lambda x:x['group']=='China' and '合同' in x['name']),
 ('litigation','类案、证据与争议焦点',False,lambda x:x['group']=='China' and '诉讼' in x['tasks']),
 ('nda-review','NDA Review & Contract Redlining',True,lambda x:x['group']!='China' and bool(re.search(r'nda|commercial|agreement|contract|redline',x.get('originalName','')))),
 ('legal-research','Legal Research & Litigation',True,lambda x:x['group']!='China' and '诉讼' in x['tasks']),
]
pages=[]
def esc(v):return html.escape(str(v),quote=True)
def label(v,en):return EN.get(v,v) if en else v
def name(x,en):return x.get('englishName',x['name']) if en else x['name']
def link(target,current):return os.path.relpath(OUT/target,(OUT/current).parent).replace('\\','/')
def write(path,text):
    p=OUT/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding='utf-8');pages.append(path)
def brand(path):return f'<a class="brand" href="{link("index.html",path)}"><img src="{link("assets/treelaw-mark.svg",path)}" alt="">Treelaw<small>LEGAL SKILLS DIRECTORY</small></a>'
def layout(path,title,desc,body,en=False,schema=None):
    data={'@context':'https://schema.org','@type':'CollectionPage','name':title,'description':desc,'url':BASE+'/'+path}
    if schema:data.update(schema)
    structured=json.dumps(data,ensure_ascii=False).replace('<','\\u003c')
    tasklinks=''.join(f'<a href="{link("tasks/"+s+".html",path)}">{esc(t)}</a>' for s,t,_,_ in TASKS)
    return f'''<!doctype html><html lang="{'en' if en else 'zh-CN'}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)} · Treelaw</title><meta name="description" content="{esc(desc)}"><link rel="canonical" href="{BASE}/{path}">
<meta property="og:title" content="{esc(title)} · Treelaw"><meta property="og:description" content="{esc(desc)}"><meta property="og:type" content="website"><meta property="og:url" content="{BASE}/{path}">
<link rel="icon" href="{link('assets/treelaw-mark.svg',path)}"><link rel="stylesheet" href="{link('assets/style.css',path)}"><script type="application/ld+json">{structured}</script><script src="{link('assets/app.js',path)}" defer></script></head><body>
<a class="skip" href="#main">{'Skip to content' if en else '跳到正文'}</a><header><div class="wrap head">{brand(path)}<nav class="nav" aria-label="Main"><a href="{link('index.html',path)}">{'Skills' if en else '技能目录'}</a><a href="{link('publishers.html',path)}">{'Publishers' if en else '来源榜'}</a><a href="{link('references.html',path)}">{'Guides' if en else '参考资料'}</a><a class="repo" href="{REPO}" target="_blank" rel="noopener">GitHub ↗</a></nav></div></header>
{body}<section class="tasks"><div class="wrap"><b>{'Browse by task' if en else '从工作任务开始'}</b>{tasklinks}</div></section><footer><div class="wrap">{brand(path)}<p>{'Curated by Treelaw. Original works belong to their publishers. Skills link to source files; plugins link to manifests. Listing does not imply endorsement. Upstream licenses apply. Execution quality has not been evaluated.' if en else 'Treelaw 负责整理与展示，作品归原发布方。技能对应原始文件，插件对应真实清单。收录不表示发布方背书。下载遵循原许可，当前未做运行效果评测。'}<br><a href="{link('about.html',path)}">{'Editorial policy' if en else '收录与授权说明'}</a> · <a href="{link('llms.txt',path)}">llms.txt</a> · 2026-11-02</p></div></footer></body></html>'''

def card(x,path,en):
    text=' '.join([x['name'],x['originalName'],x['author'],x['keywords'],x['summary'],*x['tasks'],*x['jurisdictions']])
    attrs=dict(text=text,task=x['tasks'],publisher=[x['publisher']],system=x['systems'],material=x['materials'],kind=[x['kind']],source=[x['sourceId']],access=[x['access']],name=x['name'],date=x['updated'] or '')
    actions=f'<a href="{link("resources/"+x["id"]+".html",path)}">{"Details" if en else "用途与使用条件"} →</a><a href="{esc(x["url"])}" target="_blank" rel="noopener">{"Source file" if en else "原始文件"} ↗</a>'
    if x.get('pluginId'):actions+=f'<a href="{link("resources/"+x["pluginId"]+".html",path)}">{"Plugin" if en else "所属插件"}</a>'
    members=f' · {len(x["members"])} '+('listed skills' if en else '项已收录技能') if x.get('members') else ''
    return f'''<article class="card" data-filter="{esc(json.dumps(attrs,ensure_ascii=False))}"><div class="topline"><span class="badge">{esc(label(x['kind'],en))}</span><span>{esc(label(x['publisher'],en))}</span><span>{x['group']}</span></div>
<h2><a href="{link('resources/'+x['id']+'.html',path)}">{esc(name(x,en))}</a></h2><div class="original">{esc(x['originalName'])}</div><p class="skill-description">{esc(x['summary'])}</p><div class="tags">{' · '.join(esc(label(t,en)) for t in x['tasks'])}{members}</div><div class="author">{esc(x['author'])} · {esc(x['suiteName'])}</div><div class="meta">{esc(x['license'])} · {x['sourceCommit'][:7]}</div><div class="actions">{actions}</div></article>'''

def listing(path,title,desc,items,group=None,en=False):
    nav=''.join(f'<a class="{"active" if g==group or g=="All" and group is None else ""}" href="{link("index.html" if g=="All" else g+"/index.html",path)}">{g if en else zh}<small>{len(DATA) if g=="All" else sum(x["group"]==g for x in DATA)}</small></a>' for g,zh in [('All','全部'),('China','中国'),('US','美国'),('Others','其他法域')])
    fields=[('task','业务类型','Practice',['诉讼','非诉','涉外','合规','学习与培训']),('publisher','发布方','Publisher',ORDER),('system','法系','Legal system',['中国社会主义法律体系','大陆法系','普通法系','混合法系']),('material','涉及资料','Material',['法条','司法解释','案例']),('kind','形式','Type',['Skill','插件']),('source','来源套件','Source',[s['id'] for s in SOURCES]),('access','获取方式','Access',['仓库快照','原站获取'])]
    source_labels={s['id']:s['name'] for s in SOURCES};filters=''
    for key,zh,english,values in fields:
        opts=''.join(f'<option value="{esc(v)}">{esc(source_labels[v] if key=="source" else label(v,en))}</option>' for v in values)
        filters+=f'<label>{english if en else zh}<select id="{key}" name="{key}"><option value="">{"All" if en else "全部"}</option>{opts}</select></label>'
    ordered=sorted(items,key=lambda x:(ORDER.index(x['publisher']),x['kind']!='Skill'))
    stats=f'{sum(x["kind"]=="Skill" for x in items)} '+('individual skills' if en else '个单项 Skill')+' · '+str(sum(x['kind']=='插件' for x in items))+' '+('plugins' if en else '个插件')
    pills=f'<div class="type-tabs"><button type="button" data-kind="" aria-pressed="true">{"All" if en else "全部"}</button><button type="button" data-kind="Skill" aria-pressed="false">Skill</button><button type="button" data-kind="插件" aria-pressed="false">{"Plugins" if en else "插件"}</button><span>{stats}</span></div>'
    body=f'''<main id="main" class="wrap"><section class="hero"><div><p class="eyebrow">TREELAW / LEGAL SKILLS & PLUGINS</p><h1>{esc(title)}<span>{stats}</span></h1></div><p class="hero-note">{esc(desc)}<br><strong>{'One task, one skill. Keep its source and dependencies in view.' if en else '找到具体任务，打开具体技能。作者与依赖一并列清。'}</strong></p></section><nav class="countries" aria-label="Jurisdiction">{nav}<span class="stamp">REVIEWED 2026.11.02</span></nav><div class="browse">
<form class="filters" id="filters"><h2>{'Refine search' if en else '筛选技能'}</h2>{filters}<button id="clear-filters" class="reset" type="button">{'Clear filters' if en else '清除筛选'}</button><p>{'General workflows are in Others when governing law is configurable.' if en else '通用工作流按项目配置适用法，归入Others。身份自述与独立核对在详情中分开说明。'}</p></form>
<section aria-label="Resources"><label class="skip" for="query">Search</label><input class="search" id="query" type="search" placeholder="{'Search NDA, deposition, evidence…' if en else '搜索具体任务，如：合同审查、争议焦点、保密协议、尽调'}"><div class="quick">{''.join(f'<button type="button" data-query="{q}">{q}</button>' for q in (['NDA','deposition','privacy','legislation'] if en else ['合同','类案检索','争议焦点','NDA','尽调']))}</div>{pills}
<div class="result-bar"><span aria-live="polite"><b id="count">{len(items)}</b> {'entries' if en else '项匹配'}</span><label>{'Sort ' if en else '排序 '}<select id="sort"><option value="source">{'Publisher' if en else '发布方分组'}</option><option value="recent">{'Source updated' if en else '来源更新'}</option><option value="name">{'Name' if en else '名称'}</option></select></label></div><div class="cards">{''.join(card(x,path,en) for x in ordered)}</div><p id="empty" class="empty" hidden>{'No match. Clear a filter or try a different task.' if en else '暂无匹配技能。可清除筛选或换一个任务关键词。'}</p>
<nav class="pagination" id="pagination" aria-label="Pagination" hidden><button type="button" id="previous">{'Previous' if en else '上一页'}</button><span id="page-label" aria-live="polite"></span><button type="button" id="next">{'Next' if en else '下一页'}</button></nav><noscript><p>全部条目已列在正文中。筛选与分页需要JavaScript。</p></noscript></section></div></main>'''
    schema={'mainEntity':{'@type':'ItemList','numberOfItems':len(items),'itemListElement':[{'@type':'ListItem','position':i+1,'url':BASE+'/resources/'+x['id']+'.html','name':name(x,en)} for i,x in enumerate(ordered)]}}
    write(path,layout(path,title,desc,body,en,schema))

def detail(x):
    path='resources/'+x['id']+'.html';en=x['group']=='US'
    facts=[('发布方 / Publisher',label(x['publisher'],en)+' · '+x['author']),('身份依据 / Evidence',x['identity']),('法域 / Jurisdiction','；'.join(x['jurisdictions'])),('任务 / Practice',' / '.join(label(v,en) for v in x['tasks'])),('语言 / Language',' / '.join(x['languages'])),('调用方式 / Invocation',x['invocation']),('依赖 / Dependencies',x['dependencies']),('首次发布 / Published',x['published'] or '单项日期未披露'),('仓库创建 / Created',x.get('created','未记录')),('仓库更新 / Updated',x['updated'] or '未记录'),('核对 / Checked',x['checked']),('授权 / License',x['license']),('原始文件 / Path',x['sourcePath']),('固定提交 / Commit',x['sourceCommit']),('SHA-256',x['sourceSha256']),('本次核验 / Check',x['entryEvidence']),('效果测试 / Evaluation','未执行 / Not run')]
    actions=f'<a href="{esc(x["url"])}" target="_blank" rel="noopener">{"Original file" if en else "打开原始文件"} ↗</a><a href="{esc(x["evidence"])}">{"Publisher evidence" if en else "作者背景依据"} ↗</a>'
    if x.get('mirror'):actions+=f'<a href="{REPO}/blob/main/{x["mirror"]}/README.md">{"Complete upstream archive" if en else "完整套件下载与许可"} ↓</a>'
    if x.get('pluginId'):actions+=f'<a href="{link("resources/"+x["pluginId"]+".html",path)}">{"Containing plugin" if en else "查看所属插件"} →</a>'
    members=''
    if x.get('members'):
        byid={d['id']:d for d in DATA}
        members='<section class="member-list"><h2>'+('Listed task skills' if en else '插件中已收录的业务技能')+f' · {len(x["members"])}</h2><ul>'+''.join(f'<li><a href="{id}.html">{esc(name(byid[id],en))}</a></li>' for id in x['members'])+'</ul></section>'
    body=f'''<main id="main" class="wrap detail"><div class="crumb"><a href="{link('index.html',path)}">Treelaw</a> / <a href="{link(x['group']+'/index.html',path)}">{x['group']}</a> / {esc(label(x['kind'],en))}</div><span class="badge">{esc(label(x['kind'],en))}</span><h1>{esc(name(x,en))}</h1><p class="original">{esc(x['originalName'])} · {esc(x['suiteName'])}</p><p class="lead">{esc(x.get('description',x['summary']))}</p><div class="actions">{actions}</div>
<p class="notice">{'The skill is a task entry within its upstream package. Follow the package instructions for shared references, tools and playbooks. Source-file checks are separate from execution tests.' if en else '单个 Skill 是套件中的任务入口。共享参考文件、工具与机构规则按原套件说明配置。下载入口提供完整上游套件，保留相关参考文件。原始文件已读取，运行效果尚未测试。'}</p>{members}<dl class="facts">{''.join(f'<dt>{esc(k)}</dt><dd>{esc(v)}</dd>' for k,v in facts)}</dl><p class="notice">中文名称为目录编辑译名。仓库更新日期未代表单项技能的修改日。原始名称、固定版本与校验值一并保留。</p></main>'''
    write(path,layout(path,name(x,en),x['summary'],body,en,{'@type':'CreativeWork','author':{'@type':'Organization' if x['publisher']=='厂商' else 'Person','name':x['author']},'citation':[x['url'],x['evidence']],'inLanguage':x['languages']}))

def references():
    sections=''.join(f'<article class="source-row"><span class="badge">{esc(x["kind"])}</span><h2><a href="{esc(x["url"])}">{esc(x["name"])} ↗</a></h2><p>{esc(x["summary"])}</p><p>{esc(x["author"])} · {esc(x["publisher"])} · {esc(x["license"])}</p><p>{esc(x["identity"])}</p></article>' for x in REFS)
    body=f'<main id="main" class="wrap detail prose"><p class="eyebrow">TREELAW / REFERENCE LIBRARY</p><h1>指南、Prompt 与其他套件。</h1><p class="lead">{len(REFS)}项补充资料。整库介绍、指南和商业平台流程单列，不计入Skill与插件数量。此页的套件尚未逐文件展开。</p>{sections}</main>'
    write('references.html',layout('references.html','法律Prompt、指南与套件参考','原始发布者的法律提示库、协会指南和商业工作流入口。',body))

def publishers():
    entries=[dict(name=s['name'],publisher=s['publisher'],identity=s['identity'],evidence=s['evidence'],url='index.html?source='+s['id'],count=f'{s["counts"]["skills"]} Skill / {s["counts"]["plugins"]} 插件') for s in SOURCES]
    entries.extend(dict(x,count='参考资料；未计入技能数量') for x in REFS)
    groups=''
    for category in ORDER:
        subset=[x for x in entries if x['publisher']==category]
        groups+=f'<section class="sources-group"><h2>{category} <small>/ {len(subset)}</small></h2>'+''.join(f'<div class="source-row"><a href="{esc(x["url"])}">{esc(x["name"])}</a><p>{esc(x["identity"])}</p><p>{esc(x["count"])}</p><a href="{esc(x["evidence"])}">背景依据 ↗</a></div>' for x in subset)+'</section>'
    write('publishers.html',layout('publishers.html','来源榜 · 发布方与专业依据','按发布方类型查看原始来源和身份依据。',f'<main id="main" class="wrap detail"><p class="eyebrow">TREELAW / PUBLISHER INDEX</p><h1>谁发布，依据是什么。</h1><p class="lead">每个来源只列一次，单项技能在对应目录展开。</p><p class="notice">按协会、专业律师、法律教师、厂商、个人分组。作者自述与独立核对分别说明。当前没有使用人数榜或效果评分。</p>{groups}</main>'))

def about():
    rows=''.join(f'<li>{esc(s["repo"])}：{s["skills"]}个Skill、{s["plugins"]}个插件；扫描{s["scanned"]}个技能文件。</li>' for s in AUDIT['sources'].values())
    body=f'''<main id="main" class="wrap detail prose"><p class="eyebrow">TREELAW / EDITORIAL NOTES</p><h1>按文件收录，按用途查找。</h1><h2>数量口径</h2><p>{AUDIT['skills']}个单项Skill、{AUDIT['plugins']}个插件，共{AUDIT['total']}项。另有{len(REFS)}项参考资料。插件与成员分别计数。</p><ul>{rows}</ul><h2>核验方法</h2><p>逐个读取SKILL.md，解析名称与描述，读取正文；插件读取真实plugin.json。记录路径、固定提交和SHA-256。相同文件按哈希合并，同一插件的Claude和Codex入口合并。38份英文平行版本不重复计数。初始化、技能管理、工作区辅助项排除；完整插件包仍保留这些文件。</p><p>排除路径和原因见仓库data/import-audit.json。上游格式异常单列。本轮核验文件与元数据，未执行全部技能。</p><h2>分类与作者</h2><p>China指中国大陆。US对应美国法律工作。澳大利亚、欧盟、以及使用时配置法域的通用方法放入Others。英文技能不直接归美国。法条、司法解释和案例是技能处理的资料类型，不表示随包提供法律数据库。</p><p>发布方按协会、专业律师、法律教师、厂商、个人分组；作者自述与独立核对分别说明。没有使用量或效果分。</p><h2>授权与下载</h2><p>获准再分发的上游ZIP保留原始署名、LICENSE、NOTICE（若有）、提交号和校验值。受限许可的技能只展示编辑整理的名称与用途，链接原始文件，不复制完整指令。单项Skill可能引用同套件的其他文件，下载入口提供完整套件。</p><h2>时间与维护</h2><p>核对日2026-11-02。单项首次发布时间未披露时留空，仓库创建与推送日期另列。本站提供静态正文、详情页、sitemap、JSON-LD与llms.txt。收录或AI引用效果另行观察。来源更正通过GitHub Issue提交。</p></main>'''
    write('about.html',layout('about.html','收录规则、数量与授权说明','按单项Skill、插件清单和固定版本核对的法律技能目录。',body))

def build():
    # Validate the absolute generated-directory boundary before recursive removal.
    assert OUT.resolve()==ROOT.resolve()/'site' and OUT.resolve()!=ROOT.resolve()
    if OUT.exists():shutil.rmtree(OUT)
    OUT.mkdir();shutil.copytree(ROOT/'assets',OUT/'assets')
    listing('index.html','按任务，找到法律技能。','每张卡片对应一个实际Skill或插件。法律研究、合同、诉讼、合规与文书工作，逐项查找。',DATA)
    for group,title,desc,en in [('China','中国法律技能。','面向中国大陆法律工作，逐项打开原始技能。',False),('US','Skills for US legal work.','US litigation, employment, clinic and legal education. General commercial workflows are under Others and the NDA task page.',True),('Others','其他法域与通用技能。','澳大利亚、欧盟及按项目配置法域的工作流。每项注明适用范围。',False)]:
        selected=[x for x in DATA if x['group']==group];listing(group+'/index.html',title,desc,selected,group,en)
        (ROOT/group/'README.md').write_text(f'# {group} · Treelaw\n\n{len(selected)}项：{sum(x["kind"]=="Skill" for x in selected)}个Skill、{sum(x["kind"]=="插件" for x in selected)}个插件。\n\n'+''.join(f'- [{x["name"]}]({BASE}/resources/{x["id"]}.html) — {x["kind"]} · {x["author"]} · [原始文件]({x["url"]})\n' for x in selected),encoding='utf-8')
    for slug,title,en,predicate in TASKS:listing('tasks/'+slug+'.html',title,'按具体任务比较技能；法域、作者和依赖在每项说明中列清。' if not en else 'Compare task-level skills. Check jurisdiction, author and dependencies per entry.',[x for x in DATA if predicate(x)],en=en)
    for x in DATA:detail(x)
    references();publishers();about()
    shutil.copy2(ROOT/'data/catalog.json',OUT/'catalog.json')
    write('llms.txt','# Treelaw Legal Skills & Plugins\n\n'+f'{AUDIT["skills"]} individual skills and {AUDIT["plugins"]} plugins. Each entry has a pinned source file, publisher evidence and license. Member counts and plugin counts are separate. Execution quality is untested.\n\n'+''.join(f'- [{x["name"]}]({BASE}/resources/{x["id"]}.html): {x["kind"]}; {x["group"]}; {x["author"]}; {x["license"]}\n' for x in DATA)+f'\n[Catalog JSON]({BASE}/catalog.json)\n[References]({BASE}/references.html)\n[Editorial policy]({BASE}/about.html)\n')
    write('sitemap.xml','<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{BASE}/{p}</loc><lastmod>2026-11-02</lastmod></url>' for p in pages if p.endswith('.html'))+'</urlset>')
    write('robots.txt','User-agent: *\nAllow: /\nSitemap: '+BASE+'/sitemap.xml\n');write('.nojekyll','')
    print(f'Built {len(DATA)} entries / {sum(p.endswith(".html") for p in pages)} HTML pages')
if __name__=='__main__':build()
