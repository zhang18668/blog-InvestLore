# 股市操练笔记（个人博客）

把《股市书籍》系列整理成可发布的个人博客内容，用开源博客框架 **Hexo** + **Butterfly** 主题构建。

## 内容概览

**16 篇原创学习笔记**（五大篇章 + 五个文章系列）+ **K线形态识别专题 11 篇**（入口：`/blog/kxian-zt/`）：

| 篇章（一级分类） | 子类（二级分类） | 篇数 | 对应原书 |
| --- | --- | --- | --- |
| 第一篇 · 入门导航 | 导读 / 学习方法 | 2 | 习题集 |
| 第二篇 · 基础：看图识形 | K线 / 技术图形 | 5 | 第一册 |
| 第三篇 · 进阶：技术指标 | 技术指标 | 4 | 第二册 |
| 第四篇 · 实战：选股与运用 | 选股方法 / 实战运用 | 3 | 第三、五、六、七册 |
| 第五篇 · 纪律：规矩与底线 | 操作纪律 / 识底抄底 | 2 | 第四册 |

文章系列：系列一·入门导航 / 系列二·基础：看图识形 / 系列三·进阶：技术指标 / 系列四·实战：选股与运用 / 系列五·纪律：规矩与底线（文章页侧边栏可见系列内前后篇导航）。

**专题（K线形态识别）**：11 篇（`zt-kx-01`~`zt-kx-11`），从 K 线基础、单根 K 线到双/三 K 线组合与连续形态，最后以综合练习与测验收尾；每篇开头带 AI 总结块，文末带上下篇跳转与风险提示。

所有文章均为**原创学习笔记**；文末均标注风险提示。

## 本地运行

环境要求：Node.js ≥ 16。



```
cd stock-blog

npm install          # 安装依赖（已装可跳过）

hexo server          # 本地预览，默认 http://localhost:4000

hexo generate        # 生成静态站点到 public/

hexo clean && hexo generate   # 重新生成
```

## 部署上线

**当前线上地址：https://zhangzhh13.xyz/blog/**（2026-09-21 通过 `publish-server` 技能以 Docker 容器 + Nginx 反向代理发布）

站点构建根路径为 `/blog/`（`_config.yml` 中 `root: /blog/`），所有资源链接均带 `/blog/` 前缀；如要在其他域名根路径托管，请先把 `root` 改回 `/` 再重新生成。

### 后续更新内容（发布新版本）

```bash
cd stock-blog
hexo clean && hexo generate   # 重新生成 public/
# 用 publish-server 技能重新发布（保留上一版本，失败自动回滚 Nginx）
python "<用户技能目录>\publish-server\scripts\publish_server.py" deploy --project "E:\生活\股票操练大全全套\stock-blog" --app stock-blog --path /blog/ --container-port 80 --dockerfile docker-deploy/Dockerfile --strip-prefix
```

常用命令：`status`（状态）、`logs --app stock-blog`（日志）、`restart --app stock-blog`（重启）、`rollback --app stock-blog`（回滚）。

### 其他部署方案（备选）

1. **自有云服务器（Nginx）**：`deploy/` 目录已备好部署包——`nginx-blog.conf` 站点配置、`deploy-to-server.md` 逐步指南、`dist/stock-blog-site.zip` 站点压缩包。注意站点根路径为 `/blog/`，需部署在 `/blog/` 子路径下（或先改 `root` 再生成）。
2. **GitHub Pages**：把 `public/` 内容推到 `用户名.github.io/blog` 仓库，或安装 `hexo-deployer-git` 后配置 `deploy` 字段。
3. **Netlify / Vercel**：连接本仓库，构建命令 `npm run build`，输出目录 `public/`。

## 自定义



* **站点信息**：改 `stock-blog/_config.yml`（标题、副标题、作者、关键词）。

* **主题外观**：改 `stock-blog/themes/butterfly/_config.yml`（导航、头像、配色、社交链接等）。

* **写新文章**：在 `source/_posts/` 下新建 Markdown 文件，参考现有文章的 front-matter 格式（`title/date/tags/categories/description`）。

## 版权与免责声明



* 本站内容为学习笔记性质，仅供个人学习参考，不构成投资建议。

* 内容为个人学习笔记；如需引用原书图表或大段原文，请购买正版书籍并注明出处。

* 股市有风险，入市需谨慎。