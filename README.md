# Treelaw · Global Legal Skills & Plugins

面向律师与企业法务的单项法律技能和插件目录。每个 Skill 对应一个真实的 `SKILL.md`；每个插件对应上游插件清单。

**[打开目录](https://giao-123-sun.github.io/treelaw-legal-skills/)** · [China](China/README.md) · [US](US/README.md) · [Others](Others/README.md)

A task-level directory for legal research, contract review, litigation and compliance. Each entry links to a pinned source file and identifies its publisher, jurisdiction, license and dependencies.

## 收录内容

**287 个单项 Skill + 13 个插件 = 300 项。** China 93项、US 58项、Others 149项。插件与成员分别计数；并非300个独立作者或项目。

| 已展开来源 | Skill | 插件 | 发布方 | 授权 |
|---|---:|---:|---|---|
| [潘睿 legal-skills](https://github.com/pa1nrui1/legal-skills) | 54 | 1 | 专业律师；执业背景为作者自述 | MIT |
| [Anthropic Claude for Legal](https://github.com/anthropics/claude-for-legal) | 107 | 11 | 厂商官方 | Apache-2.0 |
| [l0cka legal-skills](https://github.com/l0cka/legal-skills) | 88 | 1 | 个人；法律执业身份未核实 | MIT |
| [Legal-Skills-Chinese](https://github.com/THUYRan/Legal-Skills-Chinese) | 38 | 0 | 个人；项目未列逐项作者 | CC BY-NC-ND 4.0，仅原站链接 |

协会指南、法律教师资料、Prompt库和其他套件共15项，放在[参考资料](https://giao-123-sun.github.io/treelaw-legal-skills/references.html)，不计入300项。来源榜按协会、专业律师、法律教师、厂商、个人分组。当前没有使用量榜或效果分。

提供关键词搜索，以及任务、法系、涉及资料、发布方、来源、获取方式筛选。Skill和插件可以分开查看，插件详情列出成员。通用商业工作流归入Others，使用时指定法域。

## 核验与数量口径

逐文件读取并解析元数据，记录路径、固定提交和SHA-256；同内容合并，同插件的不同宿主入口合并。38份中英文平行版本只计中文版本。初始化与管理辅助项、1份上游格式异常文件列入[排除记录](data/import-audit.json)。完整插件归档保留其原有辅助文件。

本轮校验来源文件、分类元数据、下载与网页功能，未执行这些技能的业务任务。单项发布时间未披露时留空；仓库创建和更新日期另列。

## 目录结构

```text
China/ US/ Others/       分类索引、获准归档的完整上游ZIP、许可
data/catalog.json        300项公开目录
data/sources.json        4个已展开来源及身份依据
data/reference-library.json  15项补充资料
data/source-base.json    导入用来源基础资料
data/task-labels.txt      中文任务译名
data/source-evidence.json    原始文件路径、版本、哈希
data/import-audit.json    计数、排除项和原因
data/mirrors.json         归档版本和校验值
assets/                  黑白页面、搜索与分页、Treelaw标识
scripts/                 导入、构建、核验
docs/                    当前状态、验收、搜索意图
.github/workflows/       GitHub Pages自动发布
```

静态网页不需要账户、数据库或API。构建使用Python标准库。网页支持关闭JavaScript后阅读全部条目；JS用于搜索、筛选与分页。

## 本地构建

```sh
python scripts/build.py
python scripts/check.py
python -m http.server 3410 --bind 127.0.0.1 --directory site
```

打开 `http://127.0.0.1:3410`。构建生成311个HTML页面，以及JSON-LD、sitemap、llms.txt和公开JSON目录。`site/`为可重建产物，不纳入Git。

更新来源时，先核对新版本许可，再更新固定提交与归档。导入器将覆盖目录数据；分类规则在`scripts/import_skills.py`，中文名在`data/task-labels.txt`，来源基础资料在`data/source-base.json`。导入需要PyYAML：

```sh
python -m pip install -r requirements-dev.txt
python scripts/import_skills.py
python scripts/build.py
python scripts/check.py
```

导入器只读取上游文件。受限来源的研究缓存放在忽略的`.local/`，不发布完整指令。CI直接读取已核对的JSON，无需联网导入。

浏览器检查复用本地Playwright：设置`PLAYWRIGHT_MODULE`为已安装包路径，再运行`node scripts/browser-check.cjs`。设置`TEST_URL`可检查已发布站点。[验收记录](docs/acceptance.json) · [当前状态](docs/STATUS.md)。

## 归档与声明

Treelaw负责整理与展示，作品归原发布者。收录不表示合作或背书。4个完整上游ZIP按原许可保留：

- [潘睿技能](China/panrui/README.md)：MIT。
- [Anthropic插件](US/anthropic-legal/README.md)：Apache-2.0。
- [l0cka技能](Others/l0cka-legal/README.md)：MIT。
- [SenryLee提示库](China/senry-prompts/README.md)：MIT，属于参考资料。

原署名、LICENSE及NOTICE（若有）随包保留。单项技能可能依赖套件中的工具与参考文件，下载入口提供完整套件。其他资源链接原站。本站代码许可不覆盖第三方作品。

[搜索意图与实际查询记录](docs/search-intent.md)。新增条目请提供原始文件地址、作者、身份依据、法域、任务、时间和许可，通过Issue或PR提交。资料核对日：2026-11-02。
