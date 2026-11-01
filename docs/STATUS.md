# 当前状态

更新：2026-11-02。Treelaw Legal Skills Directory为独立公开静态目录。

## 当前交付

300项：287个Skill、13个插件；China 93、US 58、Others 149。4个来源按文件展开，15项指南、Prompt库与其他套件单列。插件与成员分别计数。

页面支持搜索、业务分类、法系、资料类型、发布方、来源和获取方式筛选；每页24项，筛选与页码写入URL。插件详情直接链接成员。原始文件、固定版本、身份依据、许可和依赖均可查看。

## 验证

- 311个HTML页面：站内链接、H1／标题／canonical、JSON-LD检查通过。
- 300条路径和哈希记录一致，插件成员关系和来源计数通过。
- 4个完整归档的许可证、ZIP完整性及SHA-256通过；其中262个目录条目与归档内原始文件逐项比对通过。
- 本地20项浏览器检查通过：搜索、筛选、分页、URL恢复、手机页面、插件成员、英文页面、无脚本阅读等。
- GitHub Pages发布成功，公开站点20项浏览器检查通过；4个ZIP公开下载均为HTTP 200，哈希与本地一致。详见`acceptance.json`。

本轮未执行287个Skill的业务任务；没有使用量和效果评分。

## 维护入口

导入：`scripts/import_skills.py`。基础资料：`data/source-base.json`。译名：`data/task-labels.txt`。计数与排除原因：`data/import-audit.json`。归档：`data/mirrors.json`，4包约6.2MB。`data/catalog.json`为构建输入；再次导入会覆盖它。

构建及校验：`scripts/build.py`、`scripts/check.py`、`scripts/browser-check.cjs`。`site/`为生成目录，`.local/`为研究缓存和截图，两者忽略。公开站点由main分支Pages工作流发布。

本次决策：单项Skill与真实插件成为主目录；指南和Prompt库分开呈现；翻译副本不重复计数；不按英文语言推定美国法域；带依赖的技能提供完整上游包。

后续独立工作：逐任务效果评测；扩充具名专业作者；有实际用户数据后建立使用榜。搜索意图和已做查询见`search-intent.md`。
