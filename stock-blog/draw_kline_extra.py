# -*- coding: utf-8 -*-
"""补充K线形态重绘图 v1o-29 ~ v1o-50"""
import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'FangSong', 'SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

OUT = r"E:\生活\股票操练大全全套\stock-blog\source\images\kxian"

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

def new_ax(xlim, ylim):
    fig, ax = plt.subplots(figsize=(4, 3))
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.axis('off')
    return fig, ax

def save(fig, name):
    path = os.path.join(OUT, name)
    fig.savefig(path, dpi=150, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close(fig)
    print(f"saved {name}")

# 29. 早晨十字星：大阴线+十字星+大阳线
fig, ax = new_ax((0, 4), (6.5, 13))
draw_kline(ax, 1, 12, 8, 12.5, 7.5)
draw_kline(ax, 2, 7.5, 7.5, 8.2, 6.8)  # 十字星
draw_kline(ax, 3, 7.8, 11, 11.5, 7.3)
save(fig, 'v1o-29.png')

# 30. 黄昏十字星：大阳线+十字星+大阴线
fig, ax = new_ax((0, 4), (6.5, 13.5))
draw_kline(ax, 1, 8, 12, 12.5, 7.5)
draw_kline(ax, 2, 12.5, 12.5, 13.2, 11.8)  # 十字星
draw_kline(ax, 3, 12.2, 9, 12.8, 8.5)
save(fig, 'v1o-30.png')

# 31. 圆底（圆弧底）
fig, ax = new_ax((0, 9), (6, 13))
prices = [11, 10.2, 9.3, 8.5, 8.2, 8.8, 9.8, 11, 12.5]
for i, p in enumerate(prices):
    o = p - 0.15
    c = p + 0.15 if i % 2 == 0 else p - 0.1
    h = max(o,c) + 0.2
    l = min(o,c) - 0.2
    draw_kline(ax, i+1, o, c, h, l)
import numpy as np
xs = np.linspace(0.5, 9.5, 100)
ys = 12.5 - 0.08*(xs-5)**2
ax.plot(xs, ys, 'k--', linewidth=1, alpha=0.5)
save(fig, 'v1o-31.png')

# 32. 圆顶（圆弧顶）
fig, ax = new_ax((0, 9), (6, 13.5))
prices = [8, 8.8, 9.8, 11, 11.5, 11, 9.8, 8.5, 7.5]
for i, p in enumerate(prices):
    o = p - 0.15
    c = p + 0.15 if i % 2 == 0 else p - 0.1
    h = max(o,c) + 0.2
    l = min(o,c) - 0.2
    draw_kline(ax, i+1, o, c, h, l)
xs = np.linspace(0.5, 9.5, 100)
ys = 7.5 + 0.08*(xs-5)**2
ax.plot(xs, ys, 'k--', linewidth=1, alpha=0.5)
save(fig, 'v1o-32.png')

# 33. 三个白色武士（3根小阳线收于最高）
fig, ax = new_ax((0, 4), (7, 13))
draw_kline(ax, 1, 8, 9.2, 9.5, 7.8)
draw_kline(ax, 2, 9.2, 10.5, 10.8, 9.0)
draw_kline(ax, 3, 10.5, 11.8, 12.0, 10.3)
save(fig, 'v1o-33.png')

# 34. 升势受阻（3阳线实体递减，上影线长）
fig, ax = new_ax((0, 4), (7, 13))
draw_kline(ax, 1, 8, 10.5, 10.8, 7.8)
draw_kline(ax, 2, 10.5, 11.5, 11.8, 10.3)
draw_kline(ax, 3, 11.5, 11.8, 12.8, 11.3)  # 实体小，上影线长
save(fig, 'v1o-34.png')

# 35. 两红夹一黑
fig, ax = new_ax((0, 4), (7, 13))
draw_kline(ax, 1, 8, 11, 11.5, 7.8)   # 长阳线
draw_kline(ax, 2, 10, 9.5, 10.5, 9.2)  # 短阴线
draw_kline(ax, 3, 9.8, 12, 12.5, 9.6)  # 长阳线
save(fig, 'v1o-35.png')

# 36. 两黑夹一红
fig, ax = new_ax((0, 4), (7, 13))
draw_kline(ax, 1, 12, 9, 12.5, 8.5)    # 长阴线
draw_kline(ax, 2, 10, 10.5, 11, 9.8)   # 短阳线
draw_kline(ax, 3, 10.8, 8, 11.3, 7.5)  # 长阴线
save(fig, 'v1o-36.png')

# 37. 上升三部曲（N形）
fig, ax = new_ax((0, 7), (7, 13.5))
draw_kline(ax, 1, 8, 11.5, 12, 7.8)    # 大阳线
draw_kline(ax, 2, 11, 10.5, 11.5, 10.3)
draw_kline(ax, 3, 10.5, 10, 11, 9.8)
draw_kline(ax, 4, 10, 9.5, 10.5, 9.3)
draw_kline(ax, 5, 9.8, 12.5, 13, 9.6)  # 大阳线
save(fig, 'v1o-37.png')

# 38. 下降三部曲
fig, ax = new_ax((0, 7), (6.5, 13))
draw_kline(ax, 1, 12, 8.5, 12.5, 8)    # 大阴线
draw_kline(ax, 2, 9, 9.5, 10, 8.8)
draw_kline(ax, 3, 9.5, 10, 10.5, 9.3)
draw_kline(ax, 4, 10, 10.5, 11, 9.8)
draw_kline(ax, 5, 10.2, 7, 10.8, 6.5)  # 大阴线
save(fig, 'v1o-38.png')

# 39. 徐缓上升形
fig, ax = new_ax((0, 7), (7, 13))
draw_kline(ax, 1, 8, 8.5, 8.8, 7.8)
draw_kline(ax, 2, 8.5, 9, 9.3, 8.3)
draw_kline(ax, 3, 9, 9.5, 9.8, 8.8)
draw_kline(ax, 4, 9.5, 10, 10.3, 9.3)
draw_kline(ax, 5, 10, 12, 12.5, 9.8)   # 中大阳线
save(fig, 'v1o-39.png')

# 40. 徐缓下降形
fig, ax = new_ax((0, 7), (7, 13))
draw_kline(ax, 1, 12, 11.5, 12.2, 11.3)
draw_kline(ax, 2, 11.5, 11, 11.7, 10.8)
draw_kline(ax, 3, 11, 10.5, 11.2, 10.3)
draw_kline(ax, 4, 10.5, 10, 10.7, 9.8)
draw_kline(ax, 5, 10, 7.5, 10.2, 7)    # 中大阴线
save(fig, 'v1o-40.png')

# 41. 上升抵抗形（连续跳高，阴线收盘仍高于前阳）
fig, ax = new_ax((0, 7), (7, 13))
draw_kline(ax, 1, 8, 9.5, 9.8, 7.8)
draw_kline(ax, 2, 9.8, 10.2, 10.5, 9.6)
draw_kline(ax, 3, 10.5, 10.0, 10.8, 9.8)  # 阴线但收盘仍高于前阳
draw_kline(ax, 4, 11, 11.5, 11.8, 10.8)
draw_kline(ax, 5, 12, 11.5, 12.3, 11.3)   # 阴线收盘高于前阳
save(fig, 'v1o-41.png')

# 42. 下降抵抗形
fig, ax = new_ax((0, 7), (6.5, 13))
draw_kline(ax, 1, 12, 10.5, 12.2, 10.3)
draw_kline(ax, 2, 10.2, 9.8, 10.5, 9.6)
draw_kline(ax, 3, 9.5, 10.0, 9.8, 9.3)    # 阳线但收盘仍低于前阴
draw_kline(ax, 4, 9.2, 8.5, 9.5, 8.3)
draw_kline(ax, 5, 8.2, 8.8, 8.5, 8.0)     # 阳线收盘低于前阴
save(fig, 'v1o-42.png')

# 43. 稳步上涨形
fig, ax = new_ax((0, 9), (7, 13))
import random
random.seed(11)
base = 8
for i in range(8):
    o = base + i*0.4
    c = o + random.choice([0.2, -0.15, 0.25, -0.1])
    h = max(o,c) + 0.2
    l = min(o,c) - 0.2
    draw_kline(ax, i+1, o, c, h, l)
save(fig, 'v1o-43.png')

# 44. 下跌不止形
fig, ax = new_ax((0, 9), (6.5, 13))
base = 12
for i in range(8):
    o = base - i*0.4
    c = o + random.choice([-0.2, 0.15, -0.25, 0.1])
    h = max(o,c) + 0.2
    l = min(o,c) - 0.2
    draw_kline(ax, i+1, o, c, h, l)
save(fig, 'v1o-44.png')

# 45. 高位并排阳线
fig, ax = new_ax((0, 4), (7, 13))
draw_kline(ax, 1, 8, 10, 10.5, 7.8)    # 前一根阳线
draw_kline(ax, 2, 11, 11.5, 12, 10.8)  # 跳空
draw_kline(ax, 3, 11, 11.8, 12.3, 10.8) # 并排
save(fig, 'v1o-45.png')

# 46. 低位并排阳线
fig, ax = new_ax((0, 4), (7, 13))
draw_kline(ax, 1, 12, 8, 12.5, 7.5)    # 前一根阴线
draw_kline(ax, 2, 7.5, 8.2, 8.5, 7.0)  # 跳空低开阳线
draw_kline(ax, 3, 7.5, 8.5, 8.8, 7.0)  # 并排阳线
save(fig, 'v1o-46.png')

# 47. 上档盘旋形
fig, ax = new_ax((0, 10), (7, 13))
draw_kline(ax, 1, 8, 11.5, 12, 7.8)    # 大阳线
random.seed(22)
for i in range(7):
    o = 11 + random.uniform(-0.3, 0.3)
    c = o + random.uniform(-0.2, 0.2)
    h = max(o,c) + 0.15
    l = min(o,c) - 0.15
    draw_kline(ax, i+2, o, c, h, l)
save(fig, 'v1o-47.png')

# 48. 低档盘旋形
fig, ax = new_ax((0, 10), (6.5, 13))
draw_kline(ax, 1, 12, 8.5, 12.5, 8)    # 前期下跌
random.seed(33)
for i in range(6):
    o = 9.5 + random.uniform(-0.2, 0.2)
    c = o + random.uniform(-0.15, 0.15)
    h = max(o,c) + 0.15
    l = min(o,c) - 0.15
    draw_kline(ax, i+2, o, c, h, l)
draw_kline(ax, 9, 9, 6.5, 9.2, 6.0)    # 跳空向下
save(fig, 'v1o-48.png')

# 49. 多方尖兵
fig, ax = new_ax((0, 6), (7, 13))
draw_kline(ax, 1, 8, 10, 10.5, 7.8)
draw_kline(ax, 2, 10, 11.5, 12.5, 9.8)  # 带上影线的阳线
draw_kline(ax, 3, 11.5, 11, 12, 10.8)   # 回落
draw_kline(ax, 4, 11, 11.5, 12.2, 10.8)
draw_kline(ax, 5, 11.5, 13, 13.5, 11.3) # 突破上影线
save(fig, 'v1o-49.png')

# 50. 空方尖兵
fig, ax = new_ax((0, 6), (6.5, 13))
draw_kline(ax, 1, 12, 10, 12.5, 9.8)
draw_kline(ax, 2, 10, 8.5, 10.2, 7.5)   # 带下影线的阴线
draw_kline(ax, 3, 8.5, 9, 9.5, 8.3)     # 反弹
draw_kline(ax, 4, 9, 8.5, 9.7, 8.3)
draw_kline(ax, 5, 8.5, 7, 8.7, 6.5)     # 跌破下影线
save(fig, 'v1o-50.png')

print("All supplementary images done!")
