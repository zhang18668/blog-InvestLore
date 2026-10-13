# 云服务器发布指南（Nginx 静态托管）

本博客是纯静态站点，部署到云服务器最简单可靠的方案是 **Nginx 托管 `public/` 目录**。
本文按 Ubuntu/Debian 系统编写（CentOS/RHEL 差异处已标注），全程约 10 分钟。

---

## 0. 你需要准备的 3 样东西

| 项目 | 说明 | 备注 |
| --- | --- | --- |
| 服务器公网 IP | 如 `1.2.3.4` | 控制台可查 |
| SSH 登录方式 | 账号（一般 `root`）+ 密码/密钥 | 用 XShell、FinalShell 或终端 |
| 域名（可选） | 如 `blog.example.com` | 没有域名可直接用 IP 访问，后续补域名也可以 |

> ⚠️ 如果服务器在**中国大陆机房**（阿里云/腾讯云/华为云等），绑定域名对外提供网站服务需要完成 **ICP 备案**，否则 80/443 端口会被运营商拦截。只用 IP 直接访问一般不强制，但建议按平台规则操作。

---

## 1. 服务器端：初始化（只需一次）

SSH 登录服务器后执行：

```bash
# Ubuntu / Debian
sudo apt update && sudo apt install -y nginx unzip

# CentOS / RHEL 7+（二选一）
# sudo yum install -y nginx unzip
```

创建站点目录并确认 Nginx 启动：

```bash
sudo mkdir -p /var/www/stock-blog
sudo systemctl enable --now nginx
curl -I http://127.0.0.1    # 返回 HTTP/1.1 200 即正常
```

---

## 2. 本地：打包并上传站点

### 2.1 打包（已为你打好，见 `dist/stock-blog-site.zip`）

本地在博客目录执行：

```bash
cd stock-blog
hexo clean && hexo generate   # 重新生成最新站点
# 打包 public 目录内容
cd public && zip -r ../dist/stock-blog-site.zip . -x ".*" && cd ..
```

### 2.2 上传到服务器（三选一）

```bash
# 方式 A：scp（本地终端）
scp dist/stock-blog-site.zip root@你的IP:/tmp/

# 方式 B：rsync（更推荐，增量同步，后续更新也用这个）
rsync -av --delete public/ root@你的IP:/var/www/stock-blog/

# 方式 C：图形工具（FileZilla / FinalShell）
# 把 stock-blog-site.zip 拖到服务器 /tmp/ 目录
```

### 2.3 服务器端解压部署

```bash
sudo unzip -o /tmp/stock-blog-site.zip -d /var/www/stock-blog/
sudo chown -R www-data:www-data /var/www/stock-blog   # Ubuntu 的 nginx 用户
# CentOS 用: sudo chown -R nginx:nginx /var/www/stock-blog
```

---

## 3. 配置 Nginx

把仓库里的 `deploy/nginx-blog.conf` 上传到服务器后执行：

```bash
# Ubuntu/Debian
sudo cp nginx-blog.conf /etc/nginx/conf.d/stock-blog.conf

# CentOS/RHEL（先确认 sites-enabled 目录存在）
# sudo cp nginx-blog.conf /etc/nginx/conf.d/stock-blog.conf
```

**修改配置里的域名/IP**（用 vi/nano 编辑）：

```bash
sudo nano /etc/nginx/conf.d/stock-blog.conf
# 把 server_name your-domain.com; 改成你的域名或公网 IP
```

验证并生效：

```bash
sudo nginx -t                    # 出现 syntax is ok 即通过
sudo systemctl reload nginx
```

**验证部署结果**：浏览器打开 `http://你的IP` 或 `http://你的域名`，应看到博客首页。

---

## 4. 防火墙与安全组（重要，容易漏）

- **服务器内防火墙**（如有开启）：
  ```bash
  sudo ufw allow 'Nginx Full'    # Ubuntu
  # CentOS: sudo firewall-cmd --permanent --add-service=http --add-service=https && sudo firewall-cmd --reload
  ```
- **云厂商安全组**：在控制台「安全组/防火墙」规则中放行 **80（HTTP）** 和 **443（HTTPS）** 入方向端口。

---

## 5. 域名解析（可选）

在 DNS 服务商（阿里云/腾讯云/Cloudflare 等）添加 **A 记录**：

| 主机记录 | 类型 | 记录值 |
| --- | --- | --- |
| `blog`（或 `@`） | A | 你的服务器公网 IP |

生效时间通常几分钟到几小时。

---

## 6. HTTPS（可选，强烈建议）

```bash
sudo apt install -y certbot python3-certbot-nginx   # Ubuntu
# CentOS: sudo yum install -y certbot python3-certbot-nginx

sudo certbot --nginx -d 你的域名
```

按提示操作即可，certbot 会自动改写 Nginx 配置并设置证书自动续期（有效期 90 天，无需手动管）。

---

## 7. 以后每次更新内容（3 个命令）

本地：

```bash
cd stock-blog
hexo clean && hexo generate
rsync -av --delete public/ root@你的IP:/var/www/stock-blog/
```

> `--delete` 会删除服务器上已不存在的旧文件，保证与本地一致。若不想删旧文件，去掉 `--delete` 即可。

---

## 8. 常见问题排查

| 现象 | 原因与处理 |
| --- | --- |
| 打开显示 Nginx 默认欢迎页 | 没加载到你的站点配置，检查 `conf.d` 下配置文件名和 `nginx -t` |
| 404 / 403 | 站点目录权限不对，执行 `sudo chown -R www-data:www-data /var/www/stock-blog` |
| 外网打不开、本地 curl 正常 | 安全组/防火墙没放行 80 端口（见第 4 步） |
| 域名打不开 | DNS 未生效（`ping 域名` 看是否指向你的 IP）、或大陆机房未备案 |
| 样式错乱（CSS 加载不出） | 清空浏览器缓存，或确认 `root` 路径正确、`public/` 内文件在 `/var/www/stock-blog/` 根下 |

---

## 9. 备份建议

服务器上执行（可选，建议每周一次）：

```bash
tar -czf /var/backups/stock-blog-$(date +%F).tar.gz -C /var/www stock-blog
```

---

*本指南由「股市操练笔记」部署包附带。部署过程中任何一步报错，把报错信息贴回来，我可以帮你逐行排查。*
