# -*- coding: utf-8 -*-
"""
修复脚本：按照 markdown 文章 v1-original-kline.md 的编号约定，
重新生成 v1o-01 ~ v1o-53 的所有单形态K线图。
v1o-54 ~ v1o-74 已经正确，不需要重新生成。
v1o-75 新增：高档五阴线。
"""
import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'FangSong', 'SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os
import random

OUT = r"E:\生活\股票操练大全全套\stock-blog\source\images\kxian"
os.makedirs(OUT, exist_ok=True)

UP = '#FF4444'   # 阳线红
DN = '#00AA00'   # 阴线绿

def draw_kline(ax, x, o, c, h, l, width=0.35):
    color = UP if c >= o else DN
    ax.plot([x, x], [l, h], color=color, linewidth=1.5)
    bottom = min(o, c)
    height = max(abs(c - o), 0.05)
    rect = patches.Rectangle((x - width/2, bottom), width, height,
                            facecolor=color, edgecolor=color, linewidth=1)
    ax.add_patch(rect)

def save(fig, name):
    path = os.path.join(OUT, name)
    fig.savefig(path, dpi=150, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close(fig)
    print(f"saved {name}")

def single(figsize=(3, 2.5), xlim=(-0.5, 3.5), ylim=(0, 10)):
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.axis('off')
    return fig, ax

# ============ 单根K线类 ============

# v1o-01 大阳线
fig, ax = single((2.5, 3), (-0.5, 1.5), (2, 9))
draw_kline(ax, 0.5, 3, 8, 8.5, 2.5)
save(fig, 'v1o-01.png')

# v1o-02 大阴线
fig, ax = single((2.5, 3), (-0.5, 1.5), (2, 9))
draw_kline(ax, 0.5, 8, 3, 8.5, 2.5)
save(fig, 'v1o-02.png')

# v1o-03 锤头线（下跌末端，小实体+长下影线）
fig, ax = single((3, 3), (-0.5, 4.5), (1, 9))
draw_kline(ax, 1, 7, 7.5, 7.8, 6.5)
draw_kline(ax, 2, 6.5, 7, 7.3, 5.5)
draw_kline(ax, 3, 5.5, 6, 6.3, 4)   # 锤头
save(fig, 'v1o-03.png')

# v1o-04 吊颈线（上涨末端，同锤头形状）
fig, ax = single((3, 3), (-0.5, 4.5), (1, 9))
draw_kline(ax, 1, 3, 3.5, 3.8, 2.5)
draw_kline(ax, 2, 3.5, 4.5, 4.8, 3)
draw_kline(ax, 3, 5.5, 6, 6.3, 4)   # 吊颈
save(fig, 'v1o-04.png')

# v1o-05 倒锤头线（下跌末端，小实体+长上影线）
fig, ax = single((3, 3), (-0.5, 4.5), (1, 9))
draw_kline(ax, 1, 7, 7.5, 8, 6.5)
draw_kline(ax, 2, 6.5, 6, 6.5, 5.5)
draw_kline(ax, 3, 5, 5.5, 8, 4.8)   # 倒锤头
save(fig, 'v1o-05.png')

# v1o-06 射击之星（上涨末端，同倒锤头形状）
fig, ax = single((3, 3), (-0.5, 4.5), (1, 9))
draw_kline(ax, 1, 3, 3.5, 4, 2.5)
draw_kline(ax, 2, 3.5, 4.5, 5, 3)
draw_kline(ax, 3, 5.5, 5, 8, 4.8)   # 射击之星
save(fig, 'v1o-06.png')

# v1o-07 T字线（开盘=收盘=最高价，长下影线）
fig, ax = single((2.5, 3), (-0.5, 1.5), (2, 8))
draw_kline(ax, 0.5, 5, 5, 5.2, 2.5)
save(fig, 'v1o-07.png')

# v1o-08 倒T字线（开盘=收盘=最低价，长上影线）
fig, ax = single((2.5, 3), (-0.5, 1.5), (2, 8))
draw_kline(ax, 0.5, 5, 5, 7.5, 4.8)
save(fig, 'v1o-08.png')

# v1o-09 一字线（四价同一）
fig, ax = single((2, 2), (-0.5, 1.5), (4.5, 5.5))
draw_kline(ax, 0.5, 5, 5, 5, 5)
save(fig, 'v1o-09.png')

# v1o-10 长十字线（十字星，上下影线都很长）
fig, ax = single((2.5, 3), (-0.5, 1.5), (1, 9))
draw_kline(ax, 0.5, 5, 5, 8.5, 1.5)
save(fig, 'v1o-10.png')

# v1o-11 螺旋桨（小实体+长上下影线）
fig, ax = single((2.5, 3), (-0.5, 1.5), (1, 9))
draw_kline(ax, 0.5, 4.8, 5.2, 8.5, 1.5)
save(fig, 'v1o-11.png')

# ============ 两根K线组合 ============

# v1o-12 曙光初现（阴线+阳线深入一半以上）
fig, ax = single((3, 3), (-0.5, 3.5), (2, 9))
draw_kline(ax, 1, 8, 4, 8.5, 3.5)   # 大阴线
draw_kline(ax, 2, 3.5, 6.5, 7, 3)  # 阳线深入阴线实体一半以上
save(fig, 'v1o-12.png')

# v1o-13 乌云盖顶（阳线+阴线深入一半以上）
fig, ax = single((3, 3), (-0.5, 3.5), (2, 9))
draw_kline(ax, 1, 4, 8, 8.5, 3.5)   # 大阳线
draw_kline(ax, 2, 8.5, 5.5, 9, 5)   # 阴线深入阳线实体一半以上
save(fig, 'v1o-13.png')

# v1o-14 旭日东升（阴线+大阳线收盘超过阴线开盘）
fig, ax = single((3, 3), (-0.5, 3.5), (2, 10))
draw_kline(ax, 1, 8, 4, 8.5, 3.5)    # 大阴线
draw_kline(ax, 2, 5, 9, 9.5, 4.5)    # 大阳线收盘超过阴线开盘
save(fig, 'v1o-14.png')

# v1o-15 倾盆大雨（阳线+大阴线收盘低于阳线开盘）
fig, ax = single((3, 3), (-0.5, 3.5), (2, 10))
draw_kline(ax, 1, 3, 7, 7.5, 2.5)    # 大阳线
draw_kline(ax, 2, 6, 2.5, 6.5, 2)    # 大阴线收盘低于阳线开盘
save(fig, 'v1o-15.png')

# v1o-20 身怀六甲（长K线+短K线在长K线内）
fig, ax = single((3, 3), (-0.5, 3.5), (2, 9))
draw_kline(ax, 1, 3, 8, 8.5, 2.5)    # 长阳线
draw_kline(ax, 2, 5.5, 6.5, 7, 5)    # 短K线在长阳线内
save(fig, 'v1o-20.png')

# v1o-21 穿头破脚（后一根吞没前一根）
fig, ax = single((3, 3), (-0.5, 3.5), (2, 9))
draw_kline(ax, 1, 5, 7, 7.5, 4.5)    # 阳线
draw_kline(ax, 2, 7.5, 3, 8, 2.5)    # 阴线完全吞没
save(fig, 'v1o-21.png')

# v1o-22 平底（两根K线最低价相同）
fig, ax = single((3, 3), (-0.5, 3.5), (2, 9))
draw_kline(ax, 1, 7, 4, 7.5, 3)
draw_kline(ax, 2, 4.5, 6, 6.5, 3)
save(fig, 'v1o-22.png')

# v1o-23 平顶（两根K线最高价相同）
fig, ax = single((3, 3), (-0.5, 3.5), (2, 9))
draw_kline(ax, 1, 3, 7, 8, 2.5)
draw_kline(ax, 2, 7, 5, 8, 4.5)
save(fig, 'v1o-23.png')

# v1o-50 好友反攻（阴线+阳线收盘与阴线收盘接近）
fig, ax = single((3, 3), (-0.5, 3.5), (2, 9))
draw_kline(ax, 1, 8, 4, 8.5, 3.5)    # 大阴线
draw_kline(ax, 2, 3.5, 4, 4.5, 3)     # 跳空低开收阳线，收盘与阴线收盘接近
save(fig, 'v1o-50.png')

# v1o-51 淡友反攻（阳线+阴线收盘与阳线收盘接近）
fig, ax = single((3, 3), (-0.5, 3.5), (2, 9))
draw_kline(ax, 1, 3, 7, 7.5, 2.5)    # 大阳线
draw_kline(ax, 2, 8, 7, 8.5, 6.5)    # 跳空高开收阴线，收盘与阳线收盘接近
save(fig, 'v1o-51.png')

# ============ 三根K线组合 ============

# v1o-16 早晨十字星（阴线+十字星+阳线）
fig, ax = single((3.5, 3), (-0.5, 4), (2, 9))
draw_kline(ax, 1, 8, 4, 8.5, 3.5)
draw_kline(ax, 2, 4.2, 4.2, 5, 3.5)   # 十字星
draw_kline(ax, 3, 4.5, 7.5, 8, 4)
save(fig, 'v1o-16.png')

# v1o-17 黄昏十字星（阳线+十字星+阴线）
fig, ax = single((3.5, 3), (-0.5, 4), (2, 9))
draw_kline(ax, 1, 3, 7, 7.5, 2.5)
draw_kline(ax, 2, 7.2, 7.2, 8, 6.5)   # 十字星
draw_kline(ax, 3, 7, 4, 7.5, 3.5)
save(fig, 'v1o-17.png')

# v1o-18 早晨之星（阴线+小K线+阳线）
fig, ax = single((3.5, 3), (-0.5, 4), (2, 9))
draw_kline(ax, 1, 8, 4, 8.5, 3.5)
draw_kline(ax, 2, 4.2, 4.5, 5, 3.5)   # 小星线
draw_kline(ax, 3, 4.5, 7.5, 8, 4)
save(fig, 'v1o-18.png')

# v1o-19 黄昏之星（阳线+小K线+阴线）
fig, ax = single((3.5, 3), (-0.5, 4), (2, 9))
draw_kline(ax, 1, 3, 7, 7.5, 2.5)
draw_kline(ax, 2, 7.2, 7.5, 8, 6.5)   # 小星线
draw_kline(ax, 3, 7, 4, 7.5, 3.5)
save(fig, 'v1o-19.png')

# v1o-28 红三兵（三根连续阳线上升）
fig, ax = single((3, 3), (-0.5, 4), (2, 9))
draw_kline(ax, 1, 3, 4.5, 5, 2.8)
draw_kline(ax, 2, 4.5, 6, 6.5, 4.3)
draw_kline(ax, 3, 6, 7.5, 8, 5.8)
save(fig, 'v1o-28.png')

# v1o-29 黑三兵（三根连续阴线下降）
fig, ax = single((3, 3), (-0.5, 4), (2, 9))
draw_kline(ax, 1, 7, 5.5, 7.5, 5.3)
draw_kline(ax, 2, 5.5, 4, 6, 3.8)
draw_kline(ax, 3, 4, 2.5, 4.5, 2.3)
save(fig, 'v1o-29.png')

# v1o-30 三个白色武士（三根大阳线实体较大逐次上升）
fig, ax = single((3, 3), (-0.5, 4), (2, 9))
draw_kline(ax, 1, 3, 5, 5.5, 2.8)
draw_kline(ax, 2, 5, 7, 7.5, 4.8)
draw_kline(ax, 3, 7, 9, 9.5, 6.8)
save(fig, 'v1o-30.png')

# v1o-31 升势受阻（三根阳线，后两根实体短且有上影线）
fig, ax = single((3, 3), (-0.5, 4), (2, 9))
draw_kline(ax, 1, 3, 5.5, 6, 2.8)
draw_kline(ax, 2, 5.5, 6.5, 7, 5.3)
draw_kline(ax, 3, 6.5, 6.8, 8, 6.3)   # 实体短，上影线长
save(fig, 'v1o-31.png')

# ============ 多根K线形态 ============

# v1o-24 圆底（弧形下跌后弧形上涨）
fig, ax = single((4, 3), (-0.5, 8.5), (2, 9))
prices = [7.5, 6.5, 5.5, 4.8, 4.5, 5, 6, 7.5]
for i, p in enumerate(prices):
    o = p - 0.15
    c = p + 0.15 if i % 2 == 0 else p - 0.1
    h = max(o, c) + 0.2
    l = min(o, c) - 0.2
    draw_kline(ax, i+1, o, c, h, l)
xs = np.linspace(0.5, 8, 100)
ys = 8 - 0.08*(xs-4.5)**2
ax.plot(xs, ys, 'k--', linewidth=1, alpha=0.5)
save(fig, 'v1o-24.png')

# v1o-25 圆顶（弧形上涨后弧形下跌）
fig, ax = single((4, 3), (-0.5, 8.5), (2, 9))
prices = [3.5, 4.5, 5.5, 6.5, 7, 6.5, 5.5, 4]
for i, p in enumerate(prices):
    o = p - 0.15
    c = p + 0.15 if i % 2 == 0 else p - 0.1
    h = max(o, c) + 0.2
    l = min(o, c) - 0.2
    draw_kline(ax, i+1, o, c, h, l)
xs = np.linspace(0.5, 8, 100)
ys = 3 + 0.08*(xs-4.5)**2
ax.plot(xs, ys, 'k--', linewidth=1, alpha=0.5)
save(fig, 'v1o-25.png')

# v1o-26 塔形底（大阴线+小阴小阳盘整+大阳线）
fig, ax = single((4, 3), (-0.5, 7.5), (2, 9))
draw_kline(ax, 1, 8, 4, 8.5, 3.5)
for i in range(2, 6):
    p = 5 + 0.15*(i-2)
    draw_kline(ax, i, p-0.2, p+0.2, p+0.4, p-0.4)
draw_kline(ax, 6, 5, 8, 8.5, 4.8)
save(fig, 'v1o-26.png')

# v1o-27 塔形顶（大阳线+小阴小阳盘整+大阴线）
fig, ax = single((4, 3), (-0.5, 7.5), (2, 9))
draw_kline(ax, 1, 3, 7, 7.5, 2.5)
for i in range(2, 6):
    p = 6 - 0.15*(i-2)
    draw_kline(ax, i, p+0.2, p-0.2, p+0.4, p-0.4)
draw_kline(ax, 6, 5, 2, 5.5, 1.5)
save(fig, 'v1o-27.png')

# v1o-32 冉冉上升形（多根小阳线缓慢向上）
fig, ax = single((4, 3), (-0.5, 8.5), (2, 9))
random.seed(42)
base = 3
for i in range(8):
    o = base + i*0.5 + random.uniform(-0.1, 0.1)
    c = o + random.choice([0.15, -0.1])
    h = max(o, c) + 0.15
    l = min(o, c) - 0.15
    draw_kline(ax, i+1, o, c, h, l)
save(fig, 'v1o-32.png')

# v1o-33 绵绵阴跌形（多根小阴线缓慢向下）
fig, ax = single((4, 3), (-0.5, 8.5), (2, 9))
base = 7
for i in range(8):
    o = base - i*0.5 + random.uniform(-0.1, 0.1)
    c = o + random.choice([-0.15, 0.1])
    h = max(o, c) + 0.15
    l = min(o, c) - 0.15
    draw_kline(ax, i+1, o, c, h, l)
save(fig, 'v1o-33.png')

# v1o-34 徐缓上升形（先小阳线后大阳线）
fig, ax = single((4, 3), (-0.5, 6.5), (2, 9))
draw_kline(ax, 1, 3, 3.5, 3.8, 2.8)
draw_kline(ax, 2, 3.5, 4, 4.3, 3.3)
draw_kline(ax, 3, 4, 4.5, 4.8, 3.8)
draw_kline(ax, 4, 4.5, 5, 5.3, 4.3)
draw_kline(ax, 5, 5, 8, 8.5, 4.8)
save(fig, 'v1o-34.png')

# v1o-35 徐缓下降形（先小阴线后大阴线）
fig, ax = single((4, 3), (-0.5, 6.5), (2, 9))
draw_kline(ax, 1, 7, 6.5, 7.2, 6.3)
draw_kline(ax, 2, 6.5, 6, 6.7, 5.8)
draw_kline(ax, 3, 6, 5.5, 6.2, 5.3)
draw_kline(ax, 4, 5.5, 5, 5.7, 4.8)
draw_kline(ax, 5, 5, 2.5, 5.2, 2)
save(fig, 'v1o-35.png')

# v1o-36 上升抵抗形（连续跳高，中间夹小阴线不补缺口）
fig, ax = single((4, 3), (-0.5, 6.5), (2, 9))
draw_kline(ax, 1, 3, 4.5, 4.8, 2.8)
draw_kline(ax, 2, 4.8, 5.2, 5.5, 4.6)
draw_kline(ax, 3, 5.5, 5.0, 5.8, 4.8)   # 阴线但收盘仍高于前阳
draw_kline(ax, 4, 6, 6.5, 6.8, 5.8)
draw_kline(ax, 5, 7, 6.5, 7.3, 6.3)     # 阴线收盘高于前阳
save(fig, 'v1o-36.png')

# v1o-37 下降抵抗形（连续跳低，中间夹小阳线不补缺口）
fig, ax = single((4, 3), (-0.5, 6.5), (2, 9))
draw_kline(ax, 1, 7, 5.5, 7.2, 5.3)
draw_kline(ax, 2, 5.2, 4.8, 5.5, 4.6)
draw_kline(ax, 3, 4.5, 5.0, 4.8, 4.3)   # 阳线但收盘仍低于前阴
draw_kline(ax, 4, 4, 3.5, 4.3, 3.3)
draw_kline(ax, 5, 3, 3.6, 3.3, 2.8)     # 阳线收盘低于前阴
save(fig, 'v1o-37.png')

# v1o-38 稳步上涨形（阳线多阴线少，实体逐渐增大）
fig, ax = single((4, 3), (-0.5, 8.5), (2, 9))
random.seed(11)
base = 3
for i in range(8):
    o = base + i*0.6
    c = o + random.choice([0.2, -0.15, 0.25, -0.1])
    h = max(o, c) + 0.2
    l = min(o, c) - 0.2
    draw_kline(ax, i+1, o, c, h, l)
save(fig, 'v1o-38.png')

# v1o-39 下跌不止形（阴线多阳线少，实体逐渐增大）
fig, ax = single((4, 3), (-0.5, 8.5), (2, 9))
base = 7
for i in range(8):
    o = base - i*0.6
    c = o + random.choice([-0.2, 0.15, -0.25, 0.1])
    h = max(o, c) + 0.2
    l = min(o, c) - 0.2
    draw_kline(ax, i+1, o, c, h, l)
save(fig, 'v1o-39.png')

# v1o-40 高位并排阳线（上涨中两根并排阳线有跳空）
fig, ax = single((3, 3), (-0.5, 4.5), (2, 9))
draw_kline(ax, 1, 3, 6, 6.5, 2.8)
draw_kline(ax, 2, 7, 7.5, 8, 6.8)
draw_kline(ax, 3, 7, 7.8, 8.3, 6.8)
save(fig, 'v1o-40.png')

# v1o-41 低位并排阳线（下跌中两根并排阳线有跳空）
fig, ax = single((3, 3), (-0.5, 4.5), (2, 9))
draw_kline(ax, 1, 8, 4, 8.5, 3.5)
draw_kline(ax, 2, 3.5, 4.2, 4.5, 3)
draw_kline(ax, 3, 3.5, 4.5, 4.8, 3)
save(fig, 'v1o-41.png')

# v1o-42 上档盘旋形（大阳线后高位盘整）
fig, ax = single((4.5, 3), (-0.5, 9.5), (2, 9))
draw_kline(ax, 1, 3, 7.5, 8, 2.8)
random.seed(22)
for i in range(7):
    o = 6.5 + random.uniform(-0.3, 0.3)
    c = o + random.uniform(-0.2, 0.2)
    h = max(o, c) + 0.15
    l = min(o, c) - 0.15
    draw_kline(ax, i+2, o, c, h, l)
save(fig, 'v1o-42.png')

# v1o-43 低档盘旋形（下跌后低位盘整再跌破）
fig, ax = single((4.5, 3), (-0.5, 9.5), (2, 9))
draw_kline(ax, 1, 8, 4.5, 8.5, 4)
random.seed(33)
for i in range(6):
    o = 5.5 + random.uniform(-0.2, 0.2)
    c = o + random.uniform(-0.15, 0.15)
    h = max(o, c) + 0.15
    l = min(o, c) - 0.15
    draw_kline(ax, i+2, o, c, h, l)
draw_kline(ax, 9, 5, 2.5, 5.2, 2)
save(fig, 'v1o-43.png')

# v1o-44 上升三部曲（大阳线+三根小阴线+大阳线）
fig, ax = single((4, 3.5), (-0.5, 6.5), (2, 9))
draw_kline(ax, 1, 3, 7.5, 8, 2.8)
draw_kline(ax, 2, 7, 6.5, 7.3, 6.3)
draw_kline(ax, 3, 6.5, 6, 6.8, 5.8)
draw_kline(ax, 4, 6, 5.5, 6.3, 5.3)
draw_kline(ax, 5, 5.8, 8, 8.5, 5.6)
save(fig, 'v1o-44.png')

# v1o-45 下降三部曲（大阴线+三根小阳线+大阴线）
fig, ax = single((4, 3.5), (-0.5, 6.5), (2, 9))
draw_kline(ax, 1, 7.5, 3, 8, 2.8)
draw_kline(ax, 2, 3.5, 4, 4.3, 3.3)
draw_kline(ax, 3, 4, 4.5, 4.8, 3.8)
draw_kline(ax, 4, 4.5, 5, 5.3, 4.3)
draw_kline(ax, 5, 5, 2.5, 5.5, 2.3)
save(fig, 'v1o-45.png')

# v1o-46 两红夹一黑（阳线+阴线+阳线）
fig, ax = single((3, 3), (-0.5, 4), (2, 9))
draw_kline(ax, 1, 3, 7, 7.5, 2.5)
draw_kline(ax, 2, 5.5, 4.5, 6, 4.3)
draw_kline(ax, 3, 4.5, 7.5, 8, 4.3)
save(fig, 'v1o-46.png')

# v1o-47 两黑夹一红（阴线+阳线+阴线）
fig, ax = single((3, 3), (-0.5, 4), (2, 9))
draw_kline(ax, 1, 7, 3, 7.5, 2.5)
draw_kline(ax, 2, 4.5, 5.5, 6, 4.3)
draw_kline(ax, 3, 5.5, 2.5, 6, 2.3)
save(fig, 'v1o-47.png')

# v1o-48 多方尖兵（上涨中阳线带上影线，后突破上影线高点）
fig, ax = single((3.5, 3), (-0.5, 5.5), (2, 9))
draw_kline(ax, 1, 3, 5, 5.5, 2.8)
draw_kline(ax, 2, 5, 6.5, 8, 4.8)    # 带上影线的阳线
draw_kline(ax, 3, 6.5, 6, 7, 5.8)    # 回落
draw_kline(ax, 4, 6, 6.5, 7.2, 5.8)
draw_kline(ax, 5, 6.5, 8.5, 9, 6.3)  # 突破上影线
save(fig, 'v1o-48.png')

# v1o-49 空方尖兵（下跌中阴线下影线，后跌破下影线低点）
fig, ax = single((3.5, 3), (-0.5, 5.5), (2, 9))
draw_kline(ax, 1, 7, 5, 7.5, 4.8)
draw_kline(ax, 2, 5, 3.5, 5.2, 1.5)  # 带下影线的阴线
draw_kline(ax, 3, 3.5, 4, 4.5, 3.3)  # 反弹
draw_kline(ax, 4, 4, 3.5, 4.7, 3.3)
draw_kline(ax, 5, 3.5, 2, 3.7, 1.5)  # 跌破下影线
save(fig, 'v1o-49.png')

# v1o-52 上涨二颗星（大阳线后两根小K线）
fig, ax = single((3, 3), (-0.5, 4.5), (2, 9))
draw_kline(ax, 1, 3, 7, 7.5, 2.8)
draw_kline(ax, 2, 7.2, 7.5, 7.8, 7)
draw_kline(ax, 3, 7.6, 7.9, 8.2, 7.4)
save(fig, 'v1o-52.png')

# v1o-53 下跌三颗星（大阴线后三根小K线）
fig, ax = single((3, 3), (-0.5, 5.5), (2, 9))
draw_kline(ax, 1, 8, 4, 8.5, 3.5)
draw_kline(ax, 2, 4.2, 3.8, 4.5, 3.5)
draw_kline(ax, 3, 4, 3.6, 4.3, 3.3)
draw_kline(ax, 4, 3.8, 3.4, 4.1, 3.1)
save(fig, 'v1o-53.png')

# v1o-75 高档五阴线（高位连续5根阴线）
fig, ax = single((3, 3), (-0.5, 6.5), (0, 9))
draw_kline(ax, 1, 8, 6.5, 8.2, 6.3)
draw_kline(ax, 2, 6.5, 5, 6.7, 4.8)
draw_kline(ax, 3, 5, 3.5, 5.2, 3.3)
draw_kline(ax, 4, 3.5, 2, 3.7, 1.8)
draw_kline(ax, 5, 2, 0.8, 2.2, 0.6)
save(fig, 'v1o-75.png')

print("All fix images generated!")
