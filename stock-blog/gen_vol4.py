# -*- coding: utf-8 -*-
"""Generate vol4 trading-discipline diagrams (red-up / green-down)."""
import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'FangSong', 'SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
import numpy as np
import os

OUT = r"E:\生活\股票操练大全全套\stock-blog\source\images\kxian"
os.makedirs(OUT, exist_ok=True)

RED = '#FF4444'
GREEN = '#00AA00'
GREY = '#888888'
BLUE = '#2E6BE6'
ORANGE = '#FF8C00'
PURPLE = '#9B59B6'
BROWN = '#8B4513'

def draw_kline(ax, x, o, c, h, l, width=0.3):
    color = RED if c >= o else GREEN
    ax.plot([x, x], [l, h], color=color, linewidth=1.2, zorder=2)
    bottom = min(o, c)
    height = abs(c - o)
    if height < 1e-6:
        height = 0.4
    rect = patches.Rectangle((x - width/2, bottom), width, height,
                             facecolor=color, edgecolor=color, linewidth=0.8, zorder=3)
    ax.add_patch(rect)

def ema(data, n):
    k = 2.0 / (n + 1)
    out = [data[0]]
    for v in data[1:]:
        out.append(out[-1] + k * (v - out[-1]))
    return out

def setup(figsize=(8, 4.5)):
    fig, ax = plt.subplots(figsize=figsize, dpi=130)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', linestyle='--', alpha=0.3)
    return fig, ax

def save(fig, name):
    p = os.path.join(OUT, name)
    fig.savefig(p, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print("saved", p)

np.random.seed(7)

def closes_from(trend, noise=1.0):
    arr = [trend[0]]
    for i in range(1, len(trend)):
        arr.append(arr[-1] + (trend[i]-trend[i-1]) + np.random.normal(0, noise))
    return arr

def kline_from_close(ax, closes, width=0.6):
    for i, c in enumerate(closes):
        o = closes[i-1] if i > 0 else c - 0.5
        h = max(o, c) + abs(np.random.normal(0, 0.6))
        l = min(o, c) - abs(np.random.normal(0, 0.6))
        draw_kline(ax, i, o, c, h, l, width=width)

# ========== 01 底部信号组合 ==========
fig, axes = plt.subplots(2, 1, figsize=(9, 5.6), dpi=130, gridspec_kw={'height_ratios':[2,1]})
np.random.seed(11)
n = 50
# Downtrend then bottoming signals
trend = np.concatenate([
    np.linspace(18, 10, 30),     # 下跌
    np.linspace(10, 9.5, 8),     # 底部震荡
    np.linspace(9.5, 14, 12),    # 回升
])
closes = closes_from(trend, 0.4)
vol = np.concatenate([
    np.linspace(20, 10, 30),     # 缩量下跌
    np.linspace(10, 35, 8),      # 低位放量
    np.linspace(35, 25, 12),     # 温和放量回升
])
ax = axes[0]
kline_from_close(ax, closes, 0.5)
# Mark signals
ax.annotate('长下影十字线\n(止跌信号)', xy=(33, 9.8), xytext=(20, 14),
            fontsize=8, arrowprops=dict(arrowstyle='->', color=BLUE))
ax.annotate('低位放大量\n(主力吸筹)', xy=(36, 9.5), xytext=(38, 12),
            fontsize=8, arrowprops=dict(arrowstyle='->', color=RED))
ax.annotate('首次新低后\n止跌回升', xy=(30, 9.2), xytext=(5, 7),
            fontsize=8, arrowprops=dict(arrowstyle='->', color=GREEN))
ax.set_title('底部信号组合：长下影 + 低位放量 + 首次新低后回升', fontsize=11)
ax.set_xticks([])
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax2 = axes[1]
colors = [RED if closes[i] >= (closes[i-1] if i > 0 else closes[i]) else GREEN for i in range(n)]
ax2.bar(range(n), vol, color=colors, width=0.6)
ax2.set_ylabel('成交量', fontsize=9)
ax2.set_xticks([])
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
save(fig, 'vol4-01.png')

# ========== 02 底部级别判断 ==========
fig, ax = setup((9, 4.5))
np.random.seed(21)
n = 80
# Multi-level bottom: short-term, medium-term, long-term
trend = np.concatenate([
    np.linspace(20, 15, 15),     # 下跌
    np.linspace(15, 16, 5),      # 短期底部反弹
    np.linspace(16, 12, 15),     # 再跌
    np.linspace(12, 13, 5),      # 中期底部反弹
    np.linspace(13, 8, 15),      # 再跌
    np.linspace(8, 9, 5),        # 长期底部
    np.linspace(9, 18, 20),      # 长期上升
])
closes = closes_from(trend, 0.5)
kline_from_close(ax, closes, 0.45)
ax.annotate('短期底部\n(反弹即走)', xy=(17, 15.5), xytext=(10, 18),
            fontsize=8, arrowprops=dict(arrowstyle='->', color=ORANGE))
ax.annotate('中期底部\n(波段操作)', xy=(37, 12.5), xytext=(30, 15),
            fontsize=8, arrowprops=dict(arrowstyle='->', color=BLUE))
ax.annotate('长期底部\n(重仓持有)', xy=(57, 8.5), xytext=(50, 5),
            fontsize=8, arrowprops=dict(arrowstyle='->', color=RED))
ax.set_title('底部级别判断：短期底、中期底、长期底，操作策略完全不同', fontsize=11)
ax.set_xticks([])
save(fig, 'vol4-02.png')

# ========== 03 对称规律 ==========
fig, ax = setup((9, 4.5))
np.random.seed(31)
n = 60
# Two tests of the same bottom level
trend = np.concatenate([
    np.linspace(15, 10, 15),     # 下跌到第一个低点
    np.linspace(10, 12, 8),      # 反弹
    np.linspace(12, 10, 7),      # 二次探底
    np.linspace(10, 11, 5),      # 横盘
    np.linspace(11, 16, 25),     # 上升
])
closes = closes_from(trend, 0.35)
kline_from_close(ax, closes, 0.5)
ax.axhline(10, color='grey', linestyle='--', linewidth=1, alpha=0.7)
ax.scatter(15, 10, color='red', zorder=5, s=50)
ax.scatter(30, 10, color='red', zorder=5, s=50)
ax.annotate('第一个低点', xy=(15, 10), xytext=(12, 8), fontsize=9, color='red')
ax.annotate('第二个低点\n(对称确认)', xy=(30, 10), xytext=(25, 7), fontsize=9, color='red')
ax.set_title('对称规律：重要低点往往反复测试、二次确认后才扎实', fontsize=11)
ax.set_xticks([])
save(fig, 'vol4-03.png')

# ========== 04 抄底操作策略 ==========
fig, ax = plt.subplots(figsize=(9, 5), dpi=130)
ax.set_xlim(0, 10); ax.set_ylim(0, 7); ax.axis('off')
steps = [
    (1.5, 5.5, '等待信号\n不抄底', GREY),
    (3.8, 5.5, '信号组合\n出现3个以上', BLUE),
    (6.1, 5.5, '轻仓试探\n(1/3)', ORANGE),
    (8.4, 5.5, '确认反转\n加仓(再1/3)', RED),
    (5, 2.5, '止损位设在\n最后低点下方', GREEN),
]
for x, y, label, color in steps:
    box = FancyBboxPatch((x-1.0, y-0.6), 2.0, 1.2, boxstyle="round,pad=0.1",
                         facecolor=color, alpha=0.2, edgecolor=color, linewidth=1.5)
    ax.add_patch(box)
    ax.text(x, y, label, ha='center', va='center', fontsize=9, color=color, fontweight='bold')
for i in range(3):
    ax.annotate('', xy=(steps[i+1][0]-1.1, 5.5), xytext=(steps[i][0]+1.1, 5.5),
                arrowprops=dict(arrowstyle='->', color=GREY, lw=1.5))
ax.text(5, 1.0, '核心纪律：不接飞刀，分批建仓，严格止损',
        ha='center', fontsize=10, color=RED, fontweight='bold')
ax.set_title('抄底操作策略：四步走，不急于一时', fontsize=13, pad=10)
save(fig, 'vol4-04.png')

# ========== 05 顶部信号组合 ==========
fig, axes = plt.subplots(2, 1, figsize=(9, 5.6), dpi=130, gridspec_kw={'height_ratios':[2,1]})
np.random.seed(41)
n = 50
# Uptrend then top signals
trend = np.concatenate([
    np.linspace(10, 18, 30),     # 上涨
    np.linspace(18, 18.5, 8),    # 高位滞涨
    np.linspace(18.5, 12, 12),   # 下跌
])
closes = closes_from(trend, 0.4)
vol = np.concatenate([
    np.linspace(10, 25, 30),
    np.linspace(25, 45, 8),      # 天量
    np.linspace(45, 15, 12),
])
ax = axes[0]
kline_from_close(ax, closes, 0.5)
ax.annotate('涨高放大量\n(无论阴阳都危险)', xy=(35, 18.2), xytext=(20, 21),
            fontsize=8, arrowprops=dict(arrowstyle='->', color=RED))
ax.annotate('放量滞涨\n(头部信号)', xy=(38, 18.5), xytext=(38, 21),
            fontsize=8, arrowprops=dict(arrowstyle='->', color=ORANGE))
ax.set_title('顶部信号组合：涨高放大量 + 放量滞涨 + 长上影线', fontsize=11)
ax.set_xticks([])
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax2 = axes[1]
colors = [RED if closes[i] >= (closes[i-1] if i > 0 else closes[i]) else GREEN for i in range(n)]
ax2.bar(range(n), vol, color=colors, width=0.6)
ax2.set_ylabel('成交量', fontsize=9)
ax2.set_xticks([])
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
save(fig, 'vol4-05.png')

# ========== 06 次顶更低 + 月线死叉 ==========
fig, axes = plt.subplots(1, 2, figsize=(11, 4.2), dpi=130)
# Left: second peak lower than first
np.random.seed(51)
n = 50
trend = np.concatenate([
    np.linspace(10, 18, 15),     # 第一个高峰
    np.linspace(18, 14, 10),     # 回调
    np.linspace(14, 16.5, 10),   # 第二个高峰(更低)
    np.linspace(16.5, 10, 15),   # 下跌
])
closes = closes_from(trend, 0.35)
ax = axes[0]
kline_from_close(ax, closes, 0.5)
ax.plot([15, 35], [18, 16.5], color='red', linestyle='--', linewidth=1.5)
ax.annotate('次顶低于前顶\n(牛市结束信号)', xy=(35, 16.5), xytext=(30, 19),
            fontsize=8, arrowprops=dict(arrowstyle='->', color='red'))
ax.set_title('次顶更低：一山更比一山低', fontsize=11)
ax.set_xticks([])
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
# Right: monthly MACD dead cross
np.random.seed(52)
n = 60
price_trend = np.concatenate([np.linspace(12, 18, 30), np.linspace(18, 12, 30)])
closes2 = closes_from(price_trend, 0.3)
ema12 = ema(closes2, 12); ema26 = ema(closes2, 26)
dif = [(ema12[i] - ema26[i]) * 3 for i in range(n)]
dea = ema(dif, 9)
ax = axes[1]
ax.axhline(0, color='black', linewidth=0.8)
ax.plot(range(n), dif, color='black', linewidth=1.4, label='DIF')
ax.plot(range(n), dea, color='orange', linewidth=1.4, label='DEA')
for i in range(n):
    bh = dif[i] - dea[i]
    c = RED if bh >= 0 else GREEN
    ax.bar(i, bh, bottom=0, color=c, width=0.6, alpha=0.7)
ax.annotate('月线死叉\n(中线离场信号)', xy=(35, dif[35]), xytext=(40, dif[35]+2),
            fontsize=8, color='green', arrowprops=dict(arrowstyle='->', color='green'))
ax.set_title('月线MACD高位死叉', fontsize=11)
ax.legend(loc='upper right', fontsize=8, frameon=False)
ax.set_xticks([])
save(fig, 'vol4-06.png')

# ========== 07 逃顶时机 ==========
fig, ax = setup((9, 4.5))
np.random.seed(61)
n = 40
trend = np.concatenate([
    np.linspace(10, 17, 25),
    np.linspace(17, 17.5, 5),
    np.linspace(17.5, 11, 10),
])
closes = closes_from(trend, 0.35)
kline_from_close(ax, closes, 0.5)
# Three sell points
ax.annotate('第一卖点\n(涨高放大量)\n立刻减仓', xy=(28, 17.3), xytext=(15, 20),
            fontsize=8, arrowprops=dict(arrowstyle='->', color=RED),
            bbox=dict(boxstyle='round,pad=0.2', facecolor='yellow', alpha=0.8))
ax.annotate('第二卖点\n(反弹无力)\n继续减仓', xy=(32, 16.5), xytext=(30, 19),
            fontsize=8, arrowprops=dict(arrowstyle='->', color=ORANGE))
ax.annotate('第三卖点\n(破位下行)\n清仓离场', xy=(36, 14), xytext=(35, 10),
            fontsize=8, arrowprops=dict(arrowstyle='->', color=GREEN))
ax.set_title('逃顶时机：三个卖点，越早走损失越小', fontsize=11)
ax.set_xticks([])
save(fig, 'vol4-07.png')

# ========== 08 金字塔建仓 ==========
fig, ax = setup((9, 4.5))
np.random.seed(71)
n = 40
# Price declines, buy more at lower prices
trend = np.linspace(15, 10, n)
closes = closes_from(trend, 0.3)
kline_from_close(ax, closes, 0.5)
# Buy points
buy_points = [(10, closes[10], '第一批\n(30%)'), (20, closes[20], '第二批\n(20%)'), (30, closes[30], '第三批\n(10%)')]
for x, y, label in buy_points:
    ax.scatter(x, y, color='red', marker='^', s=100, zorder=5)
    ax.annotate(label, xy=(x, y), xytext=(x-2, y-1.5), fontsize=8, color='red')
ax.set_title('金字塔建仓：越跌越买，但越买越少，底仓最重', fontsize=11)
ax.set_xticks([])
save(fig, 'vol4-08.png')

# ========== 09 倒金字塔减仓 ==========
fig, ax = setup((9, 4.5))
np.random.seed(81)
n = 40
# Price rises, sell more at higher prices
trend = np.linspace(10, 18, n)
closes = closes_from(trend, 0.3)
kline_from_close(ax, closes, 0.5)
# Sell points
sell_points = [(10, closes[10], '第一批\n(10%)'), (20, closes[20], '第二批\n(20%)'), (30, closes[30], '第三批\n(30%)')]
for x, y, label in sell_points:
    ax.scatter(x, y, color='green', marker='v', s=100, zorder=5)
    ax.annotate(label, xy=(x, y), xytext=(x-2, y+1), fontsize=8, color='green')
ax.set_title('倒金字塔减仓：越涨越卖，越涨卖得越多', fontsize=11)
ax.set_xticks([])
save(fig, 'vol4-09.png')

# ========== 10 仓位与趋势匹配 ==========
fig, ax = plt.subplots(figsize=(9, 4.5), dpi=130)
ax.set_xlim(0, 10); ax.set_ylim(0, 5); ax.axis('off')
trends = [
    (1.7, '上升趋势\n重仓70-90%', RED),
    (4.3, '震荡趋势\n半仓30-50%', ORANGE),
    (7.0, '下降趋势\n轻仓0-20%', GREEN),
    (9.0, '熊市空仓\n0%', GREY),
]
for x, label, color in trends:
    box = FancyBboxPatch((x-1.1, 2), 2.2, 1.2, boxstyle="round,pad=0.1",
                         facecolor=color, alpha=0.2, edgecolor=color, linewidth=2)
    ax.add_patch(box)
    ax.text(x, 2.6, label, ha='center', va='center', fontsize=9, color=color, fontweight='bold')
ax.text(5, 0.8, '核心原则：仓位跟着趋势走，趋势越强仓位越重',
        ha='center', fontsize=10, color='black', fontweight='bold')
ax.set_title('仓位与趋势匹配：顺势加仓、逆势减仓', fontsize=13, pad=10)
save(fig, 'vol4-10.png')

# ========== 11 止损纪律：颈线即生命线 ==========
fig, ax = setup((9, 4.5))
np.random.seed(91)
n = 45
# Breakout above neckline then breakdown
trend = np.concatenate([
    np.linspace(10, 12, 15),     # 底部
    np.linspace(12, 12.5, 5),    # 横盘
    np.linspace(12.5, 16, 10),   # 突破颈线
    np.linspace(16, 14, 5),      # 回落
    np.linspace(14, 11, 10),     # 跌破颈线
])
closes = closes_from(trend, 0.35)
kline_from_close(ax, closes, 0.5)
ax.axhline(12.5, color='black', linestyle='--', linewidth=1.5, alpha=0.7)
ax.text(2, 12.7, '颈线(生命线)', fontsize=9, color='black')
ax.annotate('站在颈线上方\n持股待涨', xy=(25, 14), xytext=(20, 17),
            fontsize=9, arrowprops=dict(arrowstyle='->', color=RED), color=RED)
ax.annotate('有效跌破颈线\n无条件止损', xy=(38, 12.2), xytext=(35, 9),
            fontsize=9, arrowprops=dict(arrowstyle='->', color=GREEN), color=GREEN,
            bbox=dict(boxstyle='round,pad=0.2', facecolor='yellow', alpha=0.8))
ax.set_title('止损纪律：颈线就是生命线，跌破就走不抱幻想', fontsize=11)
ax.set_xticks([])
save(fig, 'vol4-11.png')

# ========== 12 绝不摊平补仓 ==========
fig, axes = plt.subplots(1, 2, figsize=(11, 4.2), dpi=130)
# Left: correct behavior (stop loss)
np.random.seed(101)
n = 30
trend = np.concatenate([np.linspace(12, 13, 15), np.linspace(13, 10, 15)])
closes = closes_from(trend, 0.4)
ax = axes[0]
kline_from_close(ax, closes, 0.5)
ax.axhline(12.5, color='black', linestyle='--', linewidth=1, alpha=0.7)
ax.scatter(18, 12.5, color='red', zorder=5, s=60)
ax.annotate('止损离场\n保住本金', xy=(18, 12.5), xytext=(10, 9),
            fontsize=9, arrowprops=dict(arrowstyle='->', color='red'), color='red',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='lightyellow', alpha=0.8))
ax.set_title('正确做法：跌破止损位就走', fontsize=11)
ax.set_xticks([])
ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
# Right: wrong behavior (averaging down)
np.random.seed(102)
trend2 = np.concatenate([np.linspace(12, 13, 10), np.linspace(13, 6, 20)])
closes2 = closes_from(trend2, 0.4)
ax = axes[1]
kline_from_close(ax, closes2, 0.5)
# Show adding positions at lower levels
for x, y, label in [(12, 11.5, '补仓1'), (18, 9.5, '补仓2'), (24, 7, '补仓3')]:
    ax.scatter(x, y, color='blue', marker='o', s=50, zorder=5)
    ax.annotate(label, xy=(x, y), xytext=(x+1, y+0.5), fontsize=8, color='blue')
ax.set_title('错误做法：越跌越补，越套越深', fontsize=11)
ax.set_xticks([])
ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
fig.suptitle('绝不摊平补仓：止损是承认错误，不是丢面子', fontsize=12, y=1.02)
save(fig, 'vol4-12.png')

# ========== 13 三大危险信号 ==========
fig, axes = plt.subplots(1, 3, figsize=(13, 4), dpi=130)
# 断头铡刀
np.random.seed(111)
n = 25
base = np.linspace(12, 12.5, n)
closes = closes_from(base, 0.25)
closes[-1] = 10
ax = axes[0]
kline_from_close(ax, closes, 0.5)
for nn, col, lab in [(5, RED, '5日'), (10, ORANGE, '10日'), (20, BLUE, '20日')]:
    ma = np.convolve(closes, np.ones(nn)/nn, mode='valid')
    ax.plot(np.arange(nn-1, n), ma, color=col, linewidth=1.2)
ax.annotate('断头铡刀', xy=(n-1, 10), xytext=(8, 9), fontsize=9,
            arrowprops=dict(arrowstyle='->', color='green'), color='green')
ax.set_title('断头铡刀', fontsize=10)
ax.set_xticks([])
ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
# 向下跳空缺口
np.random.seed(112)
n = 30
base = np.concatenate([np.linspace(14, 15, 15), np.linspace(14, 10, 15)])
closes2 = closes_from(base, 0.3)
ax = axes[1]
kline_from_close(ax, closes2, 0.5)
ax.axvspan(14, 15, alpha=0.15, color='green')
ax.annotate('向下跳空缺口', xy=(14.5, 13), xytext=(8, 11), fontsize=9,
            arrowprops=dict(arrowstyle='->', color='green'), color='green')
ax.set_title('向下跳空缺口', fontsize=10)
ax.set_xticks([])
ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
# 死亡谷
np.random.seed(113)
n = 40
base = np.concatenate([np.linspace(15, 16, 20), np.linspace(16, 10, 20)])
closes3 = closes_from(base, 0.35)
ax = axes[2]
kline_from_close(ax, closes3, 0.5)
for nn, col, lab in [(5, RED, '5日'), (10, ORANGE, '10日'), (20, BLUE, '20日')]:
    ma = np.convolve(closes3, np.ones(nn)/nn, mode='valid')
    ax.plot(np.arange(nn-1, n), ma, color=col, linewidth=1.2)
ax.annotate('死亡谷\n(空头排列)', xy=(22, 13), xytext=(25, 9), fontsize=9,
            arrowprops=dict(arrowstyle='->', color='green'), color='green')
ax.set_title('均线死亡谷', fontsize=10)
ax.set_xticks([])
ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
fig.suptitle('三大危险出逃信号：见到就减仓或离场，不要犹豫', fontsize=12, y=1.02)
save(fig, 'vol4-13.png')

# ========== 14 操作纪律对照 ==========
fig, ax = plt.subplots(figsize=(9, 5), dpi=130)
ax.set_xlim(0, 10); ax.set_ylim(0, 8); ax.axis('off')
# Winner vs loser
ax.text(2.5, 7.2, '赢家做法', ha='center', fontsize=12, color=RED, fontweight='bold')
ax.text(7.5, 7.2, '散户做法', ha='center', fontsize=12, color=GREEN, fontweight='bold')
items = [
    (6, '买进谨慎\n(反复确认才下手)', '买进果断\n(听消息就冲)'),
    (5, '卖出果断\n(信号到了就走)', '卖出谨慎\n(被套了就死扛)'),
    (4, '只用闲钱\n(不借钱炒股)', '借钱炒股\n(加杠杆博一把)'),
    (3, '机会属于少数人\n(逆人性操作)', '随大流\n(别人买我也买)'),
    (2, '不频繁交易\n(一年做几次大行情)', '频繁交易\n(天天买卖)'),
]
for y, winner, loser in items:
    ax.text(2.5, y, winner, ha='center', va='center', fontsize=9, color=RED)
    ax.text(7.5, y, loser, ha='center', va='center', fontsize=9, color=GREEN)
ax.plot([5, 5], [1.5, 6.5], color='grey', linewidth=1, linestyle='--')
ax.set_title('操作纪律：赢家与散户的五个根本区别', fontsize=13, pad=10)
save(fig, 'vol4-14.png')

# ========== 15 常见误区 ==========
fig, ax = plt.subplots(figsize=(9, 5.5), dpi=130)
ax.set_xlim(0, 10); ax.set_ylim(0, 8); ax.axis('off')
mistakes = [
    (1, 6.8, '追涨杀跌：涨了就追、跌了就割，来回打脸', RED),
    (1, 5.5, '抄底抄在半山腰：以为跌很多了就买，结果底下还有底', ORANGE),
    (1, 4.2, '死扛不止损：套了就"长期投资"，越套越深', GREEN),
    (1, 2.9, '满仓操作：一把梭哈，跌了没有补仓余地，心态崩溃', BLUE),
    (5.5, 6.8, '听消息炒股：内幕消息、大V推荐，往往是最后一棒', PURPLE),
    (5.5, 5.5, '赚一点就跑：小赚就卖，大亏死扛，赚小亏大', BROWN),
    (5.5, 4.2, '频繁交易：手续费吃掉利润，操作越多错得越多', GREY),
    (5.5, 2.9, '不设止损：凭感觉炒股，没有计划，全靠运气', RED),
]
for x, y, label, color in mistakes:
    ax.text(x, y, '✕ ' + label if '✕' not in label else label, fontsize=9.5, va='center', color=color)
ax.set_title('常见八大误区：看看你中了几条？', fontsize=13, pad=10)
save(fig, 'vol4-15.png')

print("ALL VOL4 DONE")
