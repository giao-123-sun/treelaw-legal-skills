"""Dependency-free static directory. Every resource has crawlable HTML."""
import html
import json
import os
import shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'site'
BASE=os.environ.get('SITE_URL','https://giao-123-sun.github.io/treelaw-legal-skills').rstrip('/')
REPO='https://github.com/giao-123-sun/treelaw-legal-skills'
DATA=json.loads((ROOT/'data/catalog.json').read_text(encoding='utf-8'))
MIRRORS={x['path']:x for x in json.loads((ROOT/'data/mirrors.json').read_text(encoding='utf-8'))}
ORDER=['协会','专业律师','法律教师','厂商','个人']
EN={'协会':'Association','专业律师':'Legal practitioner','法律教师':'Legal educator','厂商':'Vendor','个人':'Individual / community','诉讼':'Litigation','非诉':'Transactional','涉外':'Cross-border','合规':'Compliance','普通法系':'Common law','混合法系':'Mixed system','中国社会主义法律体系':'Chinese socialist legal system','法条':'Statutes','司法解释':'Judicial interpretations','案例':'Case law','指南 / Prompt':'Guide / Prompt','产品工作流':'Product workflow','Skill 目录':'Skill directory','原站阅读':'Read at source','原站获取':'Get at source','付费原站':'Paid library','仓库快照':'Repository archive','商业服务':'Commercial service'}
EN_SUMMARY={
'dri-ramos':'Civil defense prompting guidance covering discovery, motions, written submissions, and pilot evaluation.',
'writelaw':'Prompts for English legal drafting, editing, summaries, and argument structure. Paid library.',
'law-librarians':'Community-contributed prompts for legal research, teaching, drafting, and productivity.',
'anthropic-legal':'Official plugins for commercial, corporate, privacy, employment, litigation, and other legal workflows. Configure jurisdiction and firm policies per skill.',
'anthropic-nda-review':'Triage inbound NDAs against attorney-reviewed sales-side or purchasing-side playbook positions.',
'anthropic-saas-msa-review':'Review SaaS and master services agreements using the team’s commercial playbook.',
'anthropic-vendor-agreement-review':'Review supplier and procurement agreements against configured team positions.',
'anthropic-amendment-history':'Organize a base contract and its amendments to trace changes across documents.',
'anthropic-stakeholder-summary':'Turn commercial legal review information into a business-facing summary.',
'anthropic-review':'Identify the contract type and attached documents, then route to the relevant commercial review workflow.',
'cocounsel':'A commercial prompt library with Practical Law attorney-editor content, favorites, collections, and team administration.',
'harvey-mtd':'A published workflow for complaint analysis, strategy confirmation, research, and motion drafting using Lexis sources.',
'anytime':'Save and share successful prompts within a platform serving US plaintiff-side legal teams.',
'legalon-prompts':'An in-house legal prompt guide for contract review, request intake, and matter management.',
}
EN_NAMES={
 'anthropic-legal':'Claude for Legal · Official plugins',
 'anthropic-nda-review':'NDA review & triage',
 'anthropic-saas-msa-review':'SaaS / MSA agreement review',
 'anthropic-vendor-agreement-review':'Vendor agreement review',
 'anthropic-amendment-history':'Contract amendment history',
 'anthropic-stakeholder-summary':'Stakeholder summary',
 'anthropic-review':'Commercial contract review',
}
TASKS=[
('contract-review','合同审查 AI Skills 与提示词','Contract review, redlining, and in-house legal workflows.','China',lambda x:'非诉' in x['tasks']),
('litigation','类案检索、证据与争议焦点梳理','Case research, evidence organization, and litigation drafting.','China',lambda x:'诉讼' in x['tasks']),
('nda-review','NDA Review & Contract Redlining Skills','Find NDA triage, SaaS/MSA review, and commercial playbook resources.','US',lambda x:'非诉' in x['tasks']),
('legal-research','Legal Research & Litigation Prompts','Compare research, discovery, civil defense, and motion-drafting resources.','US',lambda x:'诉讼' in x['tasks']),
]
paths=[]
def esc(v):return html.escape(str(v),quote=True)
def label(v,en=False):return EN.get(v,v) if en else v
def link(path,current):return os.path.relpath(OUT/path,(OUT/current).parent).replace('\\','/')
def summary(x,en):return EN_SUMMARY.get(x['id'],x['summary']) if en else x['summary']
def name(x,en):return EN_NAMES.get(x['id'],x['name']) if en else x['name']
def write(path,text):
    p=OUT/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding='utf-8');paths.append(path)
def layout(path,title,description,body,en=False,schema=None):
    root=link('index.html',path)
    brand=f'<a class="brand" href="{root}" aria-label="Treelaw home"><img src="{link("assets/treelaw-mark.svg",path)}" alt="">Treelaw<small>LEGAL SKILLS DIRECTORY</small></a>'
    structured={'@context':'https://schema.org','@type':'CollectionPage','name':title,'description':description,'url':BASE+'/'+path}
    if schema:structured.update(schema)
    js=json.dumps(structured,ensure_ascii=False).replace('<','\\u003c')
    return f'''<!doctype html><html lang="{'en' if en else 'zh-CN'}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)} · Treelaw</title><meta name="description" content="{esc(description)}"><link rel="canonical" href="{BASE}/{path}"><meta property="og:title" content="{esc(title)} · Treelaw"><meta property="og:description" content="{esc(description)}"><meta property="og:type" content="website"><meta property="og:url" content="{BASE}/{path}"><meta property="og:image" content="{BASE}/assets/treelaw-mark.svg"><link rel="icon" href="{link('assets/treelaw-mark.svg',path)}"><link rel="stylesheet" href="{link('assets/style.css',path)}"><script type="application/ld+json">{js}</script><script src="{link('assets/app.js',path)}" defer></script></head><body><a class="skip" href="#main">{'Skip to content' if en else '跳到正文'}</a><header><div class="wrap head">{brand}<nav class="nav" aria-label="Main"><a href="{root}">{'Directory' if en else '资源目录'}</a><a href="{link('publishers.html',path)}">{'Publishers' if en else '来源榜'}</a><a class="repo" href="{REPO}" target="_blank" rel="noopener">GitHub ↗</a></nav></div></header>{body}<section class="tasks"><div class="wrap"><b>{'Browse by task' if en else '从工作任务开始'}</b>{''.join(f'<a href="{link("tasks/"+slug+".html",path)}">{esc(t)}</a>' for slug,t,_,_,_ in TASKS)}</div></section><footer><div class="wrap">{brand}<p>{'Curated by Treelaw. Original works belong to their publishers. This directory presents resources and links; listing is not publisher endorsement. Archives retain the upstream license and attribution. Output quality has not been evaluated.' if en else 'Treelaw 负责整理与展示，作品归原发布方。收录不表示发布方为 Treelaw 背书。下载优先回到原站；有明确再分发许可的快照保留原署名和许可证。当前未做输出质量评测。'}<br><a href="{link('about.html',path)}">{'Editorial policy & licenses' if en else '收录规则与授权说明'}</a> · <a href="{link('llms.txt',path)}">llms.txt</a> · 2026-11-02</p></div></footer></body></html>'''
def card(x,path,en=False):
    keywords=' '.join([x['name'],x['author'],x['keywords'],x['summary'],summary(x,True),*x['tasks'],*x['jurisdictions']])
    attrs=dict(text=keywords,task=x['tasks'],publisher=[x['publisher']],system=x['systems'],material=x['materials'],kind=[x['kind']],access=[x['access']],name=x['name'],date=x['updated'] or x['published'] or '')
    mirror=x.get('mirror');date=x['published'] or x.get('created')
    date_label=('First published' if en else '发布') if x['published'] else ('Repo created' if en else '仓库创建') if x.get('created') else ('First published' if en else '发布')
    download=f'<a href="{REPO}/blob/main/{mirror}/README.md" target="_blank" rel="noopener">{label("仓库快照",en)} ↓</a>' if mirror else ''
    return f'''<article class="card" data-filter="{esc(json.dumps(attrs,ensure_ascii=False))}"><div class="topline"><span class="badge">{esc(label(x['publisher'],en))}</span><span>{esc(label(x['kind'],en))}</span><span>{x['group']}</span></div><h2><a href="{link('resources/'+x['id']+'.html',path)}">{esc(name(x,en))}</a></h2><p>{esc(summary(x,en))}</p><div class="tags">{' · '.join(esc(label(t,en)) for t in x['tasks'])}{' · '+('Subskill' if en else '同源子技能') if x.get('parent') else ''}</div><div class="author">{esc(x['author'])}</div><div class="meta">{date_label} {date or ('Not disclosed' if en else '未披露')} · {esc(x['license'])}</div><div class="actions"><a href="{link('resources/'+x['id']+'.html',path)}">{'View details' if en else '背景与用途'} →</a><a href="{esc(x['url'])}" target="_blank" rel="noopener">{'Original source' if en else '原始来源'} ↗</a>{download}</div></article>'''
def listing(path,title,desc,items,group=None,en=False):
    groups=[('All','全部'),('China','中国'),('US','美国'),('Others','其他法域')]
    nav=''.join(f'<a class="{"active" if (g==group or (g=="All" and group is None)) else ""}" href="{link("index.html" if g=="All" else g+"/index.html",path)}">{g if en else zh}<small>{len(DATA) if g=="All" else sum(x["group"]==g for x in DATA)}</small></a>' for g,zh in groups)
    fields=[('task','业务类型','Practice',['诉讼','非诉','涉外','合规']),('publisher','发布方','Publisher',ORDER),('system','法系','Legal system',['中国社会主义法律体系','大陆法系','普通法系','混合法系']),('material','涉及资料','Legal material',['法条','司法解释','案例']),('kind','资源形式','Resource type',sorted(set(x['kind'] for x in DATA))),('access','获取方式','Access',sorted(set(x['access'] for x in DATA)))]
    filters=''.join(f'<label>{english if en else zh}<select id="{key}" name="{key}"><option value="">{"All" if en else "全部"}</option>'+''.join(f'<option value="{esc(v)}">{esc(label(v,en))}</option>' for v in vals)+'</select></label>' for key,zh,english,vals in fields)
    sorteditems=sorted(items,key=lambda x:ORDER.index(x['publisher']))
    body=f'''<main id="main" class="wrap"><section class="hero"><div><p class="eyebrow">TREELAW / THE LEGAL RESOURCE INDEX</p><h1>{esc(title)}<span>{'Skills, prompts & professional practice guides' if en else '法律技能、提示词与专业实践指南'}</span></h1></div><p class="hero-note">{esc(desc)}<br><strong>{'Start with the task. Check the author. Go to the source.' if en else '先看任务，再看作者，最后回到原始来源。'}</strong></p></section><nav class="countries" aria-label="Jurisdiction">{nav}<span class="stamp">REVIEWED 2026.11.02</span></nav><div class="browse"><form class="filters" id="filters"><h2>{'Refine your search' if en else '筛选资源'}</h2>{filters}<button id="clear-filters" class="reset" type="button">{'Clear filters' if en else '清除筛选'}</button><p>{'Jurisdiction, language and legal system are recorded separately. Unspecified jurisdictions stay unspecified.' if en else '国家、语言与法系分别记录。法系仅作目录分类。通用方法不直接标为某国法律规则。'}</p></form><section aria-label="Resources"><label class="skip" for="query">Search</label><input class="search" id="query" type="search" placeholder="{'Search NDA, discovery, publisher…' if en else '搜索任务、作者或技能，如：合同审查、类案检索、NDA'}"><div class="quick">{''.join(f'<button type="button" data-query="{q}">{q}</button>' for q in (['NDA','contract review','discovery','legal research'] if en else ['合同审查','类案检索','争议焦点','NDA','合规']))}</div><div class="result-bar"><span aria-live="polite"><b id="count">{len(items)}</b> {'resources' if en else '项资源'}</span><label>{'Sort ' if en else '排序 '}<select id="sort"><option value="source">{'Publisher grouping' if en else '按发布方分组'}</option><option value="recent">{'Latest recorded update' if en else '最近记录更新'}</option><option value="name">{'Name' if en else '名称'}</option></select></label></div><div class="cards">{''.join(card(x,path,en) for x in sorteditems)}</div><p id="empty" class="empty" hidden>{'No matching resources. Clear a filter or try another task.' if en else '暂无匹配资源。可清除筛选，或换一个任务关键词。'}</p><noscript><p>筛选需要 JavaScript。所有资源和详情链接已在正文显示。</p></noscript></section></div></main>'''
    schema={'mainEntity':{'@type':'ItemList','numberOfItems':len(items),'itemListElement':[{'@type':'ListItem','position':i+1,'url':BASE+'/resources/'+x['id']+'.html','name':x['name']} for i,x in enumerate(sorteditems)]}}
    write(path,layout(path,title,desc,body,en,schema))
def detail(x):
    path='resources/'+x['id']+'.html';en=x['group']=='US';mir=MIRRORS.get(x.get('mirror'))
    facts=[('发布方 / Publisher',label(x['publisher'],en)+' · '+x['author']),('身份依据 / Evidence',x['identity']),('法域 / Jurisdiction','；'.join(x['jurisdictions'])),('法系 / Legal system','；'.join(x['systems']) or '未指定 / Not specified'),('语言 / Language',' / '.join(x['languages'])),('任务 / Practice',' / '.join(label(v,en) for v in x['tasks'])),('资料 / Materials',' / '.join(label(v,en) for v in x['materials']) or '未逐项标注 / Not itemized'),('首次发布 / Published',x['published'] or '未披露 / Not disclosed'),('仓库创建 / Repo created',x.get('created','不适用 / N/A')),('更新线索 / Update',x['updated'] or '未记录 / Not recorded'),('核对日期 / Checked',x['checked']),('授权 / License',x['license']),('依赖 / Dependencies',x['dependencies']),('效果测试 / Evaluation','尚未运行 / Not run')]
    extra=''
    if mir:
        facts.extend([('镜像版本 / Commit',mir['commit']),('SHA-256',mir['sha256'])])
        extra=f'<a href="{REPO}/blob/main/{mir["path"]}/README.md">仓库下载与许可证 / Archive & license ↓</a>'
    body=f'''<main id="main" class="wrap detail"><div class="crumb"><a href="{link('index.html',path)}">Treelaw</a> / <a href="{link(x['group']+'/index.html',path)}">{x['group']}</a> / {esc(label(x['kind'],en))}</div><span class="badge">{esc(label(x['publisher'],en))}</span><h1>{esc(name(x,en))}</h1><p class="lead">{esc(summary(x,en))}</p><div class="actions"><a href="{esc(x['url'])}" target="_blank" rel="noopener">原始来源 / Original source ↗</a><a href="{esc(x['evidence'])}" target="_blank" rel="noopener">发布方依据 / Publisher evidence ↗</a>{extra}</div><dl class="facts">{''.join(f'<dt>{esc(k)}</dt><dd>{esc(v)}</dd>' for k,v in facts)}</dl><p class="notice">{esc(x.get('licenseNote','本页只展示目录信息。下载和使用遵循原发布方许可。 / This page is a directory record. Upstream terms govern download and use.'))}</p><div class="prose"><h2>日期与版本 / Dates & versions</h2><p>首次发布、仓库创建与最近推送分别记录。“更新线索”来自仓库推送或页面更新日期，未代表每个子技能的修改日。归档使用固定提交；原站可能已有更新。 / Release, repository creation and last push are separate dates. A repository push does not date each skill.</p></div></main>'''
    schema={'@type':'CreativeWork','name':x['name'],'description':summary(x,en),'author':{'@type':'Organization' if x['publisher'] in ['协会','厂商'] else 'Person','name':x['author']},'citation':[x['url'],x['evidence']],'inLanguage':x['languages'],'isAccessibleForFree':x['access'] not in ['商业服务','付费原站']}
    if x['published']:schema['datePublished']=x['published']
    write(path,layout(path,x['name'],summary(x,en),body,en,schema))
def build():
    OUT.mkdir(exist_ok=True)
    shutil.copytree(ROOT/'assets',OUT/'assets',dirs_exist_ok=True)
    listing('index.html','法律技能与提示词。','按法域、法律任务和发布方查找资源。每项列明专业背景、日期、授权与原件入口。',DATA)
    for group,title,desc,en in [('China','中国法律 Skills 与提示词','诉讼、非诉、涉外与合规任务，原作者和专业背景逐项说明。',False),('US','Legal skills for legal work.','A source-attributed directory for US lawyers and in-house counsel. Browse skills, prompts and practice guides.',True),('Others','其他法域与跨境资源','加拿大与跨法域社区资源。适用范围按条目说明，逐步补充。',False)]:
        listing(group+'/index.html',title,desc,[x for x in DATA if x['group']==group],group,en)
        text=f'# {group} · Treelaw Legal Skills\n\n按发布方分组；原件、许可与身份依据见详情。\n\n'
        for x in DATA:
            if x['group']==group:text+=f'- [{x["name"]}]({x["url"]}) — {x["publisher"]} · {x["kind"]} · {" / ".join(x["tasks"])} · {x["license"]}\n'
        (ROOT/group/'README.md').write_text(text,encoding='utf-8')
    for slug,title,desc,group,predicate in TASKS:listing('tasks/'+slug+'.html',title,desc,[x for x in DATA if x['group']==group and predicate(x)],group,group=='US')
    for x in DATA:detail(x)
    groups=''
    for category in ORDER:
        # Do not inflate publisher counts with subskills from the same repository.
        selected=[x for x in DATA if x['publisher']==category and not x.get('parent')]
        groups+=f'<section class="sources-group"><h2>{category} <small> / {len(selected)}</small></h2>'+''.join(f'<div class="source-row"><a href="resources/{x["id"]}.html">{esc(x["name"])}</a><p>{esc(x["identity"])}</p><a href="{esc(x["evidence"])}">查看依据 ↗</a></div>' for x in selected)+'</section>'
    write('publishers.html',layout('publishers.html','来源榜 · 看发布方与专业依据','按协会、专业律师、法律教师、厂商和个人整理发布方，不使用数字信用等级。',f'<main id="main" class="wrap detail"><p class="eyebrow">TREELAW / PUBLISHER INDEX</p><h1>谁发布，依据是什么。</h1><p class="lead">协会、专业律师、法律教师、厂商、个人。按这五类查阅原作者及背景证据。</p><p class="notice">分组次序是目录顺序。身份自述与独立核对分别标明。当前没有使用人数或输出质量排名。同一仓库的子技能合并计数。</p>{groups}</main>'))
    about='''<main id="main" class="wrap detail prose"><p class="eyebrow">TREELAW / EDITORIAL NOTES</p><h1>来源清楚，边界清楚。</h1><h2>我们做什么</h2><p>Treelaw 整理法律 Skill、Prompt、指南和产品工作流的原始入口。四种交付形式分开标注。本站不自动执行、安装第三方内容。</p><h2>如何分类</h2><p>一级目录为 China、US、Others。按服务的法律工作划分，不按作者国籍或页面语言推定法域。China目前指中国大陆；US含美国法律工作与英文通用商业方法，具体范围写在详情中。加拿大属混合法系，不能据此推定每条资源同时覆盖魁北克和其他省份。</p><p>法系筛选包括中国社会主义法律体系、大陆法系、普通法系和混合法系。司法解释、法条和案例属于资料类型，单独筛选。标签表示技能涉及的材料，不表示随包附赠法律数据库。未标法系的通用方法不参与法系匹配。</p><h2>发布方与排行</h2><p>来源榜依次展示协会、专业律师、法律教师、厂商与个人。行业身份、独立核对和作者自述写明。未采集使用数据，不显示使用量、效果分或虚构星级。</p><h2>原件与许可证</h2><p>所有条目保留原站链接。当前归档三个明确采用MIT或Apache-2.0的仓库，保存完整原始ZIP、LICENSE、上游NOTICE（若有）、提交号与SHA-256。其他资源只作链接索引。转载条件未明确的材料不复制全文；原始作者可通过GitHub issue提交更正。</p><h2>日期与核验</h2><p>本轮资料核对日为2026-11-02。首次发布、仓库创建、推送日期分别记录；未知字段留空。完成的是来源与授权资料核对，输出效果未测。GitHub快照是归档，不等于经过Treelaw运行验收。</p><h2>搜索与开放目录</h2><p>每项资源都有静态正文、独立URL和引用。站点提供sitemap.xml、llms.txt与JSON目录。SEO/GEO本轮验收检查可读性及链接结构；搜索引擎收录和AI引用另行观察。</p><p>联系方式：通过仓库 Issues 提交来源、许可或署名更正。</p></main>'''
    write('about.html',layout('about.html','收录规则、来源与授权说明','Treelaw法律技能目录的分类、发布方、日期和再分发规则。',about))
    shutil.copy2(ROOT/'data/catalog.json',OUT/'catalog.json')
    write('llms.txt','# Treelaw Legal Skills Directory\n\nSource-attributed directory of legal skills, prompts and guides. China, US and Others are jurisdiction-oriented groups. No usage rankings or output-quality scores have been measured. Publisher categories are not numerical trust scores.\n\n'+''.join(f'- [{x["name"]}]({BASE}/resources/{x["id"]}.html): {x["group"]}; {x["publisher"]}; {x["kind"]}; {x["license"]}\n' for x in DATA)+'\n## Data and policy\n- [Catalog JSON]('+BASE+'/catalog.json)\n- [Editorial policy]('+BASE+'/about.html)\n')
    write('sitemap.xml','<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{BASE}/{p}</loc><lastmod>2026-11-02</lastmod></url>' for p in paths if p.endswith('.html'))+'</urlset>')
    write('robots.txt','User-agent: *\nAllow: /\nSitemap: '+BASE+'/sitemap.xml\n')
    write('.nojekyll','')
    print(f'Built {len(DATA)} resource records; {sum(p.endswith(".html") for p in paths)} HTML pages')
if __name__=='__main__':build()
