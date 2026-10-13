# blog-InvestLore

股市操练笔记 · 个人博客源码仓库

把《股市操练大全》系列等股票书籍，整理成**可发布的个人学习笔记博客**。站点基于开源博客框架 **Hexo** + **Butterfly** 主题构建，并配套一组 **Python 脚本**，用于批量生成 K 线、缠论（缠中说禅）、量价分析等学习配图。

**线上地址：** https://zhangzhh13.xyz/blog/

---

## 仓库结构

| 路径 | 说明 |
| --- | --- |
| `stock-blog/` | 博客主工程：Hexo 源码、Butterfly 主题、190+ 篇文章、22 个图表生成/修复脚本 |
| `chan-build/` | 缠论书籍章节网页与配图的构建、裁剪、校验脚本（33 个）及规范文档 |
| `gen_v6_charts.py` | 顶层（根目录）图表生成脚本 |
| `迷你pdf阅读器/` | 本地 PDF 阅读小工具（可执行程序，未纳入版本库） |
| `README.md` / `.gitignore` | 本仓库说明与提交规则 |

---

## 内容概览

博客内容整理自《股市操练大全》系列（第一至第七册、习题集）以及《聪明的投资者》《股票大作手回忆录》《威科夫量价分析图解》等书籍，均为**原创学习笔记**，共 **190+ 篇**文章，分五大篇章与五个文章系列：

| 篇章（一级分类） | 子类（二级分类） | 对应原书 |
| --- | --- | --- |
| 第一篇 · 入门导航 | 导读 / 学习方法 | 习题集 |
| 第二篇 · 基础：看图识形 | K线 / 技术图形 | 第一册 |
| 第三篇 · 进阶：技术指标 | 技术指标 | 第二册 |
| 第四篇 · 实战：选股与运用 | 选股方法 / 实战运用 | 第三、五、六、七册 |
| 第五篇 · 纪律：规矩与底线 | 操作纪律 / 识底抄底 | 第四册 |

另有 **K 线形态识别专题 11 篇**（`/blog/kxian-zt/`），从 K 线基础、单根到组合与连续形态，以综合练习与测验收尾；每篇带 AI 总结块、上下篇跳转与风险提示。所有文章文末均标注风险提示。

---

## 本地运行

环境要求：**Node.js ≥ 16**

```bash
cd stock-blog

npm install          # 安装依赖（已装可跳过）

hexo server          # 本地预览，默认 http://localhost:4000

hexo generate        # 生成静态站点到 public/

hexo clean && hexo generate   # 清理后重新生成
```

---

## 图表生成脚本

`stock-blog/` 根目录及 `chan-build/` 内含一批 Python 脚本，用于批量生成与修复博客配图：

- **K 线/量价类**：`draw_kline*.py`、`draw_v2*.py`、`gen_kx_*.py`、`gen_vol*.py`、`gen_mls_charts.py` 等
- **缠论构建**：`chan-build/` 下的 `work-*` 构建、`crop*.py` 裁剪、`verify*.py` / `check-*.py` 校验脚本
- **图表批量生成**：`gen_v3 / v5o / v7o / v8 / wbo / v6_charts.py` 等

依赖：Python 3 + matplotlib 等常用绘图库（按各脚本顶部 import 安装即可）。

---

## 部署

**当前线上方式：** 通过 `publish-server` 技能以 **Docker 容器 + Nginx 反向代理**发布，站点根路径为 `/blog/`（见 `stock-blog/_config.yml` 的 `root: /blog/`）。

```bash
cd stock-blog
hexo clean && hexo generate
python "<用户技能目录>\publish-server\scripts\publish_server.py" deploy \
  --project "E:\生活\股票操练大全全套\stock-blog" --app stock-blog \
  --path /blog/ --container-port 80 --dockerfile docker-deploy/Dockerfile --strip-prefix
```

常用命令：`status` / `logs --app stock-blog` / `restart --app stock-blog` / `rollback --app stock-blog`。

**备选方案：** `stock-blog/deploy/` 已备好 Nginx 部署包；也可用 **GitHub Pages**（将 `public/` 推到 `用户名.github.io/blog`）或 **Netlify / Vercel**（构建命令 `npm run build`，输出目录 `public/`）。

> 注意：站点根路径为 `/blog/`，在其他域名根路径托管时请先将 `root` 改回 `/` 再重新生成。

---

## 版本库提交说明

为符合 GitHub 仓库体量与单文件限制，本仓库**仅提交代码与文本内容**，未纳入以下大体积文件（已由 `.gitignore` 排除）：

- `stock-blog/source/images/` —— K 线 / 缠论 / 量价分析生成图（约 630MB）
- `public/`、`dist/`、`docker-deploy/public/` —— 构建产物
- `node_modules/` —— 依赖（`npm install` 重建）
- 原书 PDF、压缩包、可执行程序等资料
- `chan-build/work-*` 等构建中间产物

如需还原完整站点，请在 `stock-blog/` 下运行 `hexo generate` 重新生成全部页面与图片。

---

## 版权与免责声明

- 本站内容为**学习笔记性质**，仅供个人学习参考，**不构成投资建议**。
- 如需引用原书图表或大段原文，请购买正版书籍并注明出处。
- **股市有风险，入市需谨慎。**
