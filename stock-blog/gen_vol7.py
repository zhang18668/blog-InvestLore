# -*- coding: utf-8 -*-
"""Generate vol7 top-signal diagrams (red-up / green-down)."""
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

RED = '#FF4444'
GREEN = '#00AA00'
GREY = '#888888'
BLUE = '#2E6BE6'
ORANGE = '#FF8C00'
PURPLE = '#9B59B6'


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
        arr.append(arr[-1] + (trend[i] - trend[i-1]) + np.random.normal(0, noise))
    return arr


def kline_from_close(ax, closes, width=0.6):
    for i, c in enumerate(closes):
        o = closes[i-1] if i > 0 else c - 0.5
        h = max(o, c) + abs(np.random.normal(0, 0.6))
        l = min(o, c) - abs(np.random.normal(0, 0.6))
        draw_kline(ax, i, o, c, h, l, width=width)


# ========== v7-01 高位四种危险单K线 ==========
fig, axes = plt.subplots(1, 4, figsize=(12, 3.6), dpi=130)
np.random.seed(1)
kinds = [
    ('长十字线', 'doji', '高位多空大搏杀\n变盘前兆'),
    ('吊颈线', 'hanging', '长下影假支撑\n主力借撑出货'),
    ('射击之星', 'shoot', '长上影冲高回落\n看似强实则滞涨'),
    ('螺旋桨', 'prop', '上下影俱长\n高位分歧巨大'),
]
for ax, (title, kind, note) in zip(axes, kinds):
    n = 8
    base = np.linspace(10, 13, n)
    closes = closes_from(base, 0.4)
    kline_from_close(ax, closes, 0.5)
    # draw the danger candle at x = 7
    x = 7
    if kind == 'doji':
        o, c, h, l = 13.0, 13.05, 15.2, 10.9
    elif kind == 'hanging':
        o, c, h, l = 13.2, 13.05, 13.35, 10.6
    elif kind == 'shoot':
        o, c, h, l = 12.9, 13.0, 15.3, 12.7
    else:
        o, c, h, l = 13.1, 12.95, 14.9, 11.0
    draw_kline(ax, x, o, c, h, l, width=0.55)
    ax.axvline(x, color=GREY, ls=':', lw=0.8)
    ax.set_title(title, fontsize=11)
    ax.text(3, 9.6, note, fontsize=8, color=GREEN, ha='center')
    ax.set_xticks([]); ax.set_yticks([])
    ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
fig.suptitle('高位单根见顶K线"脸谱"（股价已有较大涨幅后出现）', fontsize=12, y=1.02)
save(fig, 'v7-01.png')

# ========== v7-02 三种无需后验的见顶K线 ==========
fig, axes = plt.subplots(1, 3, figsize=(11, 3.8), dpi=130)
cases = [
    ('高位高开低走\n放量大阴线', 'gap_down'),
    ('高位低开低走\n放量中阴线', 'low_open'),
    ('高位一字跌停\n封死跌停板', 'limit_down'),
]
for ax, (title, kind) in zip(axes, cases):
    n = 12
    base = np.linspace(10, 13.5, n)
    closes = closes_from(base, 0.35)
    kline_from_close(ax, closes, 0.5)
    x = 11
    if kind == 'gap_down':
        o, c, h, l = 14.6, 12.4, 14.7, 12.2
    elif kind == 'low_open':
        o, c, h, l = 13.0, 12.0, 13.1, 11.85
    else:
        o, c, h, l = 12.15, 10.85, 12.15, 10.85
    draw_kline(ax, x, o, c, h, l, width=0.55)
    ax.axvline(x, color=GREY, ls=':', lw=0.8)
    ax.set_title(title, fontsize=10)
    ax.set_xticks([]); ax.set_yticks([])
    ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
fig.suptitle('三种"出现当天就该跑"的见顶K线（无需等后验）', fontsize=12, y=1.03)
save(fig, 'v7-02.png')

# ========== v7-03 高位跳水分时：三个出逃点 ==========
fig, ax = setup((9, 4.6))
np.random.seed(9)
mins = 240
# flat open then sudden drop then weak rebound then fade
t = np.arange(mins)
price = np.full(mins, 20.0) + np.random.normal(0, 0.05, mins)
# sudden drop at t=90 over 20 min
drop_t = np.linspace(0, -1.6, 25)
price[90:115] += drop_t
# weak rebound to halfway (to -0.7)
reb = np.linspace(-1.6, -0.7, 30)
price[115:145] += reb
# fade down again
fade = np.linspace(-0.7, -1.9, mins-145)
price[145:] += fade
ax.plot(t, price, color=RED, lw=1.3)
ax.axhline(20.0, color=GREY, ls='--', lw=0.9)
# 7% line from 20 -> 18.6
ax.axhline(20.0*0.93, color=GREEN, ls='--', lw=1.0)
ax.text(2, 20.0*0.93+0.05, '-7% 预警线', fontsize=8, color=GREEN)
ax.scatter([105], [price[105]], color='black', zorder=6, s=45)
ax.annotate('第一时间：瞬时跌幅>7%\n放量跳水，立即卖出', xy=(105, price[105]),
            xytext=(115, 18.0), fontsize=8.5, arrowprops=dict(arrowstyle='->', color='black'))
ax.scatter([140], [price[140]], color=PURPLE, zorder=6, s=45)
ax.annotate('第二时间：反弹到跳水前\n一半位置、遇涨乏力时卖', xy=(140, price[140]),
            xytext=(150, 18.6), fontsize=8.5, arrowprops=dict(arrowstyle='->', color=PURPLE))
ax.scatter([210], [price[210]], color=BLUE, zorder=6, s=45)
ax.annotate('第三时间：反弹夭折\n再度下行，收盘前离场', xy=(210, price[210]),
            xytext=(150, 17.6), fontsize=8.5, arrowprops=dict(arrowstyle='->', color=BLUE))
ax.set_title('高位跳水分时：第一/第二/第三时间出逃法', fontsize=12)
ax.set_xlabel('交易时间（分钟）', fontsize=9)
ax.set_xticks([])
save(fig, 'v7-03.png')

# ========== v7-04 拉大阳线诱多出货三节奏 ==========
fig, axes = plt.subplots(1, 2, figsize=(11, 4.2), dpi=130)
np.random.seed(12)
n = 30
# left: pull up -> oscillate -> dive
trend = np.concatenate([np.linspace(10, 13, 12),
                        np.linspace(13, 13.8, 4),
                        np.full(6, 13.6),
                        np.linspace(13.6, 10.8, 8)])
closes = closes_from(trend, 0.35)
closes[15] = 15.0  # big yang lure candle
ax = axes[0]
kline_from_close(ax, closes, 0.5)
ax.annotate('拉大阳线诱多', xy=(15, 15.0), xytext=(6, 16.2), fontsize=9,
            arrowprops=dict(arrowstyle='->', color=RED))
ax.annotate('高位横盘派发出货', xy=(20, 13.6), xytext=(18, 15.2), fontsize=8.5)
ax.annotate('重心下移、跳水出货', xy=(27, 11.0), xytext=(22, 11.6), fontsize=8.5,
            arrowprops=dict(arrowstyle='->', color=GREEN))
ax.set_title('诱多出货三节奏：拉高→震荡→跳水', fontsize=11)
ax.set_xticks([]); ax.set_yticks([])
ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
# right: big yang open line as stop reference
np.random.seed(13)
trend2 = np.concatenate([np.linspace(10, 13, 10), np.linspace(13, 14.5, 3)])
closes2 = closes_from(trend2, 0.3)
closes2[12] = 16.0
kline_from_close(axes[1], closes2, 0.5)
axes[1].axhline(closes2[12]-1.2, color=GREEN, ls='--', lw=1)
axes[1].text(0.2, closes2[12]-0.9, '大阳线开盘价=止损线', fontsize=8.5, color=GREEN)
axes[1].set_title('铁律：跌破大阳线开盘价即出局', fontsize=11)
axes[1].set_xticks([]); axes[1].set_yticks([])
axes[1].spines['top'].set_visible(False); axes[1].spines['right'].set_visible(False)
save(fig, 'v7-04.png')

# ========== v7-05 连续集中拉大阳线 ==========
fig, ax = setup((9, 4.6))
np.random.seed(15)
n = 28
trend = np.concatenate([np.linspace(10, 13, 8),
                        np.linspace(13, 19, 8),
                        np.linspace(19, 14, 12)])
closes = closes_from(trend, 0.3)
closes[9] = 15.5; closes[10] = 16.8; closes[11] = 18.2; closes[12] = 19.2
kline_from_close(ax, closes, 0.5)
ax.annotate('连续涨停/大阳\n情绪推到极致 换手>20%', xy=(11, 18.0), xytext=(2, 19.5), fontsize=9,
            arrowprops=dict(arrowstyle='->', color=RED))
ax.annotate('天量之后大逃亡', xy=(22, 15.0), xytext=(20, 16.5), fontsize=9,
            arrowprops=dict(arrowstyle='->', color=GREEN))
ax.set_title('连续集中使用大阳线：情绪顶之后是大逃亡', fontsize=12)
ax.set_xticks([])
save(fig, 'v7-05.png')

# ========== v7-06 宽幅震荡出货五类型 ==========
fig, axes = plt.subplots(2, 3, figsize=(12, 6), dpi=130)
np.random.seed(20)
types = [
    ('高点下移震荡', [16, 15, 14, 13], 'peak_down'),
    ('高点上移震荡', [15, 15.6, 16.2, 16.8], 'peak_up'),
    ('高位宽幅震荡', [16, 16, 16, 16], 'wide'),
    ('中位震荡出货', [13, 13.5, 13, 13.5], 'mid'),
    ('箱顶出货', [16, 16, 16, 16], 'box'),
    ('不规则震荡', [15.5, 16.5, 15.8, 16.8], 'irregular'),
]
for ax, (title, peaks, kind) in zip(axes.flat, types):
    n = 24
    if kind == 'peak_down':
        base = np.concatenate([np.linspace(10, 15, 6), [15, 14.2, 14.8, 13.0, 13.6, 11.5, 12.0, 10.0, 9.5], np.linspace(9.5, 9, 6)])
    elif kind == 'peak_up':
        base = np.concatenate([np.linspace(10, 15, 6), [15, 15.8, 14.6, 16.4, 15.0, 17.0, 15.5, 16.2, 15.2], np.linspace(15.2, 11, 6)])
    elif kind == 'wide':
        base = np.concatenate([np.linspace(10, 16, 8), [16.5, 13.5, 16.3, 13.8, 16.0, 14.0], np.linspace(14, 10, 10)])
    elif kind == 'mid':
        base = np.concatenate([np.linspace(10, 13, 5), [13.5, 12.5, 14.0, 12.8, 13.8, 13.0], np.linspace(13, 9, 13)])
    elif kind == 'box':
        base = np.concatenate([np.linspace(10, 16, 8), [16.0, 15.2, 16.0, 15.3, 16.0, 15.4], np.linspace(15.4, 10, 10)])
    else:
        base = np.concatenate([np.linspace(10, 15.5, 7), [16.6, 14.6, 16.0, 14.9, 16.8, 14.8], np.linspace(14.8, 10, 10)])
    base = np.array(base, dtype=float)[:n]
    closes = closes_from(base, 0.25)
    kline_from_close(ax, closes, 0.45)
    ax.set_title(title, fontsize=10)
    ax.set_xticks([]); ax.set_yticks([])
    ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
fig.suptitle('宽幅震荡出货的五种类型', fontsize=13, y=1.0)
save(fig, 'v7-06.png')

# ========== v7-07 量价顶背离 ==========
fig, axes = plt.subplots(2, 1, figsize=(9, 5.4), dpi=130, gridspec_kw={'height_ratios':[2, 1]})
np.random.seed(30)
n = 38
trend = np.concatenate([np.linspace(10, 15, 16), np.linspace(15, 13.5, 6), np.linspace(13.5, 17, 16)])
closes = closes_from(trend, 0.4)
vol = np.concatenate([np.linspace(30, 46, 16), np.linspace(46, 34, 6), np.linspace(34, 18, 16)])
ax = axes[0]
kline_from_close(ax, closes, 0.5)
ax.plot([6, 28], [14.6, 16.8], color='red', ls='--', lw=1.2)
ax.set_title('量价顶背离：股价创新高，成交量却一浪低一浪', fontsize=11)
ax.set_xticks([]); ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
ax2 = axes[1]
colors = [RED if closes[i] >= (closes[i-1] if i > 0 else closes[i]) else GREEN for i in range(n)]
ax2.bar(range(n), vol, color=colors, width=0.6)
ax2.plot([6, 28], [44, 19], color='red', ls='--', lw=1.2)
ax2.set_ylabel('成交量', fontsize=9); ax2.set_xticks([])
ax2.spines['top'].set_visible(False); ax2.spines['right'].set_visible(False)
save(fig, 'v7-07.png')

# ========== v7-08 MACD顶背离 ==========
def ema(data, n):
    k = 2.0 / (n + 1)
    out = [data[0]]
    for v in data[1:]:
        out.append(out[-1] + k * (v - out[-1]))
    return out

fig, axes = plt.subplots(2, 1, figsize=(9, 5.2), dpi=130, gridspec_kw={'height_ratios':[1.3, 1]})
np.random.seed(33)
n = 48
trend = np.concatenate([np.linspace(12, 15, 14), np.linspace(15, 13.6, 7), np.linspace(13.6, 17, 18), np.linspace(17, 15, 9)])
closes = closes_from(trend, 0.3)
ema12 = ema(closes, 12); ema26 = ema(closes, 26)
dif = [(ema12[i] - ema26[i]) * 3 for i in range(n)]
ax = axes[0]
kline_from_close(ax, closes, 0.45)
ax.plot([9, 33], [14.6, 16.8], color='red', ls='--', lw=1.2)
ax.set_title('MACD顶背离：股价逐波走高，DIF却逐波走低', fontsize=11)
ax.set_xticks([]); ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
ax2 = axes[1]
ax2.plot(range(n), dif, color='black', lw=1.3)
ax2.axhline(0, color='grey', lw=0.8)
ax2.plot([11, 36], [1.1, 0.25], color='red', ls='--', lw=1.2)
ax2.set_ylabel('DIF', fontsize=9); ax2.set_xticks([])
ax2.spines['top'].set_visible(False); ax2.spines['right'].set_visible(False)
save(fig, 'v7-08.png')

# ========== v7-09 信号共振三重确认 ==========
fig, axes = plt.subplots(3, 1, figsize=(9, 6.4), dpi=130, gridspec_kw={'height_ratios':[2, 0.8, 0.8]})
np.random.seed(40)
n = 40
trend = np.concatenate([np.linspace(10, 17, 24), np.linspace(17, 12, 16)])
closes = closes_from(trend, 0.35)
closes[24] = 15.5  # 吊颈/长上影 danger
ax = axes[0]
kline_from_close(ax, closes, 0.5)
for nn, col, lab in [(5, RED, '5日'), (10, ORANGE, '10日'), (30, BLUE, '30日')]:
    ma = np.convolve(closes, np.ones(nn)/nn, mode='valid')
    ax.plot(np.arange(nn-1, n), ma, color=col, lw=1.4, label=lab)
ax.annotate('高位吊颈+长上影', xy=(24, 17.2), xytext=(12, 18.0), fontsize=8.5,
            arrowprops=dict(arrowstyle='->', color='black'))
ax.annotate('均线高位死叉', xy=(28, 15.5), xytext=(28, 17.5), fontsize=8.5, color=GREEN,
            arrowprops=dict(arrowstyle='->', color=GREEN))
ax.set_title('信号共振：K线见顶 + 均线死叉 + 量能天量，三重确认', fontsize=11)
ax.legend(loc='upper left', fontsize=8, frameon=False)
ax.set_xticks([]); ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
ax2 = axes[1]
vol = np.concatenate([np.linspace(20, 55, 24), np.linspace(55, 25, 16)])
colors = [RED if closes[i] >= (closes[i-1] if i > 0 else closes[i]) else GREEN for i in range(n)]
ax2.bar(range(n), vol, color=colors, width=0.6)
ax2.annotate('天量', xy=(24, 55), xytext=(20, 60), fontsize=8.5, color=RED)
ax2.set_ylabel('量能', fontsize=9); ax2.set_xticks([])
ax2.spines['top'].set_visible(False); ax2.spines['right'].set_visible(False)
ax3 = axes[2]
ema12 = ema(closes, 12); ema26 = ema(closes, 26)
dif = [(ema12[i] - ema26[i])*3 for i in range(n)]
ax3.plot(range(n), dif, color='black', lw=1.2)
ax3.axhline(0, color='grey', lw=0.7)
ax3.set_ylabel('MACD', fontsize=9); ax3.set_xticks([])
ax3.spines['top'].set_visible(False); ax3.spines['right'].set_visible(False)
save(fig, 'v7-09.png')

# ========== v7-10 高点下移震荡出货 ==========
fig, ax = setup((9, 4.6))
np.random.seed(44)
n = 30
base = np.concatenate([np.linspace(10, 16, 6), [16, 14.0, 15.2, 13.0, 14.2, 12.0, 12.8, 10.8, 11.2, 9.5], np.linspace(9.5, 9, 10)])
closes = closes_from(base, 0.25)
kline_from_close(ax, closes, 0.5)
ax.plot([6, 9, 12, 15], [16, 15.2, 14.2, 12.8], color=GREEN, ls='--', lw=1.3, marker='o', ms=4)
ax.annotate('反弹高点逐次下移\n一浪低过一浪', xy=(12, 14.2), xytext=(15, 15.5), fontsize=9,
            arrowprops=dict(arrowstyle='->', color=GREEN))
ax.set_title('高点下移震荡出货（最常见的出货形态）', fontsize=12)
ax.set_xticks([])
save(fig, 'v7-10.png')

# ========== v7-11 箱顶出货 ==========
fig, ax = setup((9, 4.6))
np.random.seed(46)
n = 30
base = np.concatenate([np.linspace(10, 16, 8), [16.0, 15.2, 16.0, 15.2, 16.0, 15.2, 16.0, 15.2], np.linspace(15.2, 10, 14)])
closes = closes_from(base, 0.2)
kline_from_close(ax, closes, 0.5)
ax.axhline(16.0, color=RED, ls='--', lw=1)
ax.axhline(15.2, color=GREEN, ls='--', lw=1)
ax.text(0.5, 16.1, '箱顶压力区（反复派发）', fontsize=8.5, color=RED)
ax.text(0.5, 14.7, '箱底', fontsize=8.5, color=GREEN)
ax.set_title('箱顶出货：在箱体上沿反复冲高派发', fontsize=12)
ax.set_xticks([])
save(fig, 'v7-11.png')

# ========== v7-12 跳水出货 vs 高抛低吸年线 ==========
fig, ax = setup((9, 4.6))
np.random.seed(48)
n = 40
base = np.concatenate([np.linspace(10, 16, 16), np.linspace(16, 15, 8), np.linspace(15, 9.5, 16)])
closes = closes_from(base, 0.3)
kline_from_close(ax, closes, 0.5)
ma250_proxy = np.convolve(closes, np.ones(15)/15, mode='valid')
ax.plot(np.arange(14, n), ma250_proxy, color=BLUE, lw=1.8, label='年线(250日线)')
ax.scatter([28], [closes[28]], color=GREEN, zorder=6, s=50)
ax.annotate('有效跌破年线\n无条件离场', xy=(28, closes[28]), xytext=(20, 11.5), fontsize=9,
            arrowprops=dict(arrowstyle='->', color=GREEN))
ax.set_title('年线为最后防线：跌破年线停止一切高抛低吸', fontsize=12)
ax.legend(loc='upper left', fontsize=8, frameon=False)
ax.set_xticks([])
save(fig, 'v7-12.png')

# ========== v7-13 天量天价 ==========
fig, axes = plt.subplots(2, 1, figsize=(9, 5.2), dpi=130, gridspec_kw={'height_ratios':[2, 1]})
np.random.seed(52)
n = 30
trend = np.concatenate([np.linspace(10, 17, 20), np.linspace(17, 13, 10)])
closes = closes_from(trend, 0.3)
vol = np.concatenate([np.linspace(20, 60, 18), np.linspace(60, 30, 12)])
ax = axes[0]
kline_from_close(ax, closes, 0.5)
ax.scatter([18], [closes[18]], color=RED, zorder=6, s=50)
ax.set_title('天量天价：历史最大成交量出现的当天，往往就是天价', fontsize=11)
ax.set_xticks([]); ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
ax2 = axes[1]
colors = [RED if closes[i] >= (closes[i-1] if i > 0 else closes[i]) else GREEN for i in range(n)]
ax2.bar(range(n), vol, color=colors, width=0.6)
ax2.annotate('天量', xy=(18, 60), xytext=(15, 64), fontsize=9, color=RED)
ax2.set_ylabel('成交量', fontsize=9); ax2.set_xticks([])
ax2.spines['top'].set_visible(False); ax2.spines['right'].set_visible(False)
save(fig, 'v7-13.png')

# ========== v7-14 主力出货手法对比（示意） ==========
fig, ax = setup((9, 4.8))
np.random.seed(55)
n = 26
# 诱多型：急涨急跌
base_a = np.concatenate([np.linspace(10, 17, 10), np.linspace(17, 11, 16)])
closes_a = closes_from(base_a, 0.3)
closes_a[9] = 18.5
kline_from_close(ax, closes_a, 0.45)
ax.plot(np.arange(n), closes_a, color=RED, lw=1.0, alpha=0.5, label='拉大阳线诱多出货（急涨急跌）')
# 震荡型：高位宽幅
ax2 = ax
# second series offset
np.random.seed(56)
base_b = np.concatenate([np.full(6, 12), [16.5, 13.5, 16.5, 13.5, 16.5, 13.5, 16.5, 13.5], np.linspace(13.5, 12, 12)])
closes_b = np.array(closes_from(base_b, 0.2))
ax.plot(np.arange(n), closes_b + 0.0, color=BLUE, lw=1.4, ls='--', label='宽幅震荡出货（高位反复）')
ax.set_title('两类出货手法走势对比：诱多快、震荡慢', fontsize=12)
ax.legend(loc='upper right', fontsize=8.5, frameon=False)
ax.set_xticks([]); ax.set_yticks([])
save(fig, 'v7-14.png')

# ========== v7-15 抄底接飞刀误区 ==========
fig, ax = setup((9, 4.6))
np.random.seed(60)
n = 30
base = np.concatenate([np.linspace(10, 16, 8), np.linspace(16, 15.5, 3), np.linspace(15.5, 8, 19)])
closes = closes_from(base, 0.35)
kline_from_close(ax, closes, 0.5)
ax.scatter([12], [15.3], color=RED, zorder=6, s=55)
ax.annotate('"跌这么多该反弹了"\n盲目抄底接飞刀', xy=(12, 15.3), xytext=(3, 13), fontsize=9,
            arrowprops=dict(arrowstyle='->', color=RED))
ax.annotate('结果越套越深', xy=(25, 8.5), xytext=(18, 11), fontsize=9, color=GREEN,
            arrowprops=dict(arrowstyle='->', color=GREEN))
ax.set_title('误区：见顶信号出现后，把下跌当"回调"去抄底', fontsize=12)
ax.set_xticks([])
save(fig, 'v7-15.png')

# ========== v7-16 见顶不止损，扛单越套越深 ==========
fig, ax = setup((9, 4.6))
np.random.seed(63)
n = 32
base = np.concatenate([np.linspace(10, 16, 10), np.linspace(16, 9, 22)])
closes = closes_from(base, 0.35)
kline_from_close(ax, closes, 0.5)
ax.axhline(16, color=RED, ls='--', lw=1)
ax.text(0.3, 16.2, '见顶位', fontsize=8.5, color=RED)
ax.scatter([10], [16], color=RED, zorder=6, s=45)
ax.annotate('不止损→越跌越补→深度套牢', xy=(20, closes[20]), xytext=(12, 12), fontsize=9,
            arrowprops=dict(arrowstyle='->', color=GREEN))
ax.set_title('误区：见顶不认错，小亏拖成大亏', fontsize=12)
ax.set_xticks([])
save(fig, 'v7-16.png')

# ========== v7-17 迷信单一信号 ==========
fig, ax = setup((9, 4.6))
np.random.seed(66)
n = 34
# 多头排列中假黄昏之星
base = np.concatenate([np.linspace(10, 15, 24), np.linspace(15, 15.5, 10)])
closes = closes_from(base, 0.3)
closes[16] = 14.0; closes[17] = 15.6; closes[18] = 14.3
kline_from_close(ax, closes, 0.5)
for nn, col, lab in [(5, RED, '5日'), (10, ORANGE, '10日'), (20, BLUE, '20日')]:
    ma = np.convolve(closes, np.ones(nn)/nn, mode='valid')
    ax.plot(np.arange(nn-1, n), ma, color=col, lw=1.3, label=lab)
ax.annotate('单根"黄昏之星"\n在多头排列里多为洗盘', xy=(17, 15.6), xytext=(2, 16.3), fontsize=9,
            arrowprops=dict(arrowstyle='->', color='black'))
ax.set_title('误区：仅凭单根K线就逃顶，常被洗盘甩下车', fontsize=12)
ax.legend(loc='upper left', fontsize=8, frameon=False)
ax.set_xticks([])
save(fig, 'v7-17.png')

# ========== v7-18 逃顶操作流程 ==========
fig, ax = plt.subplots(figsize=(9, 3.2), dpi=130)
ax.axis('off')
steps = ['识别高位\n单K脸谱', '检查三种\n即时见顶', '量价/MACD\n是否背离', '均线是否\n高位死叉', '信号共振\n2~3个', '执行减仓\n直至清仓']
colors = [ORANGE, RED, PURPLE, BLUE, GREEN, '#C0392B']
n = len(steps)
for i, (s, c) in enumerate(zip(steps, colors)):
    x = 0.5 + i * 1.6
    box = patches.FancyBboxPatch((x, 1.2), 1.2, 1.0, boxstyle="round,pad=0.05",
                                 facecolor=c, edgecolor='black', alpha=0.85)
    ax.add_patch(box)
    ax.text(x+0.6, 1.7, s, ha='center', va='center', fontsize=8.5, color='white')
    if i < n-1:
        ax.annotate('', xy=(x+1.62, 1.7), xytext=(x+1.22, 1.7),
                    arrowprops=dict(arrowstyle='->', lw=1.5, color='black'))
ax.set_xlim(0, n*1.6+0.4); ax.set_ylim(0.5, 2.8)
ax.set_title('标准化逃顶操作流程：先识别、再确认、后执行', fontsize=12)
save(fig, 'v7-18.png')

print("VOL7 ALL DONE")
