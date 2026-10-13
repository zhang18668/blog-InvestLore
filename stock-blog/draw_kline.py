# -*- coding: utf-8 -*-
"""批量生成同花顺风格K线形态重绘图"""
import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'FangSong', 'SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

OUT = r"E:\生活\股票操练大全全套\stock-blog\source\images\kxian"
os.makedirs(OUT, exist_ok=True)

UP = '#FF4444'
DN = '#00AA00'

def draw_kline(ax, x, o, c, h, l, width=0.35):
    color = UP if c >= o else DN
    ax.plot([x, x], [l, h], color=color, linewidth=1.5)
    bottom = min(o, c)
    height = max(abs(c - o), 0.05)
    rect = patches.Rectangle((x - width/2, bottom), width, height,
                            facecolor=color, edgecolor=color, linewidth=1)
    ax.add_patch(rect)

def setup_ax(ax, xlim, ylim):
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.axis('off')
    ax.set_aspect('auto')

def save(fig, name):
    path = os.path.join(OUT, name)
    fig.savefig(path, dpi=150, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close(fig)
    print(f"saved {name}")

# ============ 1. 大阳线与大阴线 ============
fig, axes = plt.subplots(1, 2, figsize=(6, 3.5))
# 大阳线
ax = axes[0]
draw_kline(ax, 1, 10, 18, 18.5, 9.5)
draw_kline(ax, 0.3, 9, 9.2, 9.5, 8.8)
setup_ax(ax, (0, 2), (8, 20))
ax.set_title('大阳线', fontsize=11)
# 大阴线
ax = axes[1]
draw_kline(ax, 1, 18, 10, 18.5, 9.5)
draw_kline(ax, 0.3, 19, 18.8, 19.2, 18.5)
setup_ax(ax, (0, 2), (8, 20))
ax.set_title('大阴线', fontsize=11)
fig.suptitle('', fontsize=10)
save(fig, 'v1o-01.png')

# ============ 2. 锤头线与吊颈线 ============
fig, axes = plt.subplots(1, 2, figsize=(6, 3.5))
# 锤头线（下跌末端，阳线锤头）
ax = axes[0]
for i,(o,c,h,l) in enumerate([(12,13,13.5,8.5),(11,11.5,12,9),(10.5,11,11.5,9.5)]):
    draw_kline(ax, i+1, o, c, h, l)
draw_kline(ax, 4, 9, 9.8, 10.2, 7.5)  # 锤头
setup_ax(ax, (0, 5), (7, 14))
ax.set_title('锤头线（见底）', fontsize=11)
# 吊颈线（上涨末端，阴线吊颈）
ax = axes[1]
for i,(o,c,h,l) in enumerate([(8,9,9.5,7.5),(8.5,9.5,10,8),(9,10.5,11,8.5)]):
    draw_kline(ax, i+1, o, c, h, l)
draw_kline(ax, 4, 10.5, 11.2, 11.5, 9)  # 吊颈
setup_ax(ax, (0, 5), (7, 12))
ax.set_title('吊颈线（见顶）', fontsize=11)
save(fig, 'v1o-02.png')

# ============ 3. 倒锤头线与射击之星 ============
fig, axes = plt.subplots(1, 2, figsize=(6, 3.5))
# 倒锤头（下跌末端）
ax = axes[0]
for i,(o,c,h,l) in enumerate([(12,11,12.5,9),(11,10,11.5,8.5),(10,9.5,10.5,8)]):
    draw_kline(ax, i+1, o, c, h, l)
draw_kline(ax, 4, 9, 9.5, 12, 8.8)  # 倒锤头
setup_ax(ax, (0, 5), (8, 13))
ax.set_title('倒锤头线（见底）', fontsize=11)
# 射击之星（上涨末端）
ax = axes[1]
for i,(o,c,h,l) in enumerate([(8,9,9.5,7.5),(8.5,9.5,10,8),(9,10.5,11,8.5)]):
    draw_kline(ax, i+1, o, c, h, l)
draw_kline(ax, 4, 10.5, 10, 13.5, 9.8)  # 射击之星
setup_ax(ax, (0, 5), (7.5, 14))
ax.set_title('射击之星（见顶）', fontsize=11)
save(fig, 'v1o-03.png')

# ============ 4. T字线、倒T字线与一字线 ============
fig, axes = plt.subplots(1, 3, figsize=(7, 3))
ax = axes[0]
draw_kline(ax, 1, 10, 10, 10.2, 8)
setup_ax(ax, (0, 2), (7, 11))
ax.set_title('T字线', fontsize=11)
ax = axes[1]
draw_kline(ax, 1, 10, 10, 12, 9.8)
setup_ax(ax, (0, 2), (9, 13))
ax.set_title('倒T字线', fontsize=11)
ax = axes[2]
draw_kline(ax, 1, 10, 10, 10, 10)
setup_ax(ax, (0, 2), (9.5, 10.5))
ax.set_title('一字线', fontsize=11)
save(fig, 'v1o-04.png')

# ============ 5. 长十字线与螺旋桨 ============
fig, axes = plt.subplots(1, 2, figsize=(6, 3.5))
ax = axes[0]
draw_kline(ax, 1, 10, 10, 13, 7)
setup_ax(ax, (0, 2), (6, 14))
ax.set_title('长十字线', fontsize=11)
ax = axes[1]
draw_kline(ax, 1, 9.8, 10.2, 13, 7)
setup_ax(ax, (0, 2), (6, 14))
ax.set_title('螺旋桨', fontsize=11)
save(fig, 'v1o-05.png')

# ============ 6. 曙光初现与乌云盖顶 ============
fig, axes = plt.subplots(1, 2, figsize=(6, 3.5))
# 曙光初现：大阴线后大阳线深入阴线实体一半以上
ax = axes[0]
draw_kline(ax, 1, 12, 8, 12.5, 7.5)   # 大阴线
draw_kline(ax, 2, 7.5, 10.5, 11, 7)    # 大阳线深入
setup_ax(ax, (0, 3), (6, 13))
ax.set_title('曙光初现（见底）', fontsize=11)
# 乌云盖顶：大阳线后大阴线深入阳线实体一半以下
ax = axes[1]
draw_kline(ax, 1, 8, 12, 12.5, 7.5)    # 大阳线
draw_kline(ax, 2, 12.5, 9, 13, 8.5)    # 大阴线深入
setup_ax(ax, (0, 3), (7, 13.5))
ax.set_title('乌云盖顶（见顶）', fontsize=11)
save(fig, 'v1o-06.png')

# ============ 7. 旭日东升与倾盆大雨 ============
fig, axes = plt.subplots(1, 2, figsize=(6, 3.5))
ax = axes[0]
draw_kline(ax, 1, 12, 8, 12.5, 7.5)    # 大阴线
draw_kline(ax, 2, 9, 13, 13.5, 8.5)    # 高开大阳线收盘高于阴线开盘
setup_ax(ax, (0, 3), (7, 14))
ax.set_title('旭日东升（见底）', fontsize=11)
ax = axes[1]
draw_kline(ax, 1, 8, 12, 12.5, 7.5)    # 大阳线
draw_kline(ax, 2, 11, 7.5, 11.5, 7)    # 低开大阴线收盘低于阳线开盘
setup_ax(ax, (0, 3), (6, 13))
ax.set_title('倾盆大雨（见顶）', fontsize=11)
save(fig, 'v1o-07.png')

# ============ 8. 早晨之星与黄昏之星 ============
fig, axes = plt.subplots(1, 2, figsize=(6, 3.5))
ax = axes[0]
draw_kline(ax, 1, 12, 8, 12.5, 7.5)    # 大阴线
draw_kline(ax, 2, 7.5, 7.2, 8, 6.8)    # 小星线
draw_kline(ax, 3, 7.5, 11, 11.5, 7)    # 大阳线
setup_ax(ax, (0, 4), (6, 13))
ax.set_title('早晨之星（见底）', fontsize=11)
ax = axes[1]
draw_kline(ax, 1, 8, 12, 12.5, 7.5)    # 大阳线
draw_kline(ax, 2, 12.5, 12.8, 13.5, 12) # 小星线
draw_kline(ax, 3, 12.5, 9, 13, 8.5)    # 大阴线
setup_ax(ax, (0, 4), (7, 14))
ax.set_title('黄昏之星（见顶）', fontsize=11)
save(fig, 'v1o-08.png')

# ============ 9. 好友反攻与淡友反攻 ============
fig, axes = plt.subplots(1, 2, figsize=(6, 3.5))
ax = axes[0]
draw_kline(ax, 1, 12, 8, 12.5, 7.5)    # 大阴线
draw_kline(ax, 2, 7, 8, 8.5, 6.5)      # 跳空低开收阳线，收盘与前阴线收盘相近
setup_ax(ax, (0, 3), (6, 13))
ax.set_title('好友反攻（见底）', fontsize=11)
ax = axes[1]
draw_kline(ax, 1, 8, 12, 12.5, 7.5)    # 大阳线
draw_kline(ax, 2, 13, 12, 13.5, 11.5)  # 跳空高开收阴线，收盘与前阳线收盘相近
setup_ax(ax, (0, 3), (7, 14))
ax.set_title('淡友反攻（见顶）', fontsize=11)
save(fig, 'v1o-09.png')

# ============ 10. 平底与平顶 ============
fig, axes = plt.subplots(1, 2, figsize=(6, 3.5))
ax = axes[0]
draw_kline(ax, 1, 12, 8, 12.5, 7)
draw_kline(ax, 2, 9, 10, 10.5, 7)
draw_kline(ax, 3, 9.5, 11, 11.5, 7.2)
setup_ax(ax, (0, 4), (6, 13))
ax.set_title('平底（镊子底）', fontsize=11)
ax = axes[1]
draw_kline(ax, 1, 8, 12, 13, 7.5)
draw_kline(ax, 2, 11, 10, 13, 9.5)
draw_kline(ax, 3, 10.5, 9, 13, 8.5)
setup_ax(ax, (0, 4), (7, 14))
ax.set_title('平顶（镊子顶）', fontsize=11)
save(fig, 'v1o-10.png')

# ============ 11. 塔形底与塔形顶 ============
fig, axes = plt.subplots(1, 2, figsize=(6, 3.5))
ax = axes[0]
draw_kline(ax, 1, 13, 8, 13.5, 7.5)
for i in range(2, 6):
    draw_kline(ax, i, 9+0.2*(i-2), 8.8+0.15*(i-2), 9.5+0.2*(i-2), 8.2+0.1*(i-2))
draw_kline(ax, 6, 9, 12, 12.5, 8.8)
setup_ax(ax, (0, 7), (7, 14))
ax.set_title('塔形底', fontsize=11)
ax = axes[1]
draw_kline(ax, 1, 8, 13, 13.5, 7.5)
for i in range(2, 6):
    draw_kline(ax, i, 11-0.2*(i-2), 10.8-0.15*(i-2), 11.5-0.2*(i-2), 10.2-0.1*(i-2))
draw_kline(ax, 6, 11, 8, 11.5, 7.5)
setup_ax(ax, (0, 7), (7, 14))
ax.set_title('塔形顶', fontsize=11)
save(fig, 'v1o-11.png')

# ============ 12. 红三兵与黑三兵 ============
fig, axes = plt.subplots(1, 2, figsize=(6, 3.5))
ax = axes[0]
draw_kline(ax, 1, 8, 9, 9.5, 7.8)
draw_kline(ax, 2, 9, 10.2, 10.7, 8.8)
draw_kline(ax, 3, 10.2, 11.5, 12, 10)
setup_ax(ax, (0, 4), (7, 13))
ax.set_title('红三兵', fontsize=11)
ax = axes[1]
draw_kline(ax, 1, 12, 10.5, 12.5, 10)
draw_kline(ax, 2, 10.5, 9, 11, 8.5)
draw_kline(ax, 3, 9, 7.5, 9.5, 7)
setup_ax(ax, (0, 4), (6, 13))
ax.set_title('黑三兵', fontsize=11)
save(fig, 'v1o-12.png')

# ============ 13. 冉冉上升形与绵绵阴跌形 ============
fig, axes = plt.subplots(1, 2, figsize=(7, 3.5))
ax = axes[0]
import random
random.seed(42)
base = 8
for i in range(8):
    o = base + i*0.25 + random.uniform(-0.1,0.1)
    c = o + random.choice([0.15, -0.1])
    h = max(o,c)+0.15
    l = min(o,c)-0.15
    draw_kline(ax, i+1, o, c, h, l)
setup_ax(ax, (0, 9), (7, 11))
ax.set_title('冉冉上升形', fontsize=11)
ax = axes[1]
base = 12
for i in range(8):
    o = base - i*0.25 + random.uniform(-0.1,0.1)
    c = o + random.choice([-0.15, 0.1])
    h = max(o,c)+0.15
    l = min(o,c)-0.15
    draw_kline(ax, i+1, o, c, h, l)
setup_ax(ax, (0, 9), (8, 13))
ax.set_title('绵绵阴跌形', fontsize=11)
save(fig, 'v1o-13.png')

# ============ 14. 弧形线 ============
fig, ax = plt.subplots(figsize=(5, 3.5))
import numpy as np
x = np.arange(8)
# 弧形：先缓慢上升，底部逐渐抬高，呈抛物线
prices = [8, 8.2, 8.5, 9, 9.8, 10.8, 12, 13.5]
for i, p in enumerate(prices):
    o = p - 0.15
    c = p + 0.2 if i % 2 == 0 else p - 0.1
    h = max(o,c) + 0.3
    l = min(o,c) - 0.3
    draw_kline(ax, i+1, o, c, h, l)
# 弧线
xs = np.linspace(0.5, 8.5, 100)
ys = 7.5 + 0.07*(xs-0.5)**2
ax.plot(xs, ys, 'k--', linewidth=1.5)
setup_ax(ax, (0, 9), (6, 15))
ax.set_title('弧形线（圆弧底）', fontsize=11)
save(fig, 'v1o-14.png')

# ============ 15. 下探上涨形与高开出逃形 ============
fig, axes = plt.subplots(1, 2, figsize=(6, 3.5))
ax = axes[0]
draw_kline(ax, 1, 8, 9, 9.5, 7.5)
draw_kline(ax, 2, 9, 9.5, 10, 8.5)
draw_kline(ax, 3, 8.5, 9, 9.5, 8)
draw_kline(ax, 4, 7.5, 11, 11.5, 7)  # 低开高走大阳线
setup_ax(ax, (0, 5), (6.5, 12))
ax.set_title('下探上涨形', fontsize=11)
ax = axes[1]
draw_kline(ax, 1, 12, 11, 12.5, 10.5)
draw_kline(ax, 2, 11, 10, 11.5, 9.5)
draw_kline(ax, 3, 10, 9, 10.5, 8.5)
draw_kline(ax, 4, 11, 7, 11.5, 6.5)  # 高开大阴线
setup_ax(ax, (0, 5), (6, 13))
ax.set_title('高开出逃形', fontsize=11)
save(fig, 'v1o-15.png')

# ============ 16. 上涨二颗星与下跌三颗星 ============
fig, axes = plt.subplots(1, 2, figsize=(6, 3.5))
ax = axes[0]
draw_kline(ax, 1, 8, 11, 11.5, 7.8)   # 大阳线
draw_kline(ax, 2, 11.2, 11.5, 11.8, 11) # 小星线
draw_kline(ax, 3, 11.6, 11.9, 12.2, 11.4) # 小星线
setup_ax(ax, (0, 4), (7, 13))
ax.set_title('上涨二颗星', fontsize=11)
ax = axes[1]
draw_kline(ax, 1, 12, 8, 12.5, 7.5)    # 大阴线
draw_kline(ax, 2, 7.8, 7.5, 8.2, 7.2)
draw_kline(ax, 3, 7.6, 7.3, 8, 7)
draw_kline(ax, 4, 7.4, 7.1, 7.8, 6.8)
setup_ax(ax, (0, 5), (6.5, 13))
ax.set_title('下跌三颗星', fontsize=11)
save(fig, 'v1o-16.png')

# ============ 17. 跳空上扬形（升势鹤鸦缺口） ============
fig, ax = plt.subplots(figsize=(5, 3.5))
draw_kline(ax, 1, 8, 9.5, 10, 7.8)     # 跳空上扬阳线
draw_kline(ax, 2, 9.5, 10.5, 11, 9)    # 继续上行
draw_kline(ax, 3, 11.5, 10.5, 12, 10.3) # 次日阴线，收盘在缺口附近
setup_ax(ax, (0, 4), (7, 13))
# 画缺口虚线
ax.plot([1.5, 3.5], [9.0, 9.0], 'k--', linewidth=1, alpha=0.5)
ax.set_title('跳空上扬形（升势鹤鸦缺口）', fontsize=11)
save(fig, 'v1o-17.png')

# ============ 18. 双飞乌鸦与三只乌鸦 ============
fig, axes = plt.subplots(1, 2, figsize=(6, 3.5))
ax = axes[0]
draw_kline(ax, 1, 8, 10, 10.5, 7.8)   # 大阳线
draw_kline(ax, 2, 10.5, 9.5, 11, 9.3)  # 第一根高开阴线
draw_kline(ax, 3, 10, 8.5, 10.5, 8.3)  # 第二根高开阴线吞没
setup_ax(ax, (0, 4), (7, 12))
ax.set_title('双飞乌鸦', fontsize=11)
ax = axes[1]
draw_kline(ax, 1, 8, 10, 10.5, 7.8)   # 大阳线
draw_kline(ax, 2, 10.5, 9, 11, 8.8)
draw_kline(ax, 3, 10, 8, 10.5, 7.8)
draw_kline(ax, 4, 9.5, 7, 10, 6.8)
setup_ax(ax, (0, 5), (6.5, 12))
ax.set_title('三只乌鸦', fontsize=11)
save(fig, 'v1o-18.png')

# ============ 19. 下降覆盖线 ============
fig, ax = plt.subplots(figsize=(5, 3.5))
# 穿头破脚 + 后一根阴线深入阳线
draw_kline(ax, 1, 8, 12, 12.5, 7.5)    # 阳线
draw_kline(ax, 2, 12.5, 8, 13, 7.5)    # 穿头破脚阴线
draw_kline(ax, 3, 8.5, 10, 10.5, 8.3)  # 反弹阳线
draw_kline(ax, 4, 10.5, 8.5, 11, 8.3)  # 阴线深入前阳线
setup_ax(ax, (0, 5), (7, 14))
ax.set_title('下降覆盖线', fontsize=11)
save(fig, 'v1o-19.png')

# ============ 20. 加速度线 ============
fig, axes = plt.subplots(1, 2, figsize=(6, 3.5))
ax = axes[0]
prices_up = [(8,8.5),(8.5,9),(9,10),(10,12),(12,15)]
for i,(o,c) in enumerate(prices_up):
    draw_kline(ax, i+1, o, c, c+0.3, o-0.3)
setup_ax(ax, (0, 6), (7, 16))
ax.set_title('上涨加速度线', fontsize=11)
ax = axes[1]
prices_dn = [(15,14.5),(14.5,13.5),(13.5,12),(12,9),(9,5)]
for i,(o,c) in enumerate(prices_dn):
    draw_kline(ax, i+1, o, c, o+0.3, c-0.3)
setup_ax(ax, (0, 6), (4, 16))
ax.set_title('下跌加速度线', fontsize=11)
save(fig, 'v1o-20.png')

# ============ 21. 镊子线 ============
fig, axes = plt.subplots(1, 2, figsize=(6, 3.5))
# 涨势中镊子线（顶部）
ax = axes[0]
draw_kline(ax, 1, 8, 11, 11.5, 7.8)    # 大阳线
draw_kline(ax, 2, 11.2, 10.8, 11.5, 10.5) # 中间小K线
draw_kline(ax, 3, 11, 8.5, 11.5, 8)    # 大阴线（最高点相同）
setup_ax(ax, (0, 4), (7, 12))
ax.set_title('涨势镊子线（见顶）', fontsize=11)
# 跌势中镊子线（底部）
ax = axes[1]
draw_kline(ax, 1, 12, 8.5, 12.5, 8)    # 大阴线
draw_kline(ax, 2, 8.3, 8.5, 8.8, 8.2)  # 中间小K线
draw_kline(ax, 3, 8.5, 11, 8.8, 8)     # 大阳线（最低点相同）
setup_ax(ax, (0, 4), (7.5, 13))
ax.set_title('跌势镊子线（见底）', fontsize=11)
save(fig, 'v1o-21.png')

# ============ 22. 尽头线 ============
fig, axes = plt.subplots(1, 2, figsize=(6, 3.5))
# 涨势尽头线
ax = axes[0]
draw_kline(ax, 1, 8, 12, 14, 7.8)     # 长阳线带上影
draw_kline(ax, 2, 12.5, 12.8, 13.2, 12.3) # 小K线完全在上影线内
setup_ax(ax, (0, 3), (7, 15))
ax.set_title('涨势尽头线', fontsize=11)
# 跌势尽头线
ax = axes[1]
draw_kline(ax, 1, 12, 8, 12.2, 6)     # 长阴线带下影
draw_kline(ax, 2, 7.5, 7.2, 7.7, 6.8)  # 小K线完全在下影线内
setup_ax(ax, (0, 3), (5.5, 13))
ax.set_title('跌势尽头线', fontsize=11)
save(fig, 'v1o-22.png')

# ============ 23. 搓揉线 ============
fig, axes = plt.subplots(1, 2, figsize=(6, 3.5))
ax = axes[0]
draw_kline(ax, 1, 10, 10, 12, 9)       # 倒T字线（上影长）
draw_kline(ax, 2, 10, 10, 10.2, 8)     # T字线（下影长）
setup_ax(ax, (0, 3), (7, 13))
ax.set_title('搓揉线（洗盘）', fontsize=11)
ax = axes[1]
draw_kline(ax, 1, 10, 10, 15, 8.5)
draw_kline(ax, 2, 10, 10, 10.3, 5.5)
setup_ax(ax, (0, 3), (5, 16))
ax.set_title('搓揉线（变盘）', fontsize=11)
save(fig, 'v1o-23.png')

# ============ 24. 穿头破脚与身怀六甲 ============
fig, axes = plt.subplots(1, 2, figsize=(6, 3.5))
ax = axes[0]
draw_kline(ax, 1, 9, 11, 11.5, 8.5)    # 阳线
draw_kline(ax, 2, 11.5, 8, 12, 7.5)    # 阴线完全吞没
setup_ax(ax, (0, 3), (7, 13))
ax.set_title('穿头破脚（阴包阳）', fontsize=11)
ax = axes[1]
draw_kline(ax, 1, 8, 12, 12.5, 7.5)    # 大阳线
draw_kline(ax, 2, 9.5, 10.5, 11, 9)    # 小K线在大阳线内
setup_ax(ax, (0, 3), (7, 13))
ax.set_title('身怀六甲', fontsize=11)
save(fig, 'v1o-24.png')

# ============ 25. 连续跳空三阳线与三阴线 ============
fig, axes = plt.subplots(1, 2, figsize=(6, 3.5))
ax = axes[0]
draw_kline(ax, 1, 8, 9, 9.5, 7.8)
draw_kline(ax, 2, 9.5, 11, 11.5, 9.3)  # 跳空
draw_kline(ax, 3, 11.5, 13.5, 14, 11.3) # 跳空
setup_ax(ax, (0, 4), (7, 15))
ax.set_title('连续跳空三阳线', fontsize=11)
ax = axes[1]
draw_kline(ax, 1, 14, 12, 14.2, 11.5)
draw_kline(ax, 2, 11.5, 9.5, 11.3, 9)   # 跳空
draw_kline(ax, 3, 9, 7, 8.8, 6.5)       # 跳空
setup_ax(ax, (0, 4), (6, 15))
ax.set_title('连续跳空三阴线', fontsize=11)
save(fig, 'v1o-25.png')

# ============ 26. 下档五阳线（低档五阳线） ============
fig, ax = plt.subplots(figsize=(5, 3.5))
draw_kline(ax, 1, 12, 8, 12.5, 7.5)    # 前期大阴线
for i in range(5):
    draw_kline(ax, i+2, 8.2+i*0.1, 8.8+i*0.15, 9.2+i*0.15, 7.8+i*0.08)
setup_ax(ax, (0, 8), (7, 13))
ax.set_title('下档五阳线', fontsize=11)
save(fig, 'v1o-26.png')

# ============ 27. 阳线跛脚形与倒三阳 ============
fig, axes = plt.subplots(1, 2, figsize=(6, 3.5))
ax = axes[0]
draw_kline(ax, 1, 8, 10, 10.5, 7.8)
draw_kline(ax, 2, 9.5, 11, 11.5, 9.3)   # 低开阳线
draw_kline(ax, 3, 10.5, 10.8, 11.3, 10.3) # 低开，收盘更低
setup_ax(ax, (0, 4), (7, 12))
ax.set_title('阳线跛脚形', fontsize=11)
ax = axes[1]
draw_kline(ax, 1, 10, 12, 12.5, 9.8)
draw_kline(ax, 2, 11, 11.5, 12, 10.5)    # 低开高走但收盘低于前
draw_kline(ax, 3, 10, 10.5, 11, 9.5)
setup_ax(ax, (0, 4), (9, 13))
ax.set_title('倒三阳', fontsize=11)
save(fig, 'v1o-27.png')

# ============ 28. 下跌三连阴 ============
fig, axes = plt.subplots(1, 2, figsize=(6, 3.5))
ax = axes[0]
draw_kline(ax, 1, 12, 10, 12.5, 9.5)
draw_kline(ax, 2, 10, 8.5, 10.5, 8)
draw_kline(ax, 3, 8.5, 6, 9, 5.5)
setup_ax(ax, (0, 4), (5, 13))
ax.set_title('下跌三连阴（初期）', fontsize=11)
ax = axes[1]
draw_kline(ax, 1, 14, 12, 14.5, 11.5)
draw_kline(ax, 2, 12, 9, 12.5, 8.5)
draw_kline(ax, 3, 9, 5, 9.5, 4.5)
setup_ax(ax, (0, 4), (4, 15))
ax.set_title('下跌三连阴（末期）', fontsize=11)
save(fig, 'v1o-28.png')

print("All done!")
