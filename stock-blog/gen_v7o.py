# -*- coding: utf-8 -*-
"""第七册识顶逃顶 K线形态重绘脚本
同花顺风格：阳线 #FF4444，阴线 #00AA00，白底无坐标轴
"""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

plt.rcParams['font.family'] = 'Microsoft JhengHei'
plt.rcParams['axes.unicode_minus'] = False

UP = '#FF4444'
DOWN = '#00AA00'
OUT = r'E:\生活\股票操练大全全套\stock-blog\source\images\kxian'
os.makedirs(OUT, exist_ok=True)


def kline(ax, x, o, c, h, l, w=0.55):
    color = UP if c >= o else DOWN
    ax.plot([x, x], [l, h], color=color, linewidth=1.1, zorder=2)
    top = max(o, c)
    bot = min(o, c)
    hgt = abs(c - o)
    if hgt < 0.02:
        ax.plot([x - w/2, x + w/2], [c, c], color=color, linewidth=1.6, zorder=3)
    else:
        ax.add_patch(patches.Rectangle((x - w/2, bot), w, hgt,
                                       facecolor=color, edgecolor=color, zorder=3))


def new_fig(w=4.2, h=3.2):
    fig, ax = plt.subplots(figsize=(w, h), dpi=150)
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    ax.axis('off')
    return fig, ax


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches='tight',
                facecolor='white', pad_inches=0.15)
    plt.close(fig)
    print('saved', name)


def set_lim(ax, xs, ys, pad=0.6):
    ax.set_xlim(min(xs) - pad, max(xs) + pad)
    ax.set_ylim(min(ys) - pad, max(ys) + pad)


# ============ 单根K线见顶形态 ============

# v7o-01 长十字线 普通型（振幅<10%）
fig, ax = new_fig()
kline(ax, 0, 10.0, 10.05, 11.2, 8.9)
set_lim(ax, [0], [8.9, 11.2])
save(fig, 'v7o-01.png')

# v7o-02 长十字线 增强型（振幅>10%）
fig, ax = new_fig()
kline(ax, 0, 10.0, 10.08, 12.0, 8.0)
set_lim(ax, [0], [8.0, 12.0])
save(fig, 'v7o-02.png')

# v7o-03 长十字线 超强型（振幅>15%）
fig, ax = new_fig()
kline(ax, 0, 10.0, 10.05, 12.5, 7.5)
set_lim(ax, [0], [7.5, 12.5])
save(fig, 'v7o-03.png')

# v7o-04 小十字线
fig, ax = new_fig()
kline(ax, 0, 10.0, 10.05, 10.3, 9.75)
set_lim(ax, [0], [9.75, 10.3])
save(fig, 'v7o-04.png')

# v7o-05 射击之星（阳线实体）
fig, ax = new_fig()
kline(ax, 0, 9.8, 10.1, 11.5, 9.7)
set_lim(ax, [0], [9.7, 11.5])
save(fig, 'v7o-05.png')

# v7o-06 射击之星（阴线实体）
fig, ax = new_fig()
kline(ax, 0, 10.1, 9.8, 11.5, 9.7)
set_lim(ax, [0], [9.7, 11.5])
save(fig, 'v7o-06.png')

# v7o-07 倒T字线
fig, ax = new_fig()
kline(ax, 0, 10.0, 10.0, 11.6, 9.9)
set_lim(ax, [0], [9.9, 11.6])
save(fig, 'v7o-07.png')

# v7o-08 螺旋桨
fig, ax = new_fig()
kline(ax, 0, 9.9, 10.1, 11.8, 8.2)
set_lim(ax, [0], [8.2, 11.8])
save(fig, 'v7o-08.png')

# v7o-09 吊颈线（阳线实体）
fig, ax = new_fig()
kline(ax, 0, 9.8, 10.1, 10.2, 8.0)
set_lim(ax, [0], [8.0, 10.2])
save(fig, 'v7o-09.png')

# v7o-10 吊颈线（阴线实体）
fig, ax = new_fig()
kline(ax, 0, 10.1, 9.8, 10.2, 8.0)
set_lim(ax, [0], [8.0, 10.2])
save(fig, 'v7o-10.png')

# v7o-11 T字线
fig, ax = new_fig()
kline(ax, 0, 10.0, 10.0, 10.1, 8.2)
set_lim(ax, [0], [8.2, 10.1])
save(fig, 'v7o-11.png')

# v7o-12 高位大阳线
fig, ax = new_fig()
kline(ax, 0, 8.5, 10.5, 10.6, 8.4)
set_lim(ax, [0], [8.4, 10.6])
save(fig, 'v7o-12.png')

# ============ 两根K线见顶组合 ============

# v7o-13 身怀六甲（风云突变）：大阳线 + 小K线在其腹中
fig, ax = new_fig()
kline(ax, 0, 8.0, 10.0, 10.2, 7.9)
kline(ax, 1, 9.2, 9.5, 9.7, 9.1)
set_lim(ax, [0, 1], [7.9, 10.2])
save(fig, 'v7o-13.png')

# v7o-14 淡友反攻（黑云压阵）：阳线 + 阴线，收盘价相近
fig, ax = new_fig()
kline(ax, 0, 8.0, 10.0, 10.1, 7.9)
kline(ax, 1, 10.05, 9.95, 10.1, 9.6)
set_lim(ax, [0, 1], [7.9, 10.1])
save(fig, 'v7o-14.png')

# v7o-15 乌云盖顶（长驱直入）：阳线 + 阴线深入阳线实体一半以上
fig, ax = new_fig()
kline(ax, 0, 8.0, 10.0, 10.1, 7.9)
kline(ax, 1, 10.2, 8.9, 10.3, 8.8)
set_lim(ax, [0, 1], [7.9, 10.3])
save(fig, 'v7o-15.png')

# v7o-16 倾盆大雨（暴雨成灾）：阳线 + 阴线收盘低于阳线开盘
fig, ax = new_fig()
kline(ax, 0, 8.5, 10.0, 10.1, 8.4)
kline(ax, 1, 10.1, 8.2, 10.2, 8.1)
set_lim(ax, [0, 1], [8.1, 10.2])
save(fig, 'v7o-16.png')

# v7o-17 穿头破脚（天狗吞吃）：阳线 + 阴线完全吞没
fig, ax = new_fig()
kline(ax, 0, 8.5, 9.8, 9.9, 8.4)
kline(ax, 1, 10.0, 8.2, 10.1, 8.1)
set_lim(ax, [0, 1], [8.1, 10.1])
save(fig, 'v7o-17.png')

# ============ 三根K线见顶组合 ============

# v7o-18 升势停顿：两根阳线后第三根很短
fig, ax = new_fig()
kline(ax, 0, 8.0, 9.0, 9.1, 7.9)
kline(ax, 1, 9.1, 10.0, 10.1, 9.0)
kline(ax, 2, 10.0, 10.2, 10.4, 9.9)
set_lim(ax, [0, 1, 2], [7.9, 10.4])
save(fig, 'v7o-18.png')

# v7o-19 两黑夹一红
fig, ax = new_fig()
kline(ax, 0, 9.5, 10.0, 10.1, 9.4)
kline(ax, 1, 9.6, 9.9, 10.0, 9.5)
kline(ax, 2, 9.9, 9.3, 10.0, 9.2)
set_lim(ax, [0, 1, 2], [9.2, 10.1])
save(fig, 'v7o-19.png')

# v7o-20 下跌三连阴
fig, ax = new_fig()
kline(ax, 0, 10.0, 9.3, 10.1, 9.2)
kline(ax, 1, 9.3, 8.6, 9.4, 8.5)
kline(ax, 2, 8.6, 7.9, 8.7, 7.8)
set_lim(ax, [0, 1, 2], [7.8, 10.1])
save(fig, 'v7o-20.png')

# v7o-21 黄昏之星：阳线 + 小星 + 阴线
fig, ax = new_fig()
kline(ax, 0, 8.0, 9.8, 9.9, 7.9)
kline(ax, 1, 9.9, 10.0, 10.3, 9.7)
kline(ax, 2, 9.6, 8.5, 9.7, 8.4)
set_lim(ax, [0, 1, 2], [7.9, 10.3])
save(fig, 'v7o-21.png')

# ============ 三根以上K线见顶组合 ============

# v7o-22 平顶 普通型：两根K线最高价相同
fig, ax = new_fig()
kline(ax, 0, 9.0, 10.0, 10.5, 8.9)
kline(ax, 1, 9.8, 9.5, 10.5, 9.4)
set_lim(ax, [0, 1], [8.9, 10.5])
save(fig, 'v7o-22.png')

# v7o-23 平顶 增强型：多根K线最高价相同
fig, ax = new_fig()
kline(ax, 0, 9.0, 10.0, 10.5, 8.9)
kline(ax, 1, 9.9, 9.6, 10.5, 9.4)
kline(ax, 2, 9.6, 9.8, 10.5, 9.5)
kline(ax, 3, 9.7, 9.3, 10.5, 9.2)
set_lim(ax, [0, 1, 2, 3], [8.9, 10.5])
save(fig, 'v7o-23.png')

# v7o-24 塔形顶 普通型：大阳线后小阴小阳再大阴线
fig, ax = new_fig()
kline(ax, 0, 8.0, 10.0, 10.1, 7.9)
kline(ax, 1, 9.8, 9.6, 9.9, 9.5)
kline(ax, 2, 9.6, 9.7, 9.8, 9.5)
kline(ax, 3, 9.7, 9.4, 9.8, 9.3)
kline(ax, 4, 9.4, 7.8, 9.5, 7.7)
set_lim(ax, [0, 1, 2, 3, 4], [7.7, 10.1])
save(fig, 'v7o-24.png')

# v7o-25 塔形顶 增强型：左右两根大K线实体更长
fig, ax = new_fig()
kline(ax, 0, 7.5, 10.5, 10.6, 7.4)
kline(ax, 1, 10.3, 10.0, 10.4, 9.9)
kline(ax, 2, 10.0, 10.1, 10.3, 9.9)
kline(ax, 3, 10.1, 9.8, 10.2, 9.7)
kline(ax, 4, 9.8, 7.0, 9.9, 6.9)
set_lim(ax, [0, 1, 2, 3, 4], [6.9, 10.6])
save(fig, 'v7o-25.png')

# v7o-26 下跌不止形 普通型
fig, ax = new_fig()
kline(ax, 0, 10.0, 9.5, 10.1, 9.4)
kline(ax, 1, 9.6, 9.3, 9.7, 9.2)
kline(ax, 2, 9.4, 9.0, 9.5, 8.9)
kline(ax, 3, 9.1, 8.7, 9.2, 8.6)
kline(ax, 4, 8.8, 8.3, 8.9, 8.2)
set_lim(ax, [0, 1, 2, 3, 4], [8.2, 10.1])
save(fig, 'v7o-26.png')

# v7o-27 下跌不止形 增强型（全阴线、较陡）
fig, ax = new_fig()
kline(ax, 0, 10.5, 9.8, 10.6, 9.7)
kline(ax, 1, 9.8, 9.0, 9.9, 8.9)
kline(ax, 2, 9.0, 8.2, 9.1, 8.1)
kline(ax, 3, 8.2, 7.4, 8.3, 7.3)
kline(ax, 4, 7.4, 6.6, 7.5, 6.5)
set_lim(ax, [0, 1, 2, 3, 4], [6.5, 10.6])
save(fig, 'v7o-27.png')

# ============ 长十字线出现后风险评估示意图 ============

# v7o-28 可继续持股观望型①：长十字线后小阳线重心上移
fig, ax = new_fig()
kline(ax, 0, 9.0, 9.5, 9.6, 8.9)
kline(ax, 1, 9.6, 9.65, 10.8, 8.3)  # 长十字线
kline(ax, 2, 9.7, 10.2, 10.4, 9.6)
set_lim(ax, [0, 1, 2], [8.3, 10.8])
save(fig, 'v7o-28.png')

# v7o-29 可继续持股观望型②：长十字线后小阴线但重心未下移
fig, ax = new_fig()
kline(ax, 0, 9.0, 9.5, 9.6, 8.9)
kline(ax, 1, 9.6, 9.65, 10.8, 8.3)
kline(ax, 2, 9.6, 9.4, 9.8, 9.2)
set_lim(ax, [0, 1, 2], [8.3, 10.8])
save(fig, 'v7o-29.png')

# v7o-30 应马上停损离场型③：长十字线后一根大阴线
fig, ax = new_fig()
kline(ax, 0, 9.0, 9.5, 9.6, 8.9)
kline(ax, 1, 9.6, 9.65, 10.8, 8.3)
kline(ax, 2, 9.5, 7.8, 9.6, 7.7)
set_lim(ax, [0, 1, 2], [7.7, 10.8])
save(fig, 'v7o-30.png')

# v7o-31 应马上停损离场型④：在长十字线下影线末端处开盘
fig, ax = new_fig()
kline(ax, 0, 9.0, 9.5, 9.6, 8.9)
kline(ax, 1, 9.6, 9.65, 10.8, 8.3)
kline(ax, 2, 8.35, 8.0, 8.5, 7.9)
set_lim(ax, [0, 1, 2], [7.9, 10.8])
save(fig, 'v7o-31.png')

# v7o-32 应马上停损离场型⑤：跳空低开低走，当日阴线收盘
fig, ax = new_fig()
kline(ax, 0, 9.0, 9.5, 9.6, 8.9)
kline(ax, 1, 9.6, 9.65, 10.8, 8.3)
kline(ax, 2, 8.0, 7.2, 8.1, 7.1)
set_lim(ax, [0, 1, 2], [7.1, 10.8])
save(fig, 'v7o-32.png')

# ============ 高位大阳线见顶概率示意（表3） ============

# v7o-33 见顶概率1：大阳线后小阴线吞没1/3，>60%
fig, ax = new_fig()
kline(ax, 0, 8.0, 10.0, 10.1, 7.9)
kline(ax, 1, 9.9, 9.3, 10.0, 9.2)
set_lim(ax, [0, 1], [7.9, 10.1])
save(fig, 'v7o-33.png')

# v7o-34 见顶概率2：吞没1/2，>70%
fig, ax = new_fig()
kline(ax, 0, 8.0, 10.0, 10.1, 7.9)
kline(ax, 1, 9.9, 9.0, 10.0, 8.9)
set_lim(ax, [0, 1], [7.9, 10.1])
save(fig, 'v7o-34.png')

# v7o-35 见顶概率3：吞没2/3，>80%
fig, ax = new_fig()
kline(ax, 0, 8.0, 10.0, 10.1, 7.9)
kline(ax, 1, 9.9, 8.6, 10.0, 8.5)
set_lim(ax, [0, 1], [7.9, 10.1])
save(fig, 'v7o-35.png')

# v7o-36 见顶概率4：跌破大阳线开盘价，>90%
fig, ax = new_fig()
kline(ax, 0, 8.5, 10.0, 10.1, 8.4)
kline(ax, 1, 8.6, 7.8, 8.7, 7.7)
set_lim(ax, [0, 1], [7.7, 10.1])
save(fig, 'v7o-36.png')

# v7o-37 见顶概率5：左边图形（十字线在前），见顶排除
fig, ax = new_fig()
kline(ax, 0, 9.0, 9.05, 9.3, 8.7)
kline(ax, 1, 9.0, 10.0, 10.1, 8.9)
set_lim(ax, [0, 1], [8.7, 10.1])
save(fig, 'v7o-37.png')

# ============ 第二章 特殊K线见顶 ============

# v7o-38 高位高开低走放量大阴线（日K线示意）
fig, ax = new_fig()
# 前面一段上涨
for i, (o, c, h, l) in enumerate([(8.0,8.5,8.6,7.9),(8.6,9.0,9.1,8.5),(9.1,9.6,9.7,9.0),(9.7,10.2,10.3,9.6)]):
    kline(ax, i, o, c, h, l)
# 高位高开低走大阴线
kline(ax, 4, 10.6, 9.0, 10.7, 8.9)
set_lim(ax, list(range(5)), [7.9, 10.7])
save(fig, 'v7o-38.png')

# v7o-39 高位低开低走放量大阴线（日K线示意）
fig, ax = new_fig()
for i, (o, c, h, l) in enumerate([(8.0,8.5,8.6,7.9),(8.6,9.0,9.1,8.5),(9.1,9.6,9.7,9.0),(9.7,10.2,10.3,9.6)]):
    kline(ax, i, o, c, h, l)
# 高位低开低走大阴线（昨天阳线收盘10.2，今天低开）
kline(ax, 4, 9.8, 8.5, 9.9, 8.4)
set_lim(ax, list(range(5)), [7.9, 10.7])
save(fig, 'v7o-39.png')

# v7o-40 高位跌停一字线
fig, ax = new_fig()
for i, (o, c, h, l) in enumerate([(8.0,8.5,8.6,7.9),(8.6,9.0,9.1,8.5),(9.1,9.6,9.7,9.0),(9.7,10.2,10.3,9.6)]):
    kline(ax, i, o, c, h, l)
# 跌停一字线：开盘=收盘=最高=最低（跌停价）
ax.plot([4, 4], [9.2, 9.2], color=DOWN, linewidth=3)
set_lim(ax, list(range(5)), [7.9, 10.7])
save(fig, 'v7o-40.png')

# v7o-41 高位放量跳水当日分时出逃示意（第一/二/三卖出点）
fig, ax = plt.subplots(figsize=(5.5, 3.2), dpi=150)
fig.patch.set_facecolor('white')
ax.set_facecolor('white')
# 模拟分时走势线：先平后跳水再反弹
t = np.linspace(0, 100, 500)
price = 10.0 - 0.02*t
# 跳水段
jump_start = 30
jump_end = 42
mask1 = (t >= jump_start) & (t <= jump_end)
price[mask1] = 10.0 - (t[mask1]-jump_start)*0.18
# 反弹
mask2 = (t > jump_end) & (t <= 55)
price[mask2] = 10.0 - (jump_end-jump_start)*0.18 + (t[mask2]-jump_end)*0.06
# 二次跳水
mask3 = (t > 55) & (t <= 65)
price[mask3] = price[mask2][-1] - (t[mask3]-55)*0.12
# 第三反弹
mask4 = t > 65
price[mask4] = price[mask3][-1] + (t[mask4]-65)*0.02

ax.plot(t, price, color='#333333', linewidth=1.0)
# 昨日收盘价线
ax.axhline(y=10.0, color='#999999', linestyle='--', linewidth=0.8)
ax.text(99, 10.02, '昨日收盘价', fontsize=7, ha='right', color='#666666')
# -7%线
ax.axhline(y=9.3, color=DOWN, linestyle='--', linewidth=0.8)
ax.text(99, 9.32, '-7%', fontsize=7, ha='right', color=DOWN)
# 三个卖出点
p1x, p1y = 36, 10.0-(36-jump_start)*0.18
p2x, p2y = 55, price[(t>=jump_end)][-1]
p3x, p3y = 68, price[t>65][0]
for px, py, label, dx, dy in [(p1x,p1y,'第一出逃时间',2,-0.15),(p2x,p2y,'第二出逃时间',-12,0.25),(p3x,p3y,'第三出逃时间',-12,0.25)]:
    ax.plot(px, py, 'o', color=DOWN, markersize=5, zorder=5)
    ax.annotate(label, (px, py), xytext=(px+dx, py+dy), fontsize=7,
                arrowprops=dict(arrowstyle='->', color='#333333', lw=0.7), color='#333333')
ax.set_xlim(0, 100)
ax.axis('off')
save(fig, 'v7o-41.png')

print('=== ALL DONE ===')
