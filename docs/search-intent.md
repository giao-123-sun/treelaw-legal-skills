# 法律 Skill 目录：搜索意图与页面安排

日期：2026-11-02。范围：中国律师、中国法务、中国涉外律师、美国律师、美国法务。方法：7 条公开网页搜索抽样，并打开官方页面核对。未采集搜索量、点击率或 AI 产品回答；下述搜索词是选题假设，不能作为用户流量统计。

## 页面先回答什么

用户通常带着工作任务来找资源：审合同、找类案、梳理证据、准备 discovery、核对 NDA。他需要看到作者是谁、适用哪个法域、输入什么、输出什么、如何取得原件。目录应同时覆盖「任务 + 提示词」和「任务 + AI skill」两种表达。

一级保留 China、US、Others。任务使用诉讼、非诉、涉外、合规。发布方标签使用协会、专业律师、法律教师、厂商、个人；身份已核对和身份待核对分别记录。分类顺序属于目录的编辑排序，不解释为实际输出质量排名。

## 五类读者的候选搜索词

| 人群 | 候选查询 | 想得到的结果 | 优先页面 |
|---|---|---|---|
| 中国律师 | 类案检索 AI 提示词；争议焦点梳理 skill；证据目录生成 提示词；民事起诉状 AI skill；请求权基础分析 提示词 | 检索方案、证据对应表、争点清单、文书初稿 | China / 诉讼；类案检索与争点梳理 |
| 中国法务 | 合同审查 AI 提示词；采购合同审查 skill；劳动合同解除 风险审查 AI；合同修订 Word 留痕；法律法规司法解释 核验 skill | 风险表、修订稿、合规清单、可回源依据 | China / 非诉；China / 合规；合同审查 |
| 中国涉外律师 | 英文合同审查 提示词；NDA 审查 skill；跨境并购 尽职调查 AI；境外用工 合规 AI；FIDIC 合同审查 提示词 | 原文条款定位、中英风险说明、法域条件、尽调清单 | Others / 涉外；跨境合同与尽调 |
| 美国律师 | legal research AI prompts; deposition summary AI skill; discovery response drafting prompts; motion to dismiss AI workflow; case law citation checking skill | Research memo、deposition issue map、discovery response、motion draft | US / Litigation；Legal research and litigation |
| 美国法务 | NDA review AI skill; contract redlining prompts; in-house counsel prompt library; SaaS agreement review playbook; DPA review AI prompts | NDA deviations、redline、review playbook、business summary | US / Transactional；NDA and contract review |

以上是本次选题建议。词语组合来自任务特点和抽样页面的用语；没有证据表明每一条都存在固定搜索量。

## 实际搜索记录

以下为本次提交给网页搜索工具的原始查询。返回结果会随时间变化。只以发布方原站支持收录判断。

| 查询 | 本次观察 | 对目录的影响 |
|---|---|---|
| 律师 AI 类案检索 争议焦点 提示词 skill | 出现工具目录及律协指引等结果；专业任务词与 skill 用语同时存在 | 搜索字段同时放入类案、案例、争点、证据等任务别名 |
| 企业法务 合同审查 AI 提示词 skill | 出现上海律协企业法律顾问指引；也混有个人工具市场和厂商页面 | 将协会、厂商和个人的身份依据单列 |
| 涉外律师 英文合同 NDA 审查 AI 提示词 | 本次结果偏合同审查通用内容，未获得同等清晰的涉外律师专业提示词原站 | 涉外分类只挂有实际证据的内容；用英文检索补查 NDA、due diligence |
| legal AI prompts NDA review in house counsel | 命中 LegalOn 面向 in-house 的公开提示词文章 | 英文入口用 NDA、contract review、in-house counsel，不只写 legal skill |
| lawyer AI skill deposition discovery motion to dismiss prompt github | 命中 KRASA-AI/legal-ai-skills 的 deposition、discovery 类独立提示文件 | 美国诉讼页用程序任务词；开源作者身份和许可另审 |
| cross border M&A due diligence AI prompts counsel | 命中 Dentons 的跨境 M&A 风险实务文章，也有非机构提示词结果 | 实务文章与可使用 Prompt 分开标注；不把谈 AI 风险的文章当 AI Skill |
| site.lawyers.org.cn 涉外 AI 提示词 | 命中律师协会 AI 使用指引及案例附件 | “协会发布”可以形成来源入口；用途依文中任务标注 |

核对的主要原站：

- [上海律协：律师企业法律顾问服务 AI 应用操作指引（2026）](https://www.lawyers.org.cn/new/common-detail?id=49835e6e3485429ba83efcc34fec0618)：页面日期 2026-08-04；2026-07-07 表决通过。包含合同审查、咨询、事实梳理等提示词参考。页面有转载条件，目录先提供原文入口。
- [LegalOn：ChatGPT Prompts for In-House Lawyers & Legal Teams](https://www.legalontech.com/post/chatgpt-prompts-for-lawyers)：页面标注更新 2026-06-23。作者 Eileen Policarpio 为 Communications Manager，正文说明与 legal engineering team 合作。归为厂商发布。
- [KRASA-AI/legal-ai-skills](https://github.com/KRASA-AI/legal-ai-skills)：检索结果显示独立提示文件，含 deposition transcript、discovery response。此次搜索意图研究未完成作者身份与再分发许可审查。
- [Dentons：Canada-US M&A 中的 AI 风险](https://www.dentons.com/en/insights/articles/2026/august/10/no-single-rulebook-ai-risk-in-cross-border-canada-us-part-2)：2026-08-10，跨境尽调实务文章。它支持任务用语，不是可安装 Skill。
- [上海律协：居（村）法律顾问 AI 指引](https://info.lawyers.org.cn/info/71624f5df3184a90941f317aca231c18)：已有目录候选，可链接具体示例。

## 本版页面安排

先建 3 个国家目录页和少量有实际内容的任务页。资源详情页用可抓取的 HTML 正文，筛选作为增强功能。避免为每个筛选组合生成重复页面。

| 页面 | 建议标题 | 正文必须包含 |
|---|---|---|
| China | 中国法律 AI Skills 与提示词：诉讼、合同审查、合规｜Treelaw | 分类资源、发布方、发布日期、原件入口 |
| US | US Legal AI Skills & Prompts for Lawyers and In-House Counsel · Treelaw | English descriptions, jurisdiction, publisher, license, source |
| Others | 涉外与其他法域法律 Skills / Cross-border Legal Skills｜Treelaw | 实际法域、语言、任务；未明确法域的条目如实标注 |
| 中国合同审查 | 合同审查 AI 提示词与 Skills｜Treelaw | 合同类型、审查立场、输出是风险表还是 Word 修订稿 |
| 中国诉讼 | 类案检索、证据与争议焦点梳理 Skills｜Treelaw | 检索、事实整理、文书生成分清；注明数据库依赖 |
| US NDA | NDA Review & Contract Redlining AI Skills · Treelaw | Playbook inputs, governing law, output format, source |
| US litigation | Legal Research, Discovery & Litigation AI Prompts · Treelaw | Research versus drafting, procedural task, publisher evidence |

未找到支持某个细分任务的资源时，先不创建该任务页。资源介绍和链接必须先于搜索优化。

## 发布前检查

1. 详情页有独立标题、描述、原始发布者、核验日期、适用法域、授权文本链接。
2. 首次发布日期未知就写未知。仓库创建时间、最近提交时间、文章更新时间分列。
3. HTML 自带正文和普通链接。关闭 JavaScript 后仍可查看资源及原始入口。
4. Sitemap 只收录实际页面。Canonical 指向公开网址。未上线前不填写虚构生产域名。
5. 中英文页分别设置语言；只有内容对应时才互设 hreflang。
6. 结构化数据写 CollectionPage、ItemList 和 CreativeWork 等实际实体；不虚构星级、下载量、评分与律师认证。
7. llms.txt 用作目录说明和链接清单。可读性验收与搜索引擎收录结果分别记录。
8. 页面明确 Treelaw 负责整理展示，作品归原发布方；下载入口与许可证对应。

本次参考本地 geo 技能的「可抓取性、可抽取事实块、采样与归因」部分。没有运行 AI 回答可见性测评，也未测公开站点收录。站点上线后再用以上任务词检查收录及实际回答引用，记录查询、日期、产品、回答和链接。
