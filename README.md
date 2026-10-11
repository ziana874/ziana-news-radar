# Ziana News Radar · 四频道中文新闻雷达

无本地服务器的个人新闻聚合网站：世界与中国、AI 与科技前沿、全球移民政策、投资与 Web3。

- **采集**：GitHub Actions 每 6 小时读取 20 个 RSS/Atom/Google News 信息源，按发布时间、关键词和来源类型打分、去重，并在 GitHub Pages 展示。
- **中文整理（可选）**：配置 Gemini API Key 后，仅根据 RSS 标题和摘要生成中文简述及重要性说明。**并不阅读全文，也不能替代事实核验。**
- **每日手机推送（可选）**：每天北京时间约 08:17 通过 ntfy 推送频道重点信息（定时任务可能延迟）。
- **阅读**：手机优化、深色模式、搜索、重点/时间排序、设备本地收藏。
- **安全**：所有代码和网站内容位于公开仓库。密钥必须使用 GitHub Actions Secrets，绝不能放进代码或公开数据。

## 仓库及网站

- 仓库：https://github.com/ziana874/ziana-news-radar
- 网站（GitHub Pages 发布成功后）：https://ziana874.github.io/ziana-news-radar/
- 工作流：https://github.com/ziana874/ziana-news-radar/actions/workflows/news.yml

## 第一次启用（一次性）

1. **Settings → Pages → Build and deployment → Source** 选 **GitHub Actions**，保存。
2. 进入上方工作流链接，点击 **Run workflow → Run workflow**；等待采集与 Pages 发布成功。
3. 如果 Pages 页面出现 404，查看 Actions 日志。出现 “Get Pages site failed / 404” 表示 Pages 还未配置成功。
4. GitHub Actions 定时运行并非精确时钟，GitHub 可能暂停长期无活动的公开仓库的计划工作流。

## 开启中文 AI 摘要（可选）

1. 从 https://aistudio.google.com/apikey 申请 Gemini API Key；用前确认费用与地区可用性。
2. Settings → Secrets and variables → Actions → New repository secret；名称填 GEMINI_API_KEY，值填自己的密钥。**不要将密钥发到聊天里，也不要提交到 GitHub 代码里。**
3. 默认模型 gemini-2.5-flash-lite；若不可用，可以通过 Actions Variables 的 GEMINI_MODEL 修改。
4. 重新运行工作流；无 API Key 时仍正常聚合新闻，但英文来源不会伪装成中文摘要。

## 开启 iPhone 每日通知（可选）

1. 安装 [ntfy](https://ntfy.sh/)，在 iPhone 上订阅服务 ntfy.sh 的一个高强度随机主题（建议使用随机 24 位以上字符）。
2. 在 GitHub Actions Secrets 新增 NTFY_TOPIC，填入同一个主题字符串。
3. 北京/台北时间每天约 08:17 的定时采集完成后会推送；手动运行仅测试网页更新，默认不会发通知。
4. ntfy 公共主题的内容可能被知道主题的人阅读，只发送公开新闻标题，不得用于私密数据。

## 修改来源

根目录 feeds.json 定义四组信息源：world、tech、immigration、investing。kind=official 仅用于官方直连的 RSS；Google News 查询只是**索引**，不会被错误标记为官方公告。移民政策需点击原文核实公告日期、生效日期及适用条件。

## 局限与排查

- RSS 返回的信息可能只含标题/短摘要；没有独立验证全文内容。
- Google 新闻索引可能漏掉、延迟或误分类。部分 RSS 可能无法从 GitHub 网络连接。
- 来源质量、去重与重要性评分目前是规则法，不保证每日新闻均衡或全面。
- docs/data.json 在未运行第一次采集时是空数据。Actions 首次运行后才会有实际新闻。
- 若全部新闻源失败，程序会报错并保留上一版网页数据，而不会发布伪造新闻。
- ntfy 与 Gemini 两项完全可选，未设置时仍可免费使用基本版。
- 每篇文章及其原始媒体内容的版权属于原作者；只显示短 RSS 元数据和原始链接。
