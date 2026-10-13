# -*- coding: utf-8 -*-
"""习题集 同花顺风格K线重绘图生成"""
import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'FangSong', 'SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
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

# ============ wbo-01 七字经：一看二慢三通过（上升趋势买入示意） ============
fig, ax = plt.subplots(figsize=(6, 3.5))
# 下跌后企稳，慢慢抬升
data = [
    (12, 11, 12.5, 10.5), (11, 10, 11.2, 9.5), (10, 9, 10.2, 8.5),
    (9, 8.5, 9.2, 8), (8.5, 8.8, 9.2, 8.2), (8.8, 9.2, 9.5, 8.6),
    (9.2, 9.8, 10.2, 9.0), (9.8, 10.5, 10.8, 9.6),
    (10.5, 11.2, 11.5, 10.3), (11.2, 12.0, 12.3, 11.0),
]
for i,(o,c,h,l) in enumerate(data):
    draw_kline(ax, i+1, o, c, h, l)
# 标注买点箭头
ax.annotate('买点', xy=(6.5, 9.0), xytext=(6.5, 7.0),
            fontsize=10, color='#CC0000', ha='center',
            arrowprops=dict(arrowstyle='->', color='#CC0000', lw=1.5))
setup_ax(ax, (0, 11), (7, 13))
ax.set_title('一看二慢三通过：跌透后企稳再分批吸纳', fontsize=11)
save(fig, 'wbo-01.png')

# ============ wbo-02 七字经：卖出口诀（高位见顶回落示意） ============
fig, ax = plt.subplots(figsize=(6, 3.5))
data = [
    (8, 9, 9.5, 7.8), (9, 10, 10.5, 8.8), (10, 11.5, 12, 9.8),
    (11.5, 13, 13.5, 11.3), (13, 14.5, 15, 12.8), (14.5, 15.5, 16, 14.2),
    (15.5, 15.0, 16.5, 14.5), (15.0, 13.0, 15.2, 12.5),
    (13.0, 11.5, 13.5, 11.0), (11.5, 10.0, 12.0, 9.5),
]
for i,(o,c,h,l) in enumerate(data):
    draw_kline(ax, i+1, o, c, h, l)
ax.annotate('卖点', xy=(7, 15.5), xytext=(7, 17.5),
            fontsize=10, color='#006600', ha='center',
            arrowprops=dict(arrowstyle='->', color='#006600', lw=1.5))
setup_ax(ax, (0, 11), (8, 18))
ax.set_title('卖出口诀：高位放量滞涨及时离场', fontsize=11)
save(fig, 'wbo-02.png')

# ============ wbo-03 赢家操作示例 第一步：长期下跌后见底 ============
fig, ax = plt.subplots(figsize=(6, 3.5))
np.random.seed(1)
base = 20
prices = []
p = base
for i in range(15):
    p -= np.random.uniform(0.2, 0.8)
    prices.append(p)
# 底部企稳
for i in range(5):
    prices.append(p + np.random.uniform(-0.1, 0.3))
for i, p in enumerate(prices):
    o = p - 0.3
    c = p + np.random.uniform(-0.2, 0.3)
    h = max(o, c) + 0.4
    l = min(o, c) - 0.4
    draw_kline(ax, i+1, o, c, h, l)
setup_ax(ax, (0, 22), (10, 22))
ax.set_title('第一步：长期下跌后逐步缩量企稳', fontsize=11)
save(fig, 'wbo-03.png')

# ============ wbo-04 赢家操作示例 第二步：底部横盘筑底 ============
fig, ax = plt.subplots(figsize=(6, 3.5))
np.random.seed(2)
p = 12
for i in range(20):
    o = p + np.random.uniform(-0.3, 0.3)
    c = o + np.random.uniform(-0.2, 0.2)
    h = max(o, c) + 0.25
    l = min(o, c) - 0.25
    draw_kline(ax, i+1, o, c, h, l)
    p = c
# 横盘区间线
ax.axhline(y=12.8, color='gray', linestyle='--', linewidth=1, alpha=0.6)
ax.axhline(y=11.2, color='gray', linestyle='--', linewidth=1, alpha=0.6)
setup_ax(ax, (0, 21), (10, 14))
ax.set_title('第二步：底部横盘震荡构筑长期底部', fontsize=11)
save(fig, 'wbo-04.png')

# ============ wbo-05 赢家操作示例 第三步：放量突破底部区间 ============
fig, ax = plt.subplots(figsize=(6, 3.5))
np.random.seed(3)
p = 12
for i in range(12):
    o = p + np.random.uniform(-0.2, 0.2)
    c = o + np.random.uniform(-0.15, 0.15)
    h = max(o, c) + 0.2
    l = min(o, c) - 0.2
    draw_kline(ax, i+1, o, c, h, l)
    p = c
# 突破大阳线
draw_kline(ax, 13, 12.8, 14.5, 14.8, 12.6)
draw_kline(ax, 14, 14.5, 15.2, 15.5, 14.3)
setup_ax(ax, (0, 15), (10.5, 16))
ax.set_title('第三步：放量长阳突破底部箱体上沿', fontsize=11)
save(fig, 'wbo-05.png')

# ============ wbo-06 赢家操作示例 第四步：上升途中回踩确认 ============
fig, ax = plt.subplots(figsize=(6, 3.5))
data = [
    (8, 9.5, 9.8, 7.8), (9.5, 11, 11.5, 9.3), (11, 12.5, 13, 10.8),
    (12.5, 14, 14.5, 12.3), (14, 15.5, 16, 13.8), (15.5, 15.0, 16.5, 14.5),
    (15.0, 13.5, 15.2, 13.0), (13.5, 14.0, 14.5, 13.2),
    (14.0, 15.5, 16, 13.8), (15.5, 17, 17.5, 15.3),
]
for i,(o,c,h,l) in enumerate(data):
    draw_kline(ax, i+1, o, c, h, l)
ax.annotate('回踩不破', xy=(7, 13.5), xytext=(7, 11.5),
            fontsize=9, color='#006600', ha='center',
            arrowprops=dict(arrowstyle='->', color='#006600', lw=1.2))
setup_ax(ax, (0, 11), (10, 18))
ax.set_title('第四步：上涨途中缩量回踩获支撑', fontsize=11)
save(fig, 'wbo-06.png')

# ============ wbo-07 赢家操作示例 第五步：主升浪加速 ============
fig, ax = plt.subplots(figsize=(6, 3.5))
prices = [(8,9),(9,10.5),(10.5,12),(12,14),(14,16.5),(16.5,19),(19,21.5)]
for i,(o,c) in enumerate(prices):
    draw_kline(ax, i+1, o, c, c+0.3, o-0.3)
setup_ax(ax, (0, 8), (7, 23))
ax.set_title('第五步：主升浪连续大阳向上攻击', fontsize=11)
save(fig, 'wbo-07.png')

# ============ wbo-08 赢家操作示例 第六步：高位放量滞涨 ============
fig, ax = plt.subplots(figsize=(6, 3.5))
data = [
    (8, 10, 10.5, 7.8), (10, 12, 12.5, 9.8), (12, 14, 14.5, 11.8),
    (14, 16, 16.5, 13.8), (16, 17, 17.5, 15.8), (17, 16.5, 18.5, 16),
    (16.5, 15, 17, 14.5), (15, 14, 15.5, 13.5),
]
for i,(o,c,h,l) in enumerate(data):
    draw_kline(ax, i+1, o, c, h, l)
setup_ax(ax, (0, 9), (12, 19))
ax.set_title('第六步：高位放量长上影滞涨信号', fontsize=11)
save(fig, 'wbo-08.png')

# ============ wbo-09 赢家操作示例 第七步：破位下跌离场 ============
fig, ax = plt.subplots(figsize=(6, 3.5))
data = [
    (16, 17, 17.5, 15.8), (17, 16.5, 18, 16), (16.5, 15, 17, 14.5),
    (15, 13, 15.5, 12.5), (13, 11, 13.5, 10.5), (11, 9, 11.5, 8.5),
    (9, 7, 9.5, 6.5),
]
for i,(o,c,h,l) in enumerate(data):
    draw_kline(ax, i+1, o, c, h, l)
ax.annotate('破位离场', xy=(4, 13), xytext=(4, 19),
            fontsize=10, color='#006600', ha='center',
            arrowprops=dict(arrowstyle='->', color='#006600', lw=1.5))
setup_ax(ax, (0, 8), (5, 20))
ax.set_title('第七步：有效跌破颈线果断清仓', fontsize=11)
save(fig, 'wbo-09.png')

# ============ wbo-10 填空题示例：底部锤头线买入 ============
fig, axes = plt.subplots(1, 2, figsize=(7, 3.5))
# 题目图
ax = axes[0]
for i,(o,c,h,l) in enumerate([(15,14,15.2,12),(14,13,14.2,11),(13,12,13.2,10.5)]):
    draw_kline(ax, i+1, o, c, h, l)
draw_kline(ax, 4, 11, 11.5, 11.8, 9)  # 锤头线
setup_ax(ax, (0, 5), (8.5, 16))
ax.set_title('题目：锤头线出现后应？', fontsize=10)
# 答案图
ax = axes[1]
for i,(o,c,h,l) in enumerate([(15,14,15.2,12),(14,13,14.2,11),(13,12,13.2,10.5)]):
    draw_kline(ax, i+1, o, c, h, l)
draw_kline(ax, 4, 11, 11.5, 11.8, 9)
draw_kline(ax, 5, 11.5, 13, 13.5, 11.3)
draw_kline(ax, 6, 13, 14.5, 15, 12.8)
setup_ax(ax, (0, 7), (8.5, 16))
ax.set_title('答案：见底信号，应买进', fontsize=10)
save(fig, 'wbo-10.png')

# ============ wbo-11 填空题示例：乌云盖顶卖出 ============
fig, axes = plt.subplots(1, 2, figsize=(7, 3.5))
ax = axes[0]
draw_kline(ax, 1, 8, 12, 12.5, 7.5)
draw_kline(ax, 2, 12.5, 9, 13, 8.5)
setup_ax(ax, (0, 3), (7, 13.5))
ax.set_title('题目：乌云盖顶后应？', fontsize=10)
ax = axes[1]
draw_kline(ax, 1, 8, 12, 12.5, 7.5)
draw_kline(ax, 2, 12.5, 9, 13, 8.5)
draw_kline(ax, 3, 9, 7, 9.5, 6.5)
draw_kline(ax, 4, 7, 5.5, 7.5, 5)
setup_ax(ax, (0, 5), (4.5, 13.5))
ax.set_title('答案：见顶信号，应卖出', fontsize=10)
save(fig, 'wbo-11.png')

# ============ wbo-12 填空题示例：头肩底突破 ============
fig, axes = plt.subplots(1, 2, figsize=(7, 3.5))
# 头肩底
ax = axes[0]
xs = [1,2,3,4,5,6,7,8,9,10,11,12]
ys = [10, 9, 8, 9, 7, 8, 9, 8, 7, 8, 9, 10]
for i, (x, y) in enumerate(zip(xs, ys)):
    o = y + 0.15
    c = y - 0.15
    h = y + 0.35
    l = y - 0.35
    draw_kline(ax, x, o, c, h, l)
# 颈线
ax.plot([3, 9], [9.2, 9.2], 'k--', linewidth=1.2, alpha=0.6)
setup_ax(ax, (0, 13), (6, 11))
ax.set_title('题目：头肩底颈线突破应？', fontsize=10)
ax = axes[1]
for i, (x, y) in enumerate(zip(xs, ys)):
    o = y + 0.15
    c = y - 0.15
    h = y + 0.35
    l = y - 0.35
    draw_kline(ax, x, o, c, h, l)
ax.plot([3, 9], [9.2, 9.2], 'k--', linewidth=1.2, alpha=0.6)
# 突破后上涨
draw_kline(ax, 13, 9.5, 11, 11.5, 9.3)
draw_kline(ax, 14, 11, 12.5, 13, 10.8)
draw_kline(ax, 15, 12.5, 14, 14.5, 12.3)
setup_ax(ax, (0, 16), (6, 15))
ax.set_title('答案：放量突破颈线，买进', fontsize=10)
save(fig, 'wbo-12.png')

# ============ wbo-13 填空题示例：头肩顶跌破 ============
fig, axes = plt.subplots(1, 2, figsize=(7, 3.5))
ax = axes[0]
xs = list(range(1, 13))
ys = [5, 6, 7, 6, 8, 7, 6, 7, 8, 7, 6, 5]
for x, y in zip(xs, ys):
    o = y - 0.15
    c = y + 0.15
    h = y + 0.35
    l = y - 0.35
    draw_kline(ax, x, o, c, h, l)
ax.plot([3, 9], [5.8, 5.8], 'k--', linewidth=1.2, alpha=0.6)
setup_ax(ax, (0, 13), (4, 9))
ax.set_title('题目：头肩顶颈线跌破应？', fontsize=10)
ax = axes[1]
for x, y in zip(xs, ys):
    o = y - 0.15
    c = y + 0.15
    h = y + 0.35
    l = y - 0.35
    draw_kline(ax, x, o, c, h, l)
ax.plot([3, 9], [5.8, 5.8], 'k--', linewidth=1.2, alpha=0.6)
draw_kline(ax, 13, 5.5, 4, 5.8, 3.5)
draw_kline(ax, 14, 4, 2.5, 4.5, 2)
draw_kline(ax, 15, 2.5, 1, 3, 0.5)
setup_ax(ax, (0, 16), (0, 9))
ax.set_title('答案：有效跌破颈线，卖出', fontsize=10)
save(fig, 'wbo-13.png')

# ============ wbo-14 填空题示例：上升三角形突破 ============
fig, axes = plt.subplots(1, 2, figsize=(7, 3.5))
ax = axes[0]
np.random.seed(5)
p = 10
for i in range(15):
    o = p + np.random.uniform(-0.2, 0.2)
    c = o + np.random.uniform(-0.1, 0.25)
    h = max(o, c) + 0.2
    l = min(o, c) - 0.2
    draw_kline(ax, i+1, o, c, h, l)
    p = c
# 水平阻力线
ax.axhline(y=11.8, color='gray', linestyle='--', linewidth=1, alpha=0.6)
# 上升支撑线
ax.plot([1, 15], [9.2, 10.5], color='gray', linestyle='--', linewidth=1, alpha=0.6)
setup_ax(ax, (0, 16), (8.5, 12.5))
ax.set_title('题目：上升三角形末端应？', fontsize=10)
ax = axes[1]
p = 10
for i in range(15):
    o = p + np.random.uniform(-0.2, 0.2)
    c = o + np.random.uniform(-0.1, 0.25)
    h = max(o, c) + 0.2
    l = min(o, c) - 0.2
    draw_kline(ax, i+1, o, c, h, l)
    p = c
ax.axhline(y=11.8, color='gray', linestyle='--', linewidth=1, alpha=0.6)
ax.plot([1, 15], [9.2, 10.5], color='gray', linestyle='--', linewidth=1, alpha=0.6)
# 突破
draw_kline(ax, 16, 11.8, 13.5, 14, 11.6)
draw_kline(ax, 17, 13.5, 15, 15.5, 13.3)
setup_ax(ax, (0, 18), (8.5, 16))
ax.set_title('答案：向上突破，买进做多', fontsize=10)
save(fig, 'wbo-14.png')

# ============ wbo-15 填空题示例：下降三角形跌破 ============
fig, axes = plt.subplots(1, 2, figsize=(7, 3.5))
ax = axes[0]
np.random.seed(6)
p = 12
for i in range(15):
    o = p + np.random.uniform(-0.2, 0.2)
    c = o + np.random.uniform(-0.25, 0.1)
    h = max(o, c) + 0.2
    l = min(o, c) - 0.2
    draw_kline(ax, i+1, o, c, h, l)
    p = c
ax.axhline(y=9.5, color='gray', linestyle='--', linewidth=1, alpha=0.6)
ax.plot([1, 15], [13, 10.5], color='gray', linestyle='--', linewidth=1, alpha=0.6)
setup_ax(ax, (0, 16), (8.5, 14))
ax.set_title('题目：下降三角形末端应？', fontsize=10)
ax = axes[1]
p = 12
for i in range(15):
    o = p + np.random.uniform(-0.2, 0.2)
    c = o + np.random.uniform(-0.25, 0.1)
    h = max(o, c) + 0.2
    l = min(o, c) - 0.2
    draw_kline(ax, i+1, o, c, h, l)
    p = c
ax.axhline(y=9.5, color='gray', linestyle='--', linewidth=1, alpha=0.6)
ax.plot([1, 15], [13, 10.5], color='gray', linestyle='--', linewidth=1, alpha=0.6)
draw_kline(ax, 16, 9.5, 8, 9.7, 7.5)
draw_kline(ax, 17, 8, 6.5, 8.2, 6)
setup_ax(ax, (0, 18), (5.5, 14))
ax.set_title('答案：向下跌破，卖出做空', fontsize=10)
save(fig, 'wbo-15.png')

# ============ wbo-16 填空题示例：圆底买入 ============
fig, axes = plt.subplots(1, 2, figsize=(7, 3.5))
ax = axes[0]
xs = np.arange(12)
ys = 14 - 0.15*(xs-5)**2 + 8
for i, y in enumerate(ys):
    o = y + 0.2
    c = y - 0.2
    h = y + 0.4
    l = y - 0.4
    draw_kline(ax, i+1, o, c, h, l)
setup_ax(ax, (0, 13), (7, 15))
ax.set_title('题目：圆底形态完成应？', fontsize=10)
ax = axes[1]
for i, y in enumerate(ys):
    o = y + 0.2
    c = y - 0.2
    h = y + 0.4
    l = y - 0.4
    draw_kline(ax, i+1, o, c, h, l)
draw_kline(ax, 13, 10.5, 12, 12.5, 10.3)
draw_kline(ax, 14, 12, 13.5, 14, 11.8)
setup_ax(ax, (0, 15), (7, 15))
ax.set_title('答案：圆底完成后买进', fontsize=10)
save(fig, 'wbo-16.png')

# ============ wbo-17 填空题示例：圆顶卖出 ============
fig, axes = plt.subplots(1, 2, figsize=(7, 3.5))
ax = axes[0]
xs = np.arange(12)
ys = 8 + 0.15*(xs-5)**2 + 4
for i, y in enumerate(ys):
    o = y - 0.2
    c = y + 0.2
    h = y + 0.4
    l = y - 0.4
    draw_kline(ax, i+1, o, c, h, l)
setup_ax(ax, (0, 13), (7, 15))
ax.set_title('题目：圆顶形态完成应？', fontsize=10)
ax = axes[1]
for i, y in enumerate(ys):
    o = y - 0.2
    c = y + 0.2
    h = y + 0.4
    l = y - 0.4
    draw_kline(ax, i+1, o, c, h, l)
draw_kline(ax, 13, 12.5, 11, 12.7, 10.5)
draw_kline(ax, 14, 11, 9.5, 11.2, 9)
setup_ax(ax, (0, 15), (7, 15))
ax.set_title('答案：圆顶完成后卖出', fontsize=10)
save(fig, 'wbo-17.png')

# ============ wbo-18 选择题示例：MA均线金叉死叉 ============
fig, axes = plt.subplots(1, 2, figsize=(7, 3.5))
ax = axes[0]
np.random.seed(7)
p = 10
closes = []
for i in range(20):
    o = p + np.random.uniform(-0.3, 0.3)
    c = o + np.random.uniform(-0.2, 0.4)
    h = max(o, c) + 0.3
    l = min(o, c) - 0.3
    draw_kline(ax, i+1, o, c, h, l)
    closes.append(c)
    p = c
# MA5
ma5 = [np.mean(closes[max(0,i-4):i+1]) for i in range(20)]
ax.plot(range(1,21), ma5, color='#FF4444', linewidth=1.2, label='MA5')
setup_ax(ax, (0, 21), (8, 13))
ax.set_title('金叉后应？', fontsize=10)
ax = axes[1]
p = 10
closes = []
for i in range(20):
    o = p + np.random.uniform(-0.3, 0.3)
    c = o + np.random.uniform(-0.4, 0.2)
    h = max(o, c) + 0.3
    l = min(o, c) - 0.3
    draw_kline(ax, i+1, o, c, h, l)
    closes.append(c)
    p = c
ma5 = [np.mean(closes[max(0,i-4):i+1]) for i in range(20)]
ax.plot(range(1,21), ma5, color='#FF4444', linewidth=1.2, label='MA5')
setup_ax(ax, (0, 21), (7, 12))
ax.set_title('死叉后应？', fontsize=10)
save(fig, 'wbo-18.png')

# ============ wbo-19 判断题示例：射击之星 ============
fig, axes = plt.subplots(1, 2, figsize=(7, 3.5))
ax = axes[0]
for i,(o,c,h,l) in enumerate([(8,9,9.5,7.8),(8.5,9.5,10,8),(9,10.5,11,8.5)]):
    draw_kline(ax, i+1, o, c, h, l)
draw_kline(ax, 4, 10.5, 10, 13.5, 9.8)
setup_ax(ax, (0, 5), (7.5, 14))
ax.set_title('射击之星：上影线越长越有参考价值', fontsize=9)
ax = axes[1]
for i,(o,c,h,l) in enumerate([(12,11,12.5,9),(11,10,11.5,8.5),(10,9.5,10.5,8)]):
    draw_kline(ax, i+1, o, c, h, l)
draw_kline(ax, 4, 9, 9.5, 12, 8.8)
setup_ax(ax, (0, 5), (8, 13))
ax.set_title('倒锤头线：下影线越长越有参考价值', fontsize=9)
save(fig, 'wbo-19.png')

# ============ wbo-20 简答题示例：上升趋势线买入 ============
fig, ax = plt.subplots(figsize=(6, 3.5))
np.random.seed(8)
p = 8
for i in range(18):
    o = p + np.random.uniform(-0.2, 0.2)
    c = o + np.random.uniform(0.0, 0.3)
    h = max(o, c) + 0.2
    l = min(o, c) - 0.2
    draw_kline(ax, i+1, o, c, h, l)
    p = c
# 上升趋势线
ax.plot([1, 18], [7.5, 13], color='#CC0000', linewidth=1.5, linestyle='-')
setup_ax(ax, (0, 19), (6.5, 14))
ax.set_title('上升趋势线：回档至线附近可买进', fontsize=11)
save(fig, 'wbo-20.png')

# ============ wbo-21 问答题示例：断头铡刀 ============
fig, ax = plt.subplots(figsize=(6, 3.5))
np.random.seed(9)
p = 10
closes = []
for i in range(15):
    o = p + np.random.uniform(-0.2, 0.2)
    c = o + np.random.uniform(0.0, 0.3)
    h = max(o, c) + 0.2
    l = min(o, c) - 0.2
    draw_kline(ax, i+1, o, c, h, l)
    closes.append(c)
    p = c
# 断头铡刀大阴线
draw_kline(ax, 16, 11.5, 9, 11.8, 8.5)
closes.append(9)
# 均线
ma5 = [np.mean(closes[max(0,i-4):i+1]) for i in range(16)]
ax.plot(range(1,17), ma5, color='#FF8800', linewidth=1, label='MA5')
setup_ax(ax, (0, 17), (8, 13))
ax.set_title('断头铡刀：一根大阴线吞吃多根均线，卖出信号', fontsize=10)
save(fig, 'wbo-21.png')

# ============ wbo-22 游艺会：K线组合识别图 ============
fig, axes = plt.subplots(2, 4, figsize=(9, 4.5))
# 平底
ax = axes[0][0]
draw_kline(ax, 1, 12, 8, 12.5, 7)
draw_kline(ax, 2, 9, 10, 10.5, 7)
setup_ax(ax, (0, 3), (6, 13))
ax.set_title('平底', fontsize=9)
# 好友反攻
ax = axes[0][1]
draw_kline(ax, 1, 12, 8, 12.5, 7.5)
draw_kline(ax, 2, 7, 8, 8.5, 6.5)
setup_ax(ax, (0, 3), (6, 13))
ax.set_title('好友反攻', fontsize=9)
# 曙光初现
ax = axes[0][2]
draw_kline(ax, 1, 12, 8, 12.5, 7.5)
draw_kline(ax, 2, 7.5, 10.5, 11, 7)
setup_ax(ax, (0, 3), (6, 13))
ax.set_title('曙光初现', fontsize=9)
# 旭日东升
ax = axes[0][3]
draw_kline(ax, 1, 12, 8, 12.5, 7.5)
draw_kline(ax, 2, 9, 13, 13.5, 8.5)
setup_ax(ax, (0, 3), (7, 14))
ax.set_title('旭日东升', fontsize=9)
# 平顶
ax = axes[1][0]
draw_kline(ax, 1, 8, 12, 13, 7.5)
draw_kline(ax, 2, 11, 10, 13, 9.5)
setup_ax(ax, (0, 3), (7, 14))
ax.set_title('平顶', fontsize=9)
# 淡友反攻
ax = axes[1][1]
draw_kline(ax, 1, 8, 12, 12.5, 7.5)
draw_kline(ax, 2, 13, 12, 13.5, 11.5)
setup_ax(ax, (0, 3), (7, 14))
ax.set_title('淡友反攻', fontsize=9)
# 乌云盖顶
ax = axes[1][2]
draw_kline(ax, 1, 8, 12, 12.5, 7.5)
draw_kline(ax, 2, 12.5, 9, 13, 8.5)
setup_ax(ax, (0, 3), (7, 13.5))
ax.set_title('乌云盖顶', fontsize=9)
# 倾盆大雨
ax = axes[1][3]
draw_kline(ax, 1, 8, 12, 12.5, 7.5)
draw_kline(ax, 2, 11, 7.5, 11.5, 7)
setup_ax(ax, (0, 3), (6, 13))
ax.set_title('倾盆大雨', fontsize=9)
fig.tight_layout()
save(fig, 'wbo-22.png')

# ============ wbo-23 游艺会：尽头线识别 ============
fig, axes = plt.subplots(1, 2, figsize=(7, 3.5))
ax = axes[0]
draw_kline(ax, 1, 8, 12, 14, 7.8)
draw_kline(ax, 2, 12.5, 12.8, 13.2, 12.3)
setup_ax(ax, (0, 3), (7, 15))
ax.set_title('涨势尽头线（顶部十字线移至上影线）', fontsize=9)
ax = axes[1]
draw_kline(ax, 1, 12, 8, 12.2, 6)
draw_kline(ax, 2, 7.5, 7.2, 7.7, 6.8)
setup_ax(ax, (0, 3), (5.5, 13))
ax.set_title('跌势尽头线（底部十字线移至下影线）', fontsize=9)
save(fig, 'wbo-23.png')

# ============ wbo-24 标准风险提示图：高位放量见顶 ============
fig, ax = plt.subplots(figsize=(6, 3.5))
np.random.seed(10)
p = 8
for i in range(20):
    o = p + np.random.uniform(-0.2, 0.2)
    c = o + np.random.uniform(-0.1, 0.35)
    h = max(o, c) + 0.25
    l = min(o, c) - 0.25
    draw_kline(ax, i+1, o, c, h, l)
    p = c
# 顶部长上影
draw_kline(ax, 21, p, p-0.3, p+2, p-0.5)
# 后续下跌
draw_kline(ax, 22, p-0.3, p-2, p, p-2.5)
draw_kline(ax, 23, p-2, p-4, p-1.5, p-4.5)
setup_ax(ax, (0, 24), (p-6, p+3))
ax.set_title('常见失败信号：高位放量长上影后破位', fontsize=10)
save(fig, 'wbo-24.png')

print("All workbook charts done!")
