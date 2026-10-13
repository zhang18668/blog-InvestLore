# -*- coding: utf-8 -*-
"""Generate v2o-40~51: missing diagrams that were previously text-only descriptions."""
import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'SimHei', 'FangSong']
matplotlib.rcParams['axes.unicode_minus'] = False
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os

OUT = r"E:\生活\股票操练大全全套\stock-blog\source\images\kxian"

RED = '#FF4444'
GREEN = '#00AA00'
SHORT = '#E83838'
MID = '#FF8C00'
LONG = '#2E6BE6'

def draw_kline(ax, x, o, c, h, l, width=0.35):
    color = RED if c >= o else GREEN
    ax.plot([x, x], [l, h], color=color, linewidth=1.0, zorder=2)
    bottom = min(o, c); height = abs(c - o)
    if height < 1e-6: height = 0.3
    ax.add_patch(patches.Rectangle((x-width/2, bottom), width, height,
                 facecolor=color, edgecolor=color, linewidth=0.5, zorder=3))

def kline_from_close(ax, closes, width=0.45, seed=1):
    rng = np.random.RandomState(seed)
    for i, c in enumerate(closes):
        o = closes[i-1] if i > 0 else c - 0.3
        h = max(o, c) + abs(rng.normal(0, 0.4))
        l = min(o, c) - abs(rng.normal(0, 0.4))
        draw_kline(ax, i, o, c, h, l, width=width)

def ma(closes, n):
    return np.convolve(closes, np.ones(n)/n, mode='valid')

def style_ax(ax):
    ax.set_xticks([]); ax.set_yticks([])
    for s in ['top','right','left','bottom']: ax.spines[s].set_visible(False)

def save(fig, name):
    p = os.path.join(OUT, name)
    fig.savefig(p, bbox_inches='tight', facecolor='white', dpi=130)
    plt.close(fig)
    print("saved", name)

def plot_ma_lines(ax, closes, ns=(5,10,20)):
    n = len(closes)
    colors = [SHORT, MID, LONG]
    lstyles = ['-', '-.', '--']
    for idx, nn in enumerate(ns):
        m = ma(closes, nn)
        ax.plot(np.arange(nn-1, n), m, color=colors[idx], linewidth=1.5,
                linestyle=lstyles[idx], zorder=4)

def fig_ax(w=5.5, h=3.2):
    fig, ax = plt.subplots(figsize=(w, h), dpi=130)
    return fig, ax

# v2o-40 再次粘合向上发散形：先发散一次→粘合→再向上发散
np.random.seed(60)
n = 50
# 第一段小幅上升发散，第二段粘合横盘，第三段再次向上发散
base = np.concatenate([
    np.linspace(10, 13, 12),    # 第一次向上发散
    np.linspace(13, 13.2, 15),  # 粘合横盘
    np.linspace(13.2, 19, 23),  # 再次向上发散
])
closes = list(base + np.random.normal(0, 0.25, n))
fig, ax = fig_ax()
kline_from_close(ax, closes, 0.4, seed=60)
plot_ma_lines(ax, closes)
style_ax(ax)
save(fig, 'v2o-40.png')

# v2o-41 再次粘合向下发散形
base = np.concatenate([
    np.linspace(19, 16, 12),
    np.linspace(16, 15.8, 15),
    np.linspace(15.8, 10, 23),
])
closes = list(base + np.random.normal(0, 0.25, n))
fig, ax = fig_ax()
kline_from_close(ax, closes, 0.4, seed=61)
plot_ma_lines(ax, closes)
style_ax(ax)
save(fig, 'v2o-41.png')

# v2o-42 再次交叉向上发散形：先向下发散→收敛交叉→再向上发散
base = np.concatenate([
    np.linspace(13, 10, 12),    # 第一次向下发散
    np.linspace(10, 11, 13),    # 收敛交叉
    np.linspace(11, 17, 25),    # 再次向上发散
])
closes = list(base + np.random.normal(0, 0.25, n))
fig, ax = fig_ax()
kline_from_close(ax, closes, 0.4, seed=62)
plot_ma_lines(ax, closes)
style_ax(ax)
save(fig, 'v2o-42.png')

# v2o-43 再次交叉向下发散形
base = np.concatenate([
    np.linspace(10, 13, 12),
    np.linspace(13, 12, 13),
    np.linspace(12, 6, 25),
])
closes = list(base + np.random.normal(0, 0.25, n))
fig, ax = fig_ax()
kline_from_close(ax, closes, 0.4, seed=63)
plot_ma_lines(ax, closes)
style_ax(ax)
save(fig, 'v2o-43.png')

# v2o-44 快速上涨形：短期均线快速拉升，与中长期迅速拉开
np.random.seed(64)
n = 35
base = np.concatenate([
    np.linspace(10, 11, 20),   # 前期平缓
    np.linspace(11, 19, 15),    # 短期均线快速直线拉升
])
closes = list(base + np.random.normal(0, 0.3, n))
fig, ax = fig_ax()
kline_from_close(ax, closes, 0.4, seed=64)
plot_ma_lines(ax, closes)
style_ax(ax)
save(fig, 'v2o-44.png')

# v2o-45 快速下跌形
base = np.concatenate([
    np.linspace(19, 18, 20),
    np.linspace(18, 10, 15),
])
closes = list(base + np.random.normal(0, 0.3, n))
fig, ax = fig_ax()
kline_from_close(ax, closes, 0.4, seed=65)
plot_ma_lines(ax, closes)
style_ax(ax)
save(fig, 'v2o-45.png')

# v2o-46 烘云托月形：股价沿短中期均线略向上，长期均线在下方托着，整体横盘缓升
np.random.seed(66)
n = 35
base = np.concatenate([np.linspace(11, 12.5, n)]) + 0.5*np.sin(np.arange(n)/4.0)
closes = list(base + np.random.normal(0, 0.2, n))
fig, ax = fig_ax()
kline_from_close(ax, closes, 0.4, seed=66)
plot_ma_lines(ax, closes)
style_ax(ax)
save(fig, 'v2o-46.png')

# v2o-47 乌云密布形：股价沿短中期均线略向下，长期均线在上方压着
base = np.concatenate([np.linspace(13, 11.5, n)]) + 0.5*np.sin(np.arange(n)/4.0)
closes = list(base + np.random.normal(0, 0.2, n))
fig, ax = fig_ax()
kline_from_close(ax, closes, 0.4, seed=67)
plot_ma_lines(ax, closes)
style_ax(ax)
save(fig, 'v2o-47.png')

# v2o-48 上升趋势线被有效突破：股价跌破上升趋势线3%以上
np.random.seed(68)
n = 35
low_x = [4, 18]
low_y = [9, 13]
trend = np.array([low_y[0] + (low_y[1]-low_y[0])*i/(n-1) + 0.8*np.sin(i/2.5) for i in range(n)])
# 最后一段跌破趋势线
for i in range(25, n):
    trend[i] = trend[i] - (i-24)*0.35
closes = list(trend + np.random.normal(0, 0.15, n))
fig, ax = fig_ax()
kline_from_close(ax, closes, 0.45, seed=68)
# 上升趋势线（延伸）
xs = [0, n-1]
ys = [low_y[0] - (low_y[1]-low_y[0])*low_x[0]/(n-1),
      low_y[1] + (low_y[1]-low_y[0])*(n-1-low_x[1])/(n-1)]
ax.plot(xs, ys, color=LONG, linewidth=1.5, linestyle='-', zorder=5)
# 跌破点
bx = 25
by = low_y[0] + (low_y[1]-low_y[0])*(bx-low_x[0])/(low_x[1]-low_x[0])
ax.scatter([bx], [by], color='red', zorder=6, s=30)
ax.annotate('有效跌破', xy=(bx, by), xytext=(bx+3, by+2), fontsize=8,
            arrowprops=dict(arrowstyle='->', color='red'))
style_ax(ax)
save(fig, 'v2o-48.png')

# v2o-49 下降趋势线被有效突破
np.random.seed(69)
high_x = [4, 18]
high_y = [16, 12]
trend = np.array([high_y[0] + (high_y[1]-high_y[0])*i/(n-1) - 0.8*np.sin(i/2.5) for i in range(n)])
for i in range(25, n):
    trend[i] = trend[i] + (i-24)*0.35
closes = list(trend + np.random.normal(0, 0.15, n))
fig, ax = fig_ax()
kline_from_close(ax, closes, 0.45, seed=69)
xs = [0, n-1]
ys = [high_y[0] - (high_y[1]-high_y[0])*high_x[0]/(n-1),
      high_y[1] + (high_y[1]-high_y[0])*(n-1-high_x[1])/(n-1)]
ax.plot(xs, ys, color=GREEN, linewidth=1.5, linestyle='-', zorder=5)
bx = 25
by = high_y[0] + (high_y[1]-high_y[0])*(bx-high_x[0])/(high_x[1]-high_x[0])
ax.scatter([bx], [by], color='red', zorder=6, s=30)
ax.annotate('有效突破', xy=(bx, by), xytext=(bx+3, by-2), fontsize=8,
            arrowprops=dict(arrowstyle='->', color='red'))
style_ax(ax)
save(fig, 'v2o-49.png')

# v2o-50 新的上升趋势线：原上升趋势线被跌破，但股价不跌反升创新高，形成新的更陡上升线
np.random.seed(70)
n = 40
# 第一段缓升
trend = np.concatenate([np.linspace(9, 12, 15), np.linspace(12, 11.5, 5), np.linspace(11.5, 17, 20)])
closes = list(trend + np.random.normal(0, 0.2, n))
fig, ax = fig_ax()
kline_from_close(ax, closes, 0.45, seed=70)
# 原上升趋势线（虚线，被跌破）
ax.plot([0, 20], [9, 12.5], color='#AAAAAA', linewidth=1.3, linestyle='--', zorder=4)
# 新的上升趋势线（实线，更陡）
ax.plot([18, n-1], [11.5, 17.2], color=RED, linewidth=1.8, linestyle='-', zorder=5, label='新的上升趋势线')
ax.legend(loc='upper left', fontsize=7, frameon=False)
style_ax(ax)
save(fig, 'v2o-50.png')

# v2o-51 新的下降趋势线
trend = np.concatenate([np.linspace(17, 14, 15), np.linspace(14, 14.5, 5), np.linspace(14.5, 9, 20)])
closes = list(trend + np.random.normal(0, 0.2, n))
fig, ax = fig_ax()
kline_from_close(ax, closes, 0.45, seed=71)
ax.plot([0, 20], [17, 14.5], color='#AAAAAA', linewidth=1.3, linestyle='--', zorder=4)
ax.plot([18, n-1], [14.5, 8.8], color=GREEN, linewidth=1.8, linestyle='-', zorder=5, label='新的下降趋势线')
ax.legend(loc='upper right', fontsize=7, frameon=False)
style_ax(ax)
save(fig, 'v2o-51.png')

print("EXTRA V2 DONE")
