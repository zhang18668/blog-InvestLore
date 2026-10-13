# 股市操练笔记 · Docker 镜像
# 注意：构建上下文 = stock-blog 项目根目录（发布技能以项目根作为 build context）
# 基础镜像用服务器本地已有的 nginx，避免触发坏镜像源（阿里云 mirror 403）
# 原为 nginx:alpine，因本地未缓存且镜像源可能 403，改用本地已有镜像
FROM docker.m.daocloud.io/library/nginx:stable

# 站点 Nginx 配置（相对项目根的路径）
COPY docker-deploy/nginx.conf /etc/nginx/conf.d/default.conf

# 静态站点内容
COPY public /usr/share/nginx/html

EXPOSE 80

# 健康检查：每 30 秒访问首页，失败则标记容器不健康
# 注：nginx:stable 镜像不含 wget，使用容器内已有的 curl
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s \
  CMD curl -fsS http://127.0.0.1/ >/dev/null 2>&1 || exit 1
