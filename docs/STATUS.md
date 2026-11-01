# 当前状态

更新：2026-11-02。项目：Treelaw Legal Skills Directory。独立公开静态目录，不修改Treelaw桌面端运行代码。

## 本版边界

24项资源，18个独立资源入口（6项同源子技能）。China 8、US 14、Others 2。没有建立用户账户、执行器、使用量采集或质量评分。

页面支持国家目录、诉讼／非诉／涉外／合规、发布方、法系、涉及资料、资源形式、获取方式及关键词筛选。来源榜按协会、专业律师、法律教师、厂商、个人分组，并显示背景依据。自述与独立核对分开。

## 已验证

- 构建34个HTML页面，关闭JavaScript仍有完整资源正文。
- 自动校验所有站内链接、唯一H1／标题／canonical、JSON-LD。
- Playwright检查搜索、组合筛选、空状态、清除筛选、URL恢复、手机布局、英文页、详情与无脚本阅读；15项通过。
- 3个原始ZIP的SHA-256、许可证、压缩包完整性和6个Anthropic子技能路径通过。
- 修正了清除按钮ID遮蔽表单reset方法的问题，复测通过。
- GitHub Pages发布成功。公开网址再次通过相同15项浏览器检查。3个公开ZIP下载均为HTTP 200，内容哈希与本地一致，详见`acceptance.json`。

## 文件与后续维护

条目只维护 `data/catalog.json`，构建 `scripts/build.py`。`data/mirrors.json`记录固定版本，按原始许可保存3个完整上游ZIP，约4.1MB。第三方内容只归档，未运行。

`docs/search-intent.md`记录五类用户、7次真实查询、候选关键词和新增来源。已生成静态任务页、详情页、sitemap、JSON-LD、llms.txt。发布后用仓库及站点完整URL做两次精确搜索，均未返回结果。当前记录为尚未检索到收录；AI回答引用未测。

已发布仓库：`https://github.com/giao-123-sun/treelaw-legal-skills`。公开页面：`https://giao-123-sun.github.io/treelaw-legal-skills/`。GitHub Pages从main分支工作流构建。运行过程文件与截图置于忽略的`.local/`。

待后续任务：输出效果评测；新增地区的具名专业作者；有实际用户数据后再建设使用榜。当前不要用GitHub stars或作者身份推算效果分。
