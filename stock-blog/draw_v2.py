# -*- coding: utf-8 -*-
"""Regenerate all v2o-XX.png technical indicator diagrams (red-up / green-down, clean style)."""
import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'SimHei', 'FangSong']
matplotlib.rcParams['axes.unicode_minus'] = False
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os

OUT = r"E:\生活\股票操练大全全套\stock-blog\source\images\kxian"
os.makedirs(OUT, exist_ok=True)

RED = '#FF4444'
GREEN = '#00AA00'
SHORT = '#E83838'   # 短期均线 红色实线
MID = '#FF8C00'     # 中期均线 橙色点线
LONG = '#2E6BE6'    # 长期均线 蓝色虚线

def draw_kline(ax, x, o, c, h, l, width=0.35):
    color = RED if c >= o else GREEN
    ax.plot([x, x], [l, h], color=color, linewidth=1.0, zorder=2)
    bottom = min(o, c)
    height = abs(c - o)
    if height < 1e-6:
        height = 0.3
    rect = patches.Rectangle((x - width/2, bottom), width, height,
                             facecolor=color, edgecolor=color, linewidth=0.5, zorder=3)
    ax.add_patch(rect)

def kline_from_close(ax, closes, width=0.45, seed=1):
    rng = np.random.RandomState(seed)
    for i, c in enumerate(closes):
        o = closes[i-1] if i > 0 else c - 0.3
        h = max(o, c) + abs(rng.normal(0, 0.4))
        l = min(o, c) - abs(rng.normal(0, 0.4))
        draw_kline(ax, i, o, c, h, l, width=width)

def ma(closes, n):
    return np.convolve(closes, np.ones(n)/n, mode='valid')

def style_ax(ax, ymin=None, ymax=None):
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ['top', 'right', 'left', 'bottom']:
        ax.spines[s].set_visible(False)
    if ymin is not None and ymax is not None:
        ax.set_ylim(ymin, ymax)

def save(fig, name):
    p = os.path.join(OUT, name)
    fig.savefig(p, bbox_inches='tight', facecolor='white', dpi=130)
    plt.close(fig)
    print("saved", name)

def plot_ma_lines(ax, closes, n_short=5, n_mid=10, n_long=20):
    n = len(closes)
    ms = ma(closes, n_short)
    mm = ma(closes, n_mid)
    ml = ma(closes, n_long)
    ax.plot(np.arange(n_short-1, n), ms, color=SHORT, linewidth=1.5, linestyle='-', zorder=4)
    ax.plot(np.arange(n_mid-1, n), mm, color=MID, linewidth=1.5, linestyle='-.', zorder=4)
    ax.plot(np.arange(n_long-1, n), ml, color=LONG, linewidth=1.5, linestyle='--', zorder=4)

def fig_ax(w=5.5, h=3.2):
    fig, ax = plt.subplots(figsize=(w, h), dpi=130)
    return fig, ax

# ============ v2o-01  5日均线示意图 ============
np.random.seed(42)
n = 30
trend = np.concatenate([np.linspace(10, 13, 12), np.linspace(13, 11, 8), np.linspace(11, 16, 10)])
closes = list(trend + np.random.normal(0, 0.4, n))
fig, ax = fig_ax()
kline_from_close(ax, closes, 0.4, seed=2)
ms = ma(closes, 5)
ax.plot(np.arange(4, n), ms, color=SHORT, linewidth=1.8, zorder=4, label='5日均线')
ax.legend(loc='upper left', fontsize=8, frameon=False)
style_ax(ax)
save(fig, 'v2o-01.png')

# ============ v2o-02  多头排列 ============
np.random.seed(3)
n = 35
trend = np.linspace(10, 20, n)
closes = list(trend + np.random.normal(0, 0.5, n))
fig, ax = fig_ax()
kline_from_close(ax, closes, 0.4, seed=3)
plot_ma_lines(ax, closes)
style_ax(ax)
save(fig, 'v2o-02.png')

# ============ v2o-03  空头排列 ============
np.random.seed(4)
trend = np.linspace(20, 10, n)
closes = list(trend + np.random.normal(0, 0.5, n))
fig, ax = fig_ax()
kline_from_close(ax, closes, 0.4, seed=4)
plot_ma_lines(ax, closes)
style_ax(ax)
save(fig, 'v2o-03.png')

# ============ v2o-04  黄金交叉 ============
np.random.seed(5)
# 下跌后企稳回升，长期均线走平后向上
trend = np.concatenate([np.linspace(16, 10, 18), np.linspace(10, 15, 22)])
closes = list(trend + np.random.normal(0, 0.4, 40))
fig, ax = fig_ax()
kline_from_close(ax, closes, 0.4, seed=5)
# 画两条均线：短期(5日)上穿长期(15日)，长期均线后期向上
s5 = ma(closes, 5); s15 = ma(closes, 15)
ax.plot(np.arange(4, 40), s5, color=SHORT, linewidth=1.6, zorder=4, label='短期均线')
ax.plot(np.arange(14, 40), s15, color=LONG, linewidth=1.6, linestyle='--', zorder=4, label='长期均线')
# 找交叉点
for i in range(1, len(s5)):
    si = i + 4; li = i + 14
    if si < 40 and li < 40:
        if s5[i-1] <= s15[i-1] and s5[i] > s15[i]:
            ax.annotate('黄金交叉', xy=(si, s5[i]), xytext=(si+5, s5[i]-2.5),
                        fontsize=8, arrowprops=dict(arrowstyle='->', color='red'))
            break
style_ax(ax)
save(fig, 'v2o-04.png')

# ============ v2o-05  死亡交叉 ============
np.random.seed(6)
trend = np.concatenate([np.linspace(10, 16, 18), np.linspace(16, 10, 22)])
closes = list(trend + np.random.normal(0, 0.4, 40))
fig, ax = fig_ax()
kline_from_close(ax, closes, 0.4, seed=6)
s5 = ma(closes, 5); s15 = ma(closes, 15)
ax.plot(np.arange(4, 40), s5, color=SHORT, linewidth=1.6, zorder=4, label='短期均线')
ax.plot(np.arange(14, 40), s15, color=LONG, linewidth=1.6, linestyle='--', zorder=4, label='长期均线')
for i in range(1, len(s5)):
    si = i + 4; li = i + 14
    if si < 40 and li < 40:
        if s5[i-1] >= s15[i-1] and s5[i] < s15[i]:
            ax.annotate('死亡交叉', xy=(si, s5[i]), xytext=(si+5, s5[i]+2.5),
                        fontsize=8, arrowprops=dict(arrowstyle='->', color='green'))
            break
style_ax(ax)
save(fig, 'v2o-05.png')

# ============ v2o-06  银山谷 ============
# 3条均线在低位形成尖头向上的不规则三角形
np.random.seed(7)
trend = np.concatenate([np.linspace(14, 9, 15), np.linspace(9, 11, 8), np.linspace(11, 9.5, 6), np.linspace(9.5, 16, 16)])
closes = list(trend + np.random.normal(0, 0.35, 45))
fig, ax = fig_ax()
kline_from_close(ax, closes, 0.4, seed=7)
plot_ma_lines(ax, closes, 5, 10, 20)
ax.annotate('银山谷', xy=(17, 9.3), xytext=(22, 7.5), fontsize=8,
            arrowprops=dict(arrowstyle='->', color='black'))
style_ax(ax)
save(fig, 'v2o-06.png')

# ============ v2o-07  金山谷 ============
# 和银山谷类似，但位置更高，在银山谷之后
np.random.seed(8)
trend = np.concatenate([np.linspace(14, 9, 12), np.linspace(9, 12, 8), np.linspace(12, 10.5, 6), np.linspace(10.5, 18, 19)])
closes = list(trend + np.random.normal(0, 0.35, 45))
fig, ax = fig_ax()
kline_from_close(ax, closes, 0.4, seed=8)
plot_ma_lines(ax, closes, 5, 10, 20)
ax.annotate('金山谷', xy=(28, 10.8), xytext=(33, 8.5), fontsize=8,
            arrowprops=dict(arrowstyle='->', color='black'))
style_ax(ax)
save(fig, 'v2o-07.png')

# ============ v2o-08  死亡谷 ============
np.random.seed(9)
trend = np.concatenate([np.linspace(10, 15, 12), np.linspace(15, 12, 8), np.linspace(12, 13.5, 6), np.linspace(13.5, 8, 19)])
closes = list(trend + np.random.normal(0, 0.35, 45))
fig, ax = fig_ax()
kline_from_close(ax, closes, 0.4, seed=9)
plot_ma_lines(ax, closes, 5, 10, 20)
ax.annotate('死亡谷', xy=(28, 13.2), xytext=(33, 15.5), fontsize=8,
            arrowprops=dict(arrowstyle='->', color='black'))
style_ax(ax)
save(fig, 'v2o-08.png')

# ============ v2o-09  首次粘合向上发散 ============
# 均线长期粘合（横盘），然后突然向上发散
np.random.seed(10)
n = 40
base = np.concatenate([np.full(20, 12), np.linspace(12, 18, 20)])
closes = list(base + np.random.normal(0, 0.25, n))
fig, ax = fig_ax()
kline_from_close(ax, closes, 0.4, seed=10)
plot_ma_lines(ax, closes, 5, 10, 20)
style_ax(ax)
save(fig, 'v2o-09.png')

# ============ v2o-10  首次粘合向下发散 ============
np.random.seed(11)
base = np.concatenate([np.full(20, 12), np.linspace(12, 6, 20)])
closes = list(base + np.random.normal(0, 0.25, n))
fig, ax = fig_ax()
kline_from_close(ax, closes, 0.4, seed=11)
plot_ma_lines(ax, closes, 5, 10, 20)
style_ax(ax)
save(fig, 'v2o-10.png')

# ============ v2o-11  上山爬坡形 ============
np.random.seed(12)
n = 35
trend = np.linspace(10, 17, n)
closes = list(trend + np.random.normal(0, 0.3, n))
fig, ax = fig_ax()
kline_from_close(ax, closes, 0.4, seed=12)
plot_ma_lines(ax, closes, 5, 10, 20)
style_ax(ax)
save(fig, 'v2o-11.png')

# ============ v2o-12  下山滑坡形 ============
np.random.seed(13)
trend = np.linspace(17, 10, n)
closes = list(trend + np.random.normal(0, 0.3, n))
fig, ax = fig_ax()
kline_from_close(ax, closes, 0.4, seed=13)
plot_ma_lines(ax, closes, 5, 10, 20)
style_ax(ax)
save(fig, 'v2o-12.png')

# ============ v2o-13  逐浪上升形 ============
# 短期中期均线多次交叉，长期均线托着向上
np.random.seed(14)
n = 40
base = np.zeros(n)
v = 10
for i in range(n):
    v += 0.15 + 0.8 * np.sin(i / 3.0)
    base[i] = v
closes = list(base + np.random.normal(0, 0.25, n))
fig, ax = fig_ax()
kline_from_close(ax, closes, 0.4, seed=14)
plot_ma_lines(ax, closes, 5, 10, 20)
style_ax(ax)
save(fig, 'v2o-13.png')

# ============ v2o-14  逐浪下降形 ============
np.random.seed(15)
base = np.zeros(n)
v = 17
for i in range(n):
    v -= 0.15 + 0.8 * np.sin(i / 3.0)
    base[i] = v
closes = list(base + np.random.normal(0, 0.25, n))
fig, ax = fig_ax()
kline_from_close(ax, closes, 0.4, seed=15)
plot_ma_lines(ax, closes, 5, 10, 20)
style_ax(ax)
save(fig, 'v2o-14.png')

# ============ v2o-15  加速上涨形 ============
# 前期缓慢上升，后期加速
np.random.seed(16)
n = 35
trend = np.concatenate([np.linspace(10, 12, 20), np.linspace(12, 20, 15)])
closes = list(trend + np.random.normal(0, 0.3, n))
fig, ax = fig_ax()
kline_from_close(ax, closes, 0.4, seed=16)
plot_ma_lines(ax, closes, 5, 10, 20)
style_ax(ax)
save(fig, 'v2o-15.png')

# ============ v2o-16  加速下跌形 ============
np.random.seed(17)
trend = np.concatenate([np.linspace(20, 18, 20), np.linspace(18, 10, 15)])
closes = list(trend + np.random.normal(0, 0.3, n))
fig, ax = fig_ax()
kline_from_close(ax, closes, 0.4, seed=17)
plot_ma_lines(ax, closes, 5, 10, 20)
style_ax(ax)
save(fig, 'v2o-16.png')

# ============ v2o-17  蛟龙出海 ============
# 横盘后一根大阳线同时上穿3条均线
np.random.seed(18)
n = 25
base = np.full(n, 12.0)
closes = list(base + np.random.normal(0, 0.2, n))
closes[-1] = 14.5  # 最后一根大阳线
fig, ax = fig_ax()
kline_from_close(ax, closes, 0.45, seed=18)
plot_ma_lines(ax, closes, 5, 10, 15)
ax.annotate('大阳线', xy=(n-1, 14.5), xytext=(n-8, 15.5), fontsize=8,
            arrowprops=dict(arrowstyle='->', color='red'))
style_ax(ax)
save(fig, 'v2o-17.png')

# ============ v2o-18  断头铡刀 ============
np.random.seed(19)
base = np.full(n, 12.0)
closes = list(base + np.random.normal(0, 0.2, n))
closes[-1] = 9.5  # 最后一根大阴线
fig, ax = fig_ax()
kline_from_close(ax, closes, 0.45, seed=19)
plot_ma_lines(ax, closes, 5, 10, 15)
ax.annotate('大阴线', xy=(n-1, 9.5), xytext=(n-8, 8.2), fontsize=8,
            arrowprops=dict(arrowstyle='->', color='green'))
style_ax(ax)
save(fig, 'v2o-18.png')

# ============ v2o-19  上升趋势线（支撑线） ============
np.random.seed(20)
n = 30
low_x = [4, 18]
low_y = [9, 13]
trend = np.array([low_y[0] + (low_y[1]-low_y[0])*i/(n-1) + 1.0*np.sin(i/2.5) for i in range(n)])
closes = list(trend + np.random.normal(0, 0.2, n))
fig, ax = fig_ax()
kline_from_close(ax, closes, 0.45, seed=20)
ax.plot([0, n-1], [low_y[0] - (low_y[1]-low_y[0])*low_x[0]/(n-1),
                    low_y[1] + (low_y[1]-low_y[0])*(n-1-low_x[1])/(n-1)],
        color=LONG, linewidth=1.5, linestyle='-', zorder=5)
style_ax(ax)
save(fig, 'v2o-19.png')

# ============ v2o-20  下降趋势线（压力线） ============
np.random.seed(21)
high_x = [4, 18]
high_y = [16, 12]
trend = np.array([high_y[0] + (high_y[1]-high_y[0])*i/(n-1) - 1.0*np.sin(i/2.5) for i in range(n)])
closes = list(trend + np.random.normal(0, 0.2, n))
fig, ax = fig_ax()
kline_from_close(ax, closes, 0.45, seed=21)
ax.plot([0, n-1], [high_y[0] - (high_y[1]-high_y[0])*high_x[0]/(n-1),
                    high_y[1] + (high_y[1]-high_y[0])*(n-1-high_x[1])/(n-1)],
        color=GREEN, linewidth=1.5, linestyle='-', zorder=5)
style_ax(ax)
save(fig, 'v2o-20.png')

# ============ v2o-21  慢速上升趋势线 ============
# 慢速（长周期）上升线平缓
np.random.seed(22)
n = 30
trend = np.linspace(10, 15, n) + 0.8*np.sin(np.arange(n)/3.0)
closes = list(trend + np.random.normal(0, 0.25, n))
fig, ax = fig_ax()
kline_from_close(ax, closes, 0.45, seed=22)
# 慢速上升线（长实线，平缓）
ax.plot([0, n-1], [10, 15], color=LONG, linewidth=1.8, linestyle='-', zorder=5, label='慢速上升趋势线')
ax.legend(loc='upper left', fontsize=7, frameon=False)
style_ax(ax)
save(fig, 'v2o-21.png')

# ============ v2o-22  慢速下降趋势线 ============
np.random.seed(23)
trend = np.linspace(15, 10, n) + 0.8*np.sin(np.arange(n)/3.0)
closes = list(trend + np.random.normal(0, 0.25, n))
fig, ax = fig_ax()
kline_from_close(ax, closes, 0.45, seed=23)
ax.plot([0, n-1], [15, 10], color=LONG, linewidth=1.8, linestyle='-', zorder=5, label='慢速下降趋势线')
ax.legend(loc='upper right', fontsize=7, frameon=False)
style_ax(ax)
save(fig, 'v2o-22.png')

# ============ v2o-23  快速上升趋势线（在慢速上升中） ============
np.random.seed(24)
trend = np.linspace(10, 15, n) + 1.2*np.sin(np.arange(n)/2.0)
closes = list(trend + np.random.normal(0, 0.2, n))
fig, ax = fig_ax()
kline_from_close(ax, closes, 0.45, seed=24)
# 慢速线（浅色虚线）
ax.plot([0, n-1], [10, 15], color='#AAAAAA', linewidth=1.2, linestyle='--', zorder=4)
# 快速线（红色实线，短期低点连线，更陡）
ax.plot([8, 22], [10.5, 14.5], color=RED, linewidth=1.8, linestyle='-', zorder=5, label='快速上升趋势线')
ax.legend(loc='upper left', fontsize=7, frameon=False)
style_ax(ax)
save(fig, 'v2o-23.png')

# ============ v2o-24  快速下降趋势线 ============
np.random.seed(25)
trend = np.linspace(15, 10, n) + 1.2*np.sin(np.arange(n)/2.0)
closes = list(trend + np.random.normal(0, 0.2, n))
fig, ax = fig_ax()
kline_from_close(ax, closes, 0.45, seed=25)
ax.plot([0, n-1], [15, 10], color='#AAAAAA', linewidth=1.2, linestyle='--', zorder=4)
ax.plot([8, 22], [14.5, 10.5], color=GREEN, linewidth=1.8, linestyle='-', zorder=5, label='快速下降趋势线')
ax.legend(loc='upper right', fontsize=7, frameon=False)
style_ax(ax)
save(fig, 'v2o-24.png')

# ============ 成交量图 helper ============
def vol_chart(volumes, closes, name, seed=30):
    n = len(volumes)
    fig, ax = plt.subplots(figsize=(5.5, 2.2), dpi=130)
    colors = [RED if closes[i] >= (closes[i-1] if i > 0 else closes[i]) else GREEN for i in range(n)]
    ax.bar(range(n), volumes, color=colors, width=0.6)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ['top', 'right', 'left', 'bottom']:
        ax.spines[s].set_visible(False)
    save(fig, name)

# v2o-25 逐渐放量
np.random.seed(31)
n = 20
v = np.linspace(10, 40, n) + np.random.normal(0, 2, n)
c = np.linspace(10, 14, n) + np.random.normal(0, 0.2, n)
vol_chart(list(v), list(c), 'v2o-25.png', seed=31)

# v2o-26 逐渐缩量
v = np.linspace(40, 10, n) + np.random.normal(0, 2, n)
c = np.linspace(14, 10, n) + np.random.normal(0, 0.2, n)
vol_chart(list(v), list(c), 'v2o-26.png', seed=32)

# v2o-27 快速放大量（连续小量后突然大量）
v = np.concatenate([np.full(10, 10) + np.random.normal(0, 1, 10), [45, 50, 48], np.full(7, 12) + np.random.normal(0, 1, 7)])
c = np.linspace(10, 12, n)
vol_chart(list(v), list(c), 'v2o-27.png', seed=33)

# v2o-28 快速出小量（连续大量后突然小量）
v = np.concatenate([np.full(10, 40) + np.random.normal(0, 2, 10), [8, 6, 10], np.full(7, 35) + np.random.normal(0, 2, 7)])
c = np.linspace(12, 10, n)
vol_chart(list(v), list(c), 'v2o-28.png', seed=34)

# v2o-29 量平
v = np.full(n, 25) + np.random.normal(0, 1.5, n)
c = np.linspace(11, 11.5, n)
vol_chart(list(v), list(c), 'v2o-29.png', seed=35)

# ============ MACD helper ============
def ema(data, n):
    k = 2.0 / (n + 1)
    out = [data[0]]
    for v in data[1:]:
        out.append(out[-1] + k * (v - out[-1]))
    return out

def macd_lines(closes):
    e12 = ema(closes, 12)
    e26 = ema(closes, 26)
    dif = [(e12[i] - e26[i]) * 3 for i in range(len(closes))]
    dea = ema(dif, 9)
    return dif, dea

def macd_chart(dif, dea, name, annotate=None):
    n = len(dif)
    fig, ax = plt.subplots(figsize=(5.5, 2.8), dpi=130)
    ax.axhline(0, color='black', linewidth=0.8)
    # bars
    for i in range(n):
        bh = dif[i] - dea[i]
        c = RED if bh >= 0 else GREEN
        ax.bar(i, bh, bottom=0, color=c, width=0.6, alpha=0.7, zorder=2)
    ax.plot(range(n), dif, color='black', linewidth=1.3, zorder=4, label='DIF')
    ax.plot(range(n), dea, color=MID, linewidth=1.3, zorder=4, label='DEA')
    ax.set_xticks([]); ax.set_yticks([])
    for s in ['top', 'right', 'left', 'bottom']:
        ax.spines[s].set_visible(False)
    if annotate:
        annotate(ax, dif, dea)
    save(fig, name)

# v2o-30 MACD上穿O轴
np.random.seed(40)
n = 50
price = np.concatenate([np.linspace(12, 9, 20), np.linspace(9, 14, 30)])
closes = list(price + np.random.normal(0, 0.2, n))
dif, dea = macd_lines(closes)
def annotate_cross_zero_up(ax, dif, dea):
    for i in range(1, n):
        if dif[i-1] <= 0 and dif[i] > 0:
            ax.annotate('上穿O轴', xy=(i, dif[i]), xytext=(i+5, dif[i]+0.8),
                        fontsize=8, arrowprops=dict(arrowstyle='->', color='red'))
            break
macd_chart(dif, dea, 'v2o-30.png', annotate_cross_zero_up)

# v2o-31 MACD下穿O轴
np.random.seed(41)
price = np.concatenate([np.linspace(9, 14, 20), np.linspace(14, 9, 30)])
closes = list(price + np.random.normal(0, 0.2, n))
dif, dea = macd_lines(closes)
def annotate_cross_zero_dn(ax, dif, dea):
    for i in range(1, n):
        if dif[i-1] >= 0 and dif[i] < 0:
            ax.annotate('下穿O轴', xy=(i, dif[i]), xytext=(i+5, dif[i]-1.0),
                        fontsize=8, arrowprops=dict(arrowstyle='->', color='green'))
            break
macd_chart(dif, dea, 'v2o-31.png', annotate_cross_zero_dn)

# v2o-32 MACD黄金交叉
np.random.seed(42)
price = np.concatenate([np.linspace(14, 10, 20), np.linspace(10, 13, 30)])
closes = list(price + np.random.normal(0, 0.2, n))
dif, dea = macd_lines(closes)
def annotate_golden(ax, dif, dea):
    for i in range(1, n):
        if dif[i-1] <= dea[i-1] and dif[i] > dea[i]:
            ax.annotate('黄金交叉', xy=(i, dif[i]), xytext=(i+5, dif[i]+0.8),
                        fontsize=8, arrowprops=dict(arrowstyle='->', color='red'))
            break
macd_chart(dif, dea, 'v2o-32.png', annotate_golden)

# v2o-33 MACD死亡交叉
np.random.seed(43)
price = np.concatenate([np.linspace(10, 14, 20), np.linspace(14, 11, 30)])
closes = list(price + np.random.normal(0, 0.2, n))
dif, dea = macd_lines(closes)
def annotate_dead(ax, dif, dea):
    for i in range(1, n):
        if dif[i-1] >= dea[i-1] and dif[i] < dea[i]:
            ax.annotate('死亡交叉', xy=(i, dif[i]), xytext=(i+5, dif[i]-1.0),
                        fontsize=8, arrowprops=dict(arrowstyle='->', color='green'))
            break
macd_chart(dif, dea, 'v2o-33.png', annotate_dead)

# v2o-34 MACD底背离（股价逐波下降，DIF逐波上升）
np.random.seed(44)
n = 50
# 两个低点，第二个更低，但DIF第二个低点更高
price = np.concatenate([np.linspace(12, 9, 15), np.linspace(9, 11, 8), np.linspace(11, 8.5, 12), np.linspace(8.5, 10, 15)])
closes = list(price + np.random.normal(0, 0.15, n))
dif, dea = macd_lines(closes)
fig, axes = plt.subplots(2, 1, figsize=(5.5, 3.5), dpi=130, gridspec_kw={'height_ratios':[1.2,1]})
ax0 = axes[0]
kline_from_close(ax0, closes, 0.4, seed=44)
ax0.plot([12, 32], [9.5, 8.8], color='red', linestyle='--', linewidth=1.0)  # 股价低点降低
ax0.set_xticks([]); ax0.set_yticks([])
for s in ['top','right','left','bottom']: ax0.spines[s].set_visible(False)
ax1 = axes[1]
ax1.axhline(0, color='black', linewidth=0.6)
ax1.plot(range(n), dif, color='black', linewidth=1.2)
ax1.plot([12, 32], [dif[12], dif[32]], color='red', linestyle='--', linewidth=1.0)  # DIF低点抬高
ax1.set_xticks([]); ax1.set_yticks([])
for s in ['top','right','left','bottom']: ax1.spines[s].set_visible(False)
save(fig, 'v2o-34.png')

# v2o-35 MACD顶背离（股价逐波上升，DIF逐波下降）
np.random.seed(45)
price = np.concatenate([np.linspace(9, 12, 15), np.linspace(12, 10, 8), np.linspace(10, 13, 12), np.linspace(13, 11, 15)])
closes = list(price + np.random.normal(0, 0.15, n))
dif, dea = macd_lines(closes)
fig, axes = plt.subplots(2, 1, figsize=(5.5, 3.5), dpi=130, gridspec_kw={'height_ratios':[1.2,1]})
ax0 = axes[0]
kline_from_close(ax0, closes, 0.4, seed=45)
ax0.plot([12, 32], [11.5, 12.5], color='red', linestyle='--', linewidth=1.0)  # 股价高点抬高
ax0.set_xticks([]); ax0.set_yticks([])
for s in ['top','right','left','bottom']: ax0.spines[s].set_visible(False)
ax1 = axes[1]
ax1.axhline(0, color='black', linewidth=0.6)
ax1.plot(range(n), dif, color='black', linewidth=1.2)
ax1.plot([12, 32], [dif[12], dif[32]], color='red', linestyle='--', linewidth=1.0)  # DIF高点降低
ax1.set_xticks([]); ax1.set_yticks([])
for s in ['top','right','left','bottom']: ax1.spines[s].set_visible(False)
save(fig, 'v2o-35.png')

# ============ BIAS helper ============
def bias_calc(closes, n=10):
    out = []
    for i in range(len(closes)):
        lo = max(0, i - n + 1)
        ma_val = np.mean(closes[lo:i+1])
        out.append((closes[i] - ma_val) / ma_val * 100)
    return out

# v2o-36 乖离率由负变正
np.random.seed(46)
n = 40
price = np.concatenate([np.linspace(12, 10, 15), np.linspace(10, 13, 25)])
closes = list(price + np.random.normal(0, 0.15, n))
bias = bias_calc(closes, 10)
fig, axes = plt.subplots(2, 1, figsize=(5.5, 3.2), dpi=130, gridspec_kw={'height_ratios':[1.2,1]})
ax0 = axes[0]
kline_from_close(ax0, closes, 0.4, seed=46)
ax0.set_xticks([]); ax0.set_yticks([])
for s in ['top','right','left','bottom']: ax0.spines[s].set_visible(False)
ax1 = axes[1]
ax1.axhline(0, color='black', linewidth=0.8)
ax1.plot(range(n), bias, color='black', linewidth=1.3)
for i in range(1, n):
    if bias[i-1] <= 0 and bias[i] > 0:
        ax1.annotate('由负变正', xy=(i, bias[i]), xytext=(i+4, bias[i]+1.5),
                     fontsize=8, arrowprops=dict(arrowstyle='->', color='red'))
        break
ax1.set_xticks([]); ax1.set_yticks([])
for s in ['top','right','left','bottom']: ax1.spines[s].set_visible(False)
save(fig, 'v2o-36.png')

# v2o-37 乖离率由正变负
np.random.seed(47)
price = np.concatenate([np.linspace(10, 13, 15), np.linspace(13, 10, 25)])
closes = list(price + np.random.normal(0, 0.15, n))
bias = bias_calc(closes, 10)
fig, axes = plt.subplots(2, 1, figsize=(5.5, 3.2), dpi=130, gridspec_kw={'height_ratios':[1.2,1]})
ax0 = axes[0]
kline_from_close(ax0, closes, 0.4, seed=47)
ax0.set_xticks([]); ax0.set_yticks([])
for s in ['top','right','left','bottom']: ax0.spines[s].set_visible(False)
ax1 = axes[1]
ax1.axhline(0, color='black', linewidth=0.8)
ax1.plot(range(n), bias, color='black', linewidth=1.3)
for i in range(1, n):
    if bias[i-1] >= 0 and bias[i] < 0:
        ax1.annotate('由正变负', xy=(i, bias[i]), xytext=(i+4, bias[i]-2),
                     fontsize=8, arrowprops=dict(arrowstyle='->', color='green'))
        break
ax1.set_xticks([]); ax1.set_yticks([])
for s in ['top','right','left','bottom']: ax1.spines[s].set_visible(False)
save(fig, 'v2o-37.png')

# v2o-38 乖离率接近历史最大值
np.random.seed(48)
n = 45
price = np.concatenate([np.linspace(10, 12, 15), np.linspace(12, 18, 15), np.linspace(18, 16, 15)])
closes = list(price + np.random.normal(0, 0.15, n))
bias = bias_calc(closes, 10)
fig, axes = plt.subplots(2, 1, figsize=(5.5, 3.2), dpi=130, gridspec_kw={'height_ratios':[1.2,1]})
ax0 = axes[0]
kline_from_close(ax0, closes, 0.4, seed=48)
ax0.set_xticks([]); ax0.set_yticks([])
for s in ['top','right','left','bottom']: ax0.spines[s].set_visible(False)
ax1 = axes[1]
ax1.axhline(0, color='black', linewidth=0.8)
ax1.plot(range(n), bias, color='black', linewidth=1.3)
peak_i = int(np.argmax(bias))
ax1.annotate('接近历史最大值', xy=(peak_i, bias[peak_i]), xytext=(peak_i-12, bias[peak_i]+1.5),
             fontsize=8, arrowprops=dict(arrowstyle='->', color='red'))
ax1.set_xticks([]); ax1.set_yticks([])
for s in ['top','right','left','bottom']: ax1.spines[s].set_visible(False)
save(fig, 'v2o-38.png')

# v2o-39 乖离率接近历史最小值
np.random.seed(49)
price = np.concatenate([np.linspace(18, 16, 15), np.linspace(16, 10, 15), np.linspace(10, 12, 15)])
closes = list(price + np.random.normal(0, 0.15, n))
bias = bias_calc(closes, 10)
fig, axes = plt.subplots(2, 1, figsize=(5.5, 3.2), dpi=130, gridspec_kw={'height_ratios':[1.2,1]})
ax0 = axes[0]
kline_from_close(ax0, closes, 0.4, seed=49)
ax0.set_xticks([]); ax0.set_yticks([])
for s in ['top','right','left','bottom']: ax0.spines[s].set_visible(False)
ax1 = axes[1]
ax1.axhline(0, color='black', linewidth=0.8)
ax1.plot(range(n), bias, color='black', linewidth=1.3)
trough_i = int(np.argmin(bias))
ax1.annotate('接近历史最小值', xy=(trough_i, bias[trough_i]), xytext=(trough_i-12, bias[trough_i]-2),
             fontsize=8, arrowprops=dict(arrowstyle='->', color='green'))
ax1.set_xticks([]); ax1.set_yticks([])
for s in ['top','right','left','bottom']: ax1.spines[s].set_visible(False)
save(fig, 'v2o-39.png')

print("ALL V2 DONE")
