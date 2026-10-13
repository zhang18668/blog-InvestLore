# -*- coding: utf-8 -*-
"""Generate vol5 new diagrams 08-15 (red-up / green-down)."""
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

def setup(figsize=(9, 4.6)):
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

def ma(closes, n):
    return np.convolve(closes, np.ones(n)/n, mode='valid')

# ========== 08 大阳线起步：收于5周均线上方 ==========
fig, ax = setup((9, 4.6))
np.random.seed(101)
n = 30
base = np.concatenate([np.linspace(10, 9.5, 12), np.linspace(9.5, 14, 18)])
closes = closes_from(base, 0.35)
# make index 12 a big yang line
closes[12] = 11.5
closes[11] = 9.6
kline_from_close(ax, closes, 0.5)
ma5 = ma(closes, 5)
ax.plot(np.arange(4, n), ma5, color=RED, lw=1.6, label='5周均线')
# mark big yang
ax.annotate('大阳线起步\n收盘站上5周均线', xy=(12, 11.5), xytext=(2, 13.5),
            fontsize=9, arrowprops=dict(arrowstyle='->', color='black'))
ax.axhline(ma5[8], xmin=0.35, xmax=0.45, color=GREY, ls=':', lw=1)
ax.set_title('特征①：周K线拉出大阳线，收于5周均线上方——行情起步信号', fontsize=11)
ax.legend(loc='upper left', fontsize=8, frameon=False)
ax.set_xticks([])
save(fig, 'vol5-08.png')

# ========== 09 沿5周均线爬升 ==========
fig, ax = setup((9, 4.6))
np.random.seed(102)
n = 35
base = np.linspace(11, 20, n)
closes = closes_from(base, 0.4)
kline_from_close(ax, closes, 0.5)
ma5 = ma(closes, 5)
ma10 = ma(closes, 10)
ax.plot(np.arange(4, n), ma5, color=RED, lw=1.6, label='5周均线')
ax.plot(np.arange(9, n), ma10, color=BLUE, lw=1.6, label='10周均线')
# shade above ma5
ax.fill_between(np.arange(4, n), ma5, closes[4:], alpha=0.08, color=RED)
ax.annotate('指数沿5周均线\n一路向上爬升\n持股做多为主', xy=(20, closes[20]), xytext=(20, 23),
            fontsize=9, ha='center', arrowprops=dict(arrowstyle='->', color=RED))
ax.set_title('特征②：沿5周均线稳步爬升——多头趋势确立，一路持股', fontsize=11)
ax.legend(loc='upper left', fontsize=8, frameon=False)
ax.set_xticks([])
save(fig, 'vol5-09.png')

# ========== 10 螺旋桨见顶 ==========
fig, ax = setup((9, 4.6))
np.random.seed(103)
n = 30
base = np.concatenate([np.linspace(12, 19, 22), np.linspace(19, 19.5, 8)])
closes = closes_from(base, 0.35)
kline_from_close(ax, closes, 0.5)
# hand-draw a spinning-top (螺旋桨) at index 22: long upper & lower shadow, small body
xi = 22
o, c = 19.0, 19.3
h, l = 21.5, 16.5
ax.plot([xi, xi], [l, h], color=GREY, lw=1.4, zorder=2)
rect = patches.Rectangle((xi-0.25, o), 0.5, c-o, facecolor=RED, edgecolor=RED, zorder=3)
ax.add_patch(rect)
ax.annotate('螺旋桨K线\n长上下影+小实体\n多空分歧到极点\n→开始分批卖出', xy=(xi, 21.5), xytext=(xi+2, 22.5),
            fontsize=9, arrowprops=dict(arrowstyle='->', color='black'))
ax.set_title('特征③：高位出现螺旋桨——多空剧烈搏杀，变盘在即', fontsize=11)
ax.set_xticks([])
save(fig, 'vol5-10.png')

# ========== 11 跌破螺旋桨下影线 ==========
fig, ax = setup((9, 4.6))
np.random.seed(104)
n = 32
base = np.concatenate([np.linspace(12, 19, 20), np.linspace(19, 17, 12)])
closes = closes_from(base, 0.3)
kline_from_close(ax, closes, 0.5)
# spinning top at 20
xi = 20
ax.plot([xi, xi], [15.5, 21.5], color=GREY, lw=1.4, zorder=2)
rect = patches.Rectangle((xi-0.25, 19.0), 0.5, 0.3, facecolor=RED, edgecolor=RED, zorder=3)
ax.add_patch(rect)
ax.axhline(15.5, color=GREEN, ls='--', lw=1.2)
ax.text(1, 15.2, '螺旋桨下影线支撑位', fontsize=8, color=GREEN)
# breaking candle at 24
ax.annotate('跌破下影线\n→全部抛空出局', xy=(24, closes[24]), xytext=(25, 13),
            fontsize=9, color=GREEN, arrowprops=dict(arrowstyle='->', color=GREEN))
ax.set_title('特征④：周阴线跌破螺旋桨下影线——确认见顶，必须清仓', fontsize=11)
ax.set_xticks([])
save(fig, 'vol5-11.png')

# ========== 12 5周线下穿10周线 死叉走弱 ==========
fig, ax = setup((9, 4.6))
np.random.seed(105)
n = 40
base = np.concatenate([np.linspace(12, 19, 22), np.linspace(19, 13, 18)])
closes = closes_from(base, 0.35)
kline_from_close(ax, closes, 0.45)
m5 = ma(closes, 5)
m10 = ma(closes, 10)
ax.plot(np.arange(4, n), m5, color=RED, lw=1.6, label='5周均线')
ax.plot(np.arange(9, n), m10, color=BLUE, lw=1.6, label='10周均线')
# find dead cross
for i in range(1, len(m5)):
    si = i + 4
    li = i + 9
    if li < len(m10) and m5[i-1] >= m10[li-9] and m5[i] < m10[li-9+1] if li-9+1 < len(m10) else False:
        pass
# approximate cross point at index 26
cx = 26
cy = 16.5
ax.scatter([cx], [cy], color='black', zorder=6, s=50)
ax.annotate('5周线下穿10周线\n10周线调头向下\n趋势走弱，看空', xy=(cx, cy), xytext=(cx+3, 19),
            fontsize=9, arrowprops=dict(arrowstyle='->', color='black'))
ax.set_title('特征⑤：5周线死叉10周线——趋势转弱，持币观望', fontsize=11)
ax.legend(loc='upper right', fontsize=8, frameon=False)
ax.set_xticks([])
save(fig, 'vol5-12.png')

# ========== 13 有效突破 vs 假突破 对比 ==========
fig, axes = plt.subplots(1, 2, figsize=(11, 4.4), dpi=130)
# left: valid breakout
np.random.seed(106)
n = 30
box_top, box_bot = 13, 10
base = np.concatenate([np.full(14, 11.5), np.linspace(12, 16, 16)])
closes = closes_from(base, 0.25)
closes[13] = 13.2
ax = axes[0]
kline_from_close(ax, closes, 0.5)
ax.axhline(box_top, color=BLUE, ls='--', lw=1.2, label='箱体上边线(压力)')
ax.axhline(box_bot, color=GREEN, ls='--', lw=1.2, label='箱体下边线(支撑)')
ax.annotate('有效突破\n放量站稳上边线上方', xy=(15, closes[15]), xytext=(16, 17.5),
            fontsize=9, arrowprops=dict(arrowstyle='->', color=BLUE))
ax.set_title('有效突破：放量站稳，回踩不破', fontsize=11)
ax.legend(loc='upper left', fontsize=7.5, frameon=False)
ax.set_xticks([]); ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
# right: false breakout
np.random.seed(107)
base2 = np.concatenate([np.full(14, 11.5), np.array([13.5, 13.0, 11.0, 10.5, 10.0, 9.5]), np.linspace(9.5, 9, 10)])
closes2 = closes_from(base2, 0.25)
ax = axes[1]
kline_from_close(ax, closes2, 0.5)
ax.axhline(box_top, color=BLUE, ls='--', lw=1.2)
ax.axhline(box_bot, color=GREEN, ls='--', lw=1.2)
ax.annotate('假突破：刺破上边线\n一根大阴线打回箱体内', xy=(16, closes2[16]), xytext=(15, 14.5),
            fontsize=9, color=GREEN, arrowprops=dict(arrowstyle='->', color=GREEN))
ax.set_title('假突破：刺破即回落，必须停损', fontsize=11)
ax.set_xticks([]); ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
fig.suptitle('矩形箱体：有效突破与假突破的辨别', fontsize=12, y=1.02)
save(fig, 'vol5-13.png')

# ========== 14 易混淆图形辨析 ==========
fig, axes = plt.subplots(2, 2, figsize=(10, 6.5), dpi=130)
np.random.seed(108)
# (a) 上升途中整理 vs 顶部
n = 20
ax = axes[0][0]
base = np.concatenate([np.linspace(10, 14, 10), np.linspace(14, 14.5, 10)])
cl = closes_from(base, 0.3)
kline_from_close(ax, cl, 0.45)
ax.set_title('(A) 上升途中横盘整理\n位置低+均线多头→继续看涨', fontsize=9.5)
ax.set_xticks([]); ax.set_yticks([])
# (b) 高位横盘出货
ax = axes[0][1]
base2 = np.concatenate([np.linspace(10, 18, 10), np.linspace(18, 17, 10)])
cl2 = closes_from(base2, 0.3)
kline_from_close(ax, cl2, 0.45)
ax.set_title('(B) 高位横盘出货\n涨幅大+均线走平→警惕见顶', fontsize=9.5)
ax.set_xticks([]); ax.set_yticks([])
# (c) 洗盘 vs 真跌破
ax = axes[1][0]
base3 = np.concatenate([np.linspace(10, 14, 10), np.array([12.5, 13, 14, 14.5, 15])])
cl3 = closes_from(np.concatenate([base3, np.linspace(15, 16, 5)]), 0.25)
kline_from_close(ax, cl3, 0.45)
ax.set_title('(C) 洗盘假跌破\n缩量下探后快速收回→可持有', fontsize=9.5)
ax.set_xticks([]); ax.set_yticks([])
# (d) 真破位
ax = axes[1][1]
base4 = np.concatenate([np.linspace(14, 11, 12), np.linspace(11, 9, 8)])
cl4 = closes_from(base4, 0.25)
kline_from_close(ax, cl4, 0.45)
ax.set_title('(D) 真破位\n放量跌破支撑后不回头→必须离场', fontsize=9.5)
ax.set_xticks([]); ax.set_yticks([])
fig.suptitle('图形识别强化训练：易混淆图形的关键区别在"位置+量能+均线方向"', fontsize=11, y=1.0)
save(fig, 'vol5-14.png')

# ========== 15 赢家操作检查清单（时间轴） ==========
fig, ax = setup((10, 4.8))
ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis('off')
steps = [
    ('①识别', '大阳线起步\n收5周均线上方', RED, 1),
    ('②确认', '沿5周均线爬升\n多头排列', RED, 2.3),
    ('③建仓', '突破时买进\n持股待涨', RED, 3.6),
    ('④预警', '螺旋桨出现\n分批减仓', ORANGE, 4.9),
    ('⑤减仓', '跌破下影线\n全部清仓', GREEN, 6.2),
    ('⑥清仓', '5周死叉10周\n持币观望', GREEN, 7.5),
    ('⑦等待', '调整幅度>1/2\n时间>上涨期', BLUE, 8.8),
]
for label, desc, color, x in steps:
    ax.scatter([x], [3], s=300, color=color, zorder=5)
    ax.text(x, 3, label[0], ha='center', va='center', fontsize=10, color='white', fontweight='bold', zorder=6)
    ax.text(x, 4.2, label, ha='center', fontsize=9, color=color, fontweight='bold')
    ax.text(x, 1.6, desc, ha='center', fontsize=8, color='#333333')
# arrow line
ax.annotate('', xy=(9.5, 3), xytext=(0.5, 3),
            arrowprops=dict(arrowstyle='->', color=GREY, lw=1.5))
ax.set_title('赢家操作七步地图：从识别到等待，每一步都有明确触发信号', fontsize=12)
save(fig, 'vol5-15.png')

print("VOL5 NEW IMAGES DONE")
