# Treelaw · Global Legal Skills & Prompts

面向律师与企业法务的法律技能、提示词和实务指南目录。按 **China / US / Others** 整理，支持诉讼、非诉、涉外、合规、发布方、法系和资料类型筛选。

**[浏览静态目录](https://giao-123-sun.github.io/treelaw-legal-skills/)** · [China](China/README.md) · [US](US/README.md) · [Others](Others/README.md)

A source-attributed directory for lawyers and in-house counsel. Find legal research prompts, NDA review skills, contract redlining workflows and litigation practice guides. Each record identifies the original publisher, jurisdiction, dates, license and access method.

## 本版收录

24项资源：China 8项、US 14项、Others 2项。包含6项同源Anthropic子技能；扣除子技能后为18个资源入口。源自17个发布方项目／机构组合，上海律协的两份指南单独列出。收录统计按条目计算，不按内部Prompt数量放大。

- **协会**：上海律协、DRI。
- **专业律师**：爽律、潘睿工作流。作者自述与独立核对在详情中分开。
- **法律教师**：Write.law、AI Law Librarians。
- **厂商**：Anthropic、Thomson Reuters、Harvey / LexisNexis、Anytime AI、LegalOn、好律狮、LexisNexis Canada。
- **个人／社区**：Legal-Skills-Chinese、SenryLee、XimilalaXiang、Lawve。

以上为来源分组。当前没有使用量榜或质量评分。已核对原站、背景资料及许可；未执行第三方技能、未测输出效果。

## 简单结构

```text
China/ US/ Others/   分类索引；获准归档的上游ZIP和许可证
data/catalog.json    条目与筛选字段，编辑入口
data/mirrors.json    固定提交、文件大小、SHA-256
assets/             页面样式、筛选脚本、Treelaw标识
scripts/build.py    生成静态HTML、任务页、JSON-LD、sitemap、llms.txt
scripts/check.py    内容、链接与归档校验
docs/               搜索意图、交付记录
.github/workflows/  GitHub Pages自动发布
```

静态站不需要账户、数据库、API密钥或Node。GitHub Pages发布时使用Python 3.12标准库生成。网页阅读与筛选不需要安装任何程序。

## 本地预览与更新

```sh
python scripts/build.py
python scripts/check.py
python -m http.server 3410 --bind 127.0.0.1 --directory site
```

打开 `http://127.0.0.1:3410`。修改 `data/catalog.json` 后重新构建。`scripts/seed_catalog.py`仅保留本次初始编目的复现记录，日常编辑直接改JSON。更新快照时先查新版本授权，再修改 `scripts/mirror.py` 中的固定提交，并在全新目录保存新归档。

## 归档与声明

Treelaw只负责整理、分类和展示。作品归原发布者，所有条目保留原始链接。收录不代表原发布者与Treelaw合作或背书。

3个上游仓库已按明确许可保留未修改的完整ZIP：

| 原作者 | 分类目录 | 授权 |
|---|---|---|
| pa1nrui1/legal-skills | [China/panrui](China/panrui/README.md) | MIT |
| SenryLee/legal-prompts | [China/senry-prompts](China/senry-prompts/README.md) | MIT |
| anthropics/claude-for-legal | [US/anthropic-legal](US/anthropic-legal/README.md) | Apache-2.0 |

原署名、LICENSE和上游NOTICE（若有）保留。其他条目仅链接原站。可见源代码、免费阅读和可商业再分发分别记录。第三方内容不受本站原创代码许可覆盖。

## 搜索与贡献

HTML预渲染：关闭JavaScript仍有完整目录和详情。提供独立资源页、4个任务页、3个法域页、来源榜、JSON目录、结构化数据、sitemap和llms.txt。英文US页包含英文摘要。发布后精确搜索暂未检索到新站；AI引用效果未测。

公开站点已通过15项浏览器检查；3个公开ZIP下载及SHA-256核对通过。[验收记录](docs/acceptance.json) · [当前状态](docs/STATUS.md)。

[五类用户的搜索意图与实际查询记录](docs/search-intent.md)。提交新条目时请提供：原始地址、作者、身份依据、适用法域、任务、发布时间及许可。通过Issue或PR更正。请勿上传用户案件、密钥或付费内容。

资料核对：2026-11-02（北京时间）。
