"""Editorial metadata only. Third-party instructions are never executed."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
items = []
def add(id, name, group, publisher, author, kind, tasks, summary, url, evidence, identity, published=None, updated=None, license="未见开放再分发许可", **extra):
    item = dict(id=id, name=name, group=group, publisher=publisher, author=author, kind=kind,
                tasks=tasks.split('|'), summary=summary, url=url, evidence=evidence, identity=identity,
                published=published, updated=updated, license=license, checked="2026-11-02",
                tested=False, systems=[], materials=[], languages=['中文'] if group=='China' else ['English'],
                jurisdictions=['中国大陆'] if group=='China' else ['美国法律工作'] if group=='US' else ['多法域，逐项确认'],
                dependencies='见原始使用说明', keywords='', access='原站阅读', **{})
    item.update(extra)
    items.append(item)
    return item

add('shanghai-enterprise','上海律协 · 企业法律顾问 AI 操作指引','China','协会','上海市律师协会','指南 / Prompt','非诉|诉讼|合规',
    '面向企业顾问的变量式提示词示例，涵盖合同审查、事实梳理与日常咨询。',
    'https://www.lawyers.org.cn/new/common-detail?id=49835e6e3485429ba83efcc34fec0618',
    'https://www.lawyers.org.cn/new/common-detail?id=49835e6e3485429ba83efcc34fec0618',
    '协会组织编制；2026-07-07业务研究指导委员会通过。', '2026-08-04',
    license='原站有转载条件；本目录只索引', systems=['中国社会主义法律体系'], materials=['法条','司法解释','案例'],
    keywords='合同审查 争议焦点 证据 时间线 用工 compliance contract review', dependencies='按示例准备脱敏材料与AI工具')
add('shanghai-community','上海律协 · 居村法律顾问 AI 指引','China','协会','上海市律师协会','指南 / Prompt','非诉|诉讼',
    '社区法律咨询、普法和法律文书的操作示例。2025版试行指引。',
    'https://info.lawyers.org.cn/info/71624f5df3184a90941f317aca231c18',
    'https://info.lawyers.org.cn/info/71624f5df3184a90941f317aca231c18','协会指引，列有撰稿律师及支持委员会。','2025-08-13',
    systems=['中国社会主义法律体系'], keywords='普法 法律咨询 起诉状 执行申请')
add('shuanglaw','爽律 ShuangLaw','China','专业律师','蔡诗爽 / zj-ai-lab','Skill','诉讼|非诉|合规',
    '刑事、民商事、合同与尽调工作流，配有文书质量检查方法。',
    'https://github.com/zj-ai-lab/shuanglv-legal-skills',
    'https://www.lawzj.cn/claprod_view.aspx?fid=t28%3A81%3A28&id=486&typeid=81',
    '卓建官网可核对律师身份；深圳律协材料列数字经济专业委员会任职。', updated='2026-08-20',
    license='ShuangLaw Professional Use License 1.0', created='2026-08-15', systems=['中国社会主义法律体系'],
    licenseUrl='https://github.com/zj-ai-lab/shuanglv-legal-skills/blob/main/LICENSE',
    licenseNote='允许律师、律所内部使用；收费软件或技能市场集成需书面授权。', access='原站获取', keywords='刑事辩护 尽职调查 合同审查 争议焦点')
add('panrui','潘睿 · 中国法律工作流','China','专业律师','潘睿','Skill','诉讼|非诉|合规',
    '串联法律材料、合同红线、劳动争议和 Word 交付的工作流。',
    'https://github.com/pa1nrui1/legal-skills','https://github.com/pa1nrui1/legal-skills',
    '作者自述为广东广和（长春）律师；本目录尚未独立核对执业身份。', updated='2026-07-03', license='MIT', created='2026-06-16',
    systems=['中国社会主义法律体系'], materials=['法条','司法解释','案例'], mirror='China/panrui',
    keywords='合同审查 红线 修订 Word 要素式起诉状 争议焦点 类案检索 劳动仲裁', access='仓库快照', dependencies='按子技能配置文书处理与检索工具')
add('legal-skills-chinese','Legal-Skills-Chinese','China','个人','THUYRan','Skill','诉讼|非诉',
    '法律检索、事实要素、争点识别、解释与论证的分步技能集合。',
    'https://github.com/THUYRan/Legal-Skills-Chinese','https://github.com/THUYRan/Legal-Skills-Chinese',
    '项目称由法律专业人员编写；首页未提供可逐项核对的作者名单。', updated='2026-08-22', license='CC BY-NC-ND 4.0', created='2026-05-20',
    systems=['中国社会主义法律体系'], materials=['法条','司法解释','案例'], keywords='类案检索 争议焦点 法律解释 证据 裁判')
add('senry-prompts','中文法律 Prompt 库','China','个人','SenryLee','Prompt','诉讼|非诉|涉外|合规',
    '按诉讼与非诉业务整理的提示词库，可用作法律任务指令的起点。',
    'https://github.com/SenryLee/legal-prompts','https://github.com/SenryLee/legal-prompts',
    '个人项目；未找到明确执业身份或所在律所证据。', updated='2026-07-22', license='MIT', created='2026-02-27',
    systems=['中国社会主义法律体系'], materials=['法条','案例'], mirror='China/senry-prompts',
    keywords='合同审查 劳动争议 尽职调查 数据合规 国际贸易 争议焦点', access='仓库快照', dependencies='支持文字输入的AI工具；检索任务另配法源')
add('haolvshi','好律狮法律技能包','China','厂商','律品汇科技（北京）有限公司','Skill','诉讼|非诉',
    '通过服务接口处理咨询、赔偿计算、合同审核与诉讼文书。',
    'https://github.com/mtcto/haolvshi-legal-skill','https://github.com/mtcto/haolvshi-legal-skill/blob/main/LICENSE',
    '许可证列明公司权利人；未见逐技能负责律师名单。', updated='2026-09-20', license='MIT No Attribution', created='2026-09-01',
    systems=['中国社会主义法律体系'], keywords='合同审查 起诉状 答辩状 赔偿计算', dependencies='Node ≥20；好律狮远端服务及其登录、收费条件', access='原站获取')
add('xiang-law','Law · 中国法律检索与材料处理','China','个人','XimilalaXiang','Skill','诉讼|非诉',
    '将法条与案例 API 检索、证据缺口分析和 Word 文书导出串联。',
    'https://github.com/XimilalaXiang/Law','https://github.com/XimilalaXiang/Law/blob/master/README.md',
    '个人仓库；本轮未核实法律执业背景。', updated='2026-04-19', created='2026-04-12',
    license='README称MIT；根目录未见LICENSE，暂不镜像', systems=['中国社会主义法律体系'], materials=['法条','案例'],
    keywords='类案检索 证据 争议焦点 起诉状 合同审查', dependencies='Python ≥3.9；法律API凭据；文书处理依赖', access='原站获取')
add('dri-ramos','DRI · Civil Defense Prompting Guide','US','协会','DRI / Frank Ramos','指南 / Prompt','诉讼',
    '美国民事被告代理的提示词与试用方法，涉及证据开示、动议和书面提交。',
    'https://www.dri.org/docs/default-source/center-law-public-policy/2026-ai-seminar/center-ai-prompting.pdf?sfvrsn=4739d618_6',
    'https://www.goldbergsegalla.com/news-and-knowledge/news/goldberg-segalla-expands-miami-presence-with-the-addition-of-attorney-frank-ramos/',
    'Frank Ramos为Goldberg Segalla合伙人，律所介绍其26年以上民事诉讼经历。','2026-03-10',
    systems=['普通法系'], materials=['案例'], keywords='civil defense litigation discovery motion drafting deposition')
add('writelaw','Write.law Prompt Library','US','法律教师','Joe Regalia / Write.law','Prompt','诉讼|非诉',
    '英文法律写作、摘要、改写与论证组织的专业提示库。',
    'https://write.law/ailibrary','https://law.unlv.edu/faculty/joseph-regalia',
    'UNLV法学教授；高校履历列法院书记员与多家律所执业经历。',
    systems=['普通法系'], keywords='legal memo brief drafting legal writing plain English', access='付费原站')
add('law-librarians','AI Law Librarians Prompt Library','US','法律教师','Rebecca Fordon 等法律图书馆工作者','Prompt','诉讼|非诉',
    '面向法律研究、教学与起草的社区提示词目录。',
    'https://www.ailawlibrarians.com/prompt-library/','https://www.ailawlibrarians.com/about-us/',
    '团队列多所法学院图书馆与法律教育岗位；社区投稿的作者分别核对。','2024-09-23',
    systems=['普通法系'], materials=['法条','案例'], keywords='legal research case law research teaching law librarian')
add('anthropic-legal','Claude for Legal · 官方插件集','US','厂商','Anthropic','Skill','诉讼|非诉|涉外|合规',
    '商业合同、公司、隐私、劳动与诉讼等插件；按具体技能与机构规则配置。',
    'https://github.com/anthropics/claude-for-legal','https://claude.com/blog/claude-for-the-legal-industry',
    '模型厂商官方发布；未见每项技能具名律师审阅名单。','2026-05-12','2026-10-29','Apache-2.0',
    mirror='US/anthropic-legal', systems=[], jurisdictions=['美国法律工作及跨法域任务；逐技能配置'],
    access='仓库快照', keywords='NDA contract review MSA employment due diligence privacy litigation',
    dependencies='Claude插件环境、机构playbook；第三方数据库账户单独配置')
for id, title, summary, kw in [
    ('nda-review','NDA 保密协议分流 / NDA triage','按机构采购方或销售方规则检查 NDA，并列出需法律团队处理的偏离项。','NDA non disclosure agreement review 保密协议'),
    ('saas-msa-review','SaaS / MSA 主服务协议审查','围绕软件服务及主协议条款，结合团队规则生成审查建议。','SaaS MSA limitation liability indemnity 服务协议'),
    ('vendor-agreement-review','供应商合同审查 / Vendor review','针对采购与供应商协议，读取本团队的审查立场。','vendor procurement supplier contract review 采购 合同审查'),
    ('amendment-history','合同修订沿革 / Amendment history','组织主合同与修改文件，跟踪条款的变更关系。','amendment history contract changes 合同变更'),
    ('stakeholder-summary','业务方摘要 / Stakeholder summary','将合同审查信息整理为业务团队可读的摘要。','in house counsel stakeholder summary 法务 合同摘要'),
    ('review','合同审查入口 / Commercial review','识别合同类型、主文与附件，再选择对应的审查流程。','contract redline review legal playbook 合同审查 修订')]:
    add('anthropic-'+id, title,'US','厂商','Anthropic','Skill','非诉|涉外',summary,
        'https://github.com/anthropics/claude-for-legal/tree/main/commercial-legal/skills/'+id,
        'https://github.com/anthropics/claude-for-legal',
        'Anthropic官方子技能；与插件集同源。', license='Apache-2.0', mirror='US/anthropic-legal', access='仓库快照',
        jurisdictions=['商业合同方法；适用法由项目配置'], keywords=kw, parent='anthropic-legal',
        dependencies='完整commercial-legal插件及机构playbook；下载链接为完整上游快照')
add('cocounsel','CoCounsel Prompt Library','US','厂商','Thomson Reuters / Practical Law律师编辑','产品工作流','诉讼|非诉|合规',
    '商业平台内的律师编辑提示库，支持收藏、分组和团队使用管理。',
    'https://legal.thomsonreuters.com/en/legal/criminal-law',
    'https://legal.thomsonreuters.com/en/legal/criminal-law','官方明确说明预置提示词由Practical Law律师编辑创建。',updated='2026-10-14',
    systems=['普通法系'], materials=['法条','案例'], keywords='legal research contract review Practical Law Westlaw', access='商业服务')
add('harvey-mtd','Harvey × Lexis · Motion to Dismiss','US','厂商','Harvey / LexisNexis','产品工作流','诉讼',
    '从起诉书分析、策略确认到法律检索和驳回动议起草的流程说明。',
    'https://www.harvey.ai/blog/motion-to-dismiss-workflow-lexisnexis',
    'https://www.harvey.ai/blog/motion-to-dismiss-workflow-lexisnexis','厂商联合公告；列明Lexis法源与Shepard’s。','2026-10-07',
    systems=['普通法系'], materials=['法条','案例'], keywords='motion to dismiss complaint defense litigation', access='商业服务')
add('anytime','Anytime AI Prompt Library','US','厂商','Anytime AI','产品工作流','诉讼',
    '面向美国原告律师团队，把成功问答保存并共享为提示库。',
    'https://www.anytimeai.ai/resources/blog/anytime-ai-unveils-prompt-library-to-boost-collaboration-and-efficiency',
    'https://www.anytimeai.ai/resources/blog/anytime-ai-unveils-prompt-library-to-boost-collaboration-and-efficiency',
    '厂商公告；未列单条Prompt负责律师。','2024-10-10',systems=['普通法系'],keywords='plaintiff litigation prompt library',access='商业服务')
add('legalon-prompts','LegalOn · In-house Legal Prompt Guide','US','厂商','LegalOn / Eileen Policarpio','指南 / Prompt','非诉|合规',
    '企业法务的英文提示词示例，涉及合同审查、需求受理和事项管理。',
    'https://www.legalontech.com/post/chatgpt-prompts-for-lawyers','https://www.legalontech.com/post/chatgpt-prompts-for-lawyers',
    '作者职务为传播经理；原文称与法律工程团队共同整理。',updated='2026-06-23',
    jurisdictions=['英文企业法务方法；具体法域按任务设置'],keywords='in house counsel NDA contract review legal intake board policy', systems=[])
add('lawve','Lawve · Awesome Legal Skills','Others','个人','Lawve 社区及各原作者','Skill 目录','诉讼|非诉|涉外|合规',
    '跨法域技能聚合目录。逐项追溯原作者、适用法与许可证。',
    'https://github.com/lawve-ai/awesome-legal-skills','https://lawve.ai/about',
    '社区平台称进行发布前审查；条目作者背景分别核对。',updated='2026-10-19',license='根目录CC BY-NC-ND 4.0；单项另核',created='2025-12-18',
    keywords='international cross border sanctions trade arbitration 跨境 国际贸易 涉外', access='原站获取')
add('lexis-canada','Lexis+ AI · Canada Prompt Library','Others','厂商','LexisNexis Canada','产品工作流','诉讼|非诉',
    '加拿大版提示库发布说明，作为加拿大法律工作入口单独收录。',
    'https://www.lexisnexis.com/blogs/en-ca/b/canadian-product-spotlight/posts/new-release-lexis-plus-ai-prompt-library',
    'https://www.lexisnexis.com/blogs/en-ca/b/canadian-product-spotlight/posts/new-release-lexis-plus-ai-prompt-library',
    'LexisNexis加拿大产品官方公告。','2025-05-12',systems=['混合法系'],jurisdictions=['加拿大；具体省份另核'],
    keywords='Canada legal research prompt library Canadian law',access='商业服务')
(ROOT/'data/catalog.json').write_text(json.dumps(items,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f'{len(items)} resources written')
