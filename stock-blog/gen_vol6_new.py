# -*- coding: utf-8 -*-
"""Generate vol6 new diagrams 08-15 (red-up / green-down)."""
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

# ========== 08 趋势线画法与有效突破 ==========
fig, axes = plt.subplots(1, 2, figsize=(11, 4.4), dpi=130)
# left: uptrend line drawn from two rising lows
np.random.seed(201)
n = 40
low_x = [6, 24]; low_y = [9, 13]
trend = np.array([low_y[0] + (low_y[1]-low_y[0])*i/(n-1) for i in range(n)]) + np.array([1.3*np.sin(i/3.0) for i in range(n)])
closes = closes_from(trend, 0.25)
ax = axes[0]
kline_from_close(ax, closes, 0.5)
ax.plot([low_x[0], low_x[1]], [low_y[0], low_y[1]], color=BLUE, lw=2, label='上升趋势线')
ax.scatter(low_x, low_y, color='black', zorder=5, s=40)
ax.annotate('连接两个依次抬高的低点\n形成支撑线', xy=(15, 10.5), fontsize=9, color=BLUE)
ax.set_title('上升趋势线画法：两点连线成支撑', fontsize=11)
ax.legend(loc='upper left', fontsize=8, frameon=False)
ax.set_xticks([]); ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
# right: valid breakout above downtrend line
np.random.seed(202)
high_x = [6, 24]; high_y = [16, 11]
trend2 = np.array([high_y[0] + (high_y[1]-high_y[0])*i/(n-1) for i in range(n)]) - np.array([1.3*np.sin(i/3.0) for i in range(n)])
trend2 = list(trend2)
# after index 28, break above
for i in range(28, n):
    trend2[i] = 11.5 + (i-28)*0.35
closes2 = closes_from(trend2, 0.25)
ax = axes[1]
kline_from_close(ax, closes2, 0.5)
ax.plot([high_x[0], high_x[1]+6], [high_y[0], high_y[1]-1.5], color=GREEN, lw=2, label='下降趋势线')
ax.scatter(high_x, high_y, color='black', zorder=5, s=40)
ax.annotate('放量突破下降趋势线\n→趋势反转确认', xy=(30, closes2[30]), xytext=(18, 17),
            fontsize=9, color=RED, arrowprops=dict(arrowstyle='->', color=RED))
ax.set_title('有效突破：放量站上下降趋势线', fontsize=11)
ax.legend(loc='upper right', fontsize=8, frameon=False)
ax.set_xticks([]); ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
fig.suptitle('趋势线实战：画法要点与有效突破的辨认', fontsize=12, y=1.02)
save(fig, 'vol6-08.png')

# ========== 09 趋势线操作：支撑变压力 ==========
fig, ax = setup((9, 4.8))
np.random.seed(203)
n = 50
low_x = [8, 22]; low_y = [9, 12]
trend = np.array([low_y[0] + (low_y[1]-low_y[0])*i/(n-1) for i in range(n)]) + np.array([1.1*np.sin(i/2.5) for i in range(n)])
for i in range(34, n):
    trend[i] = 12.5 - (i-34)*0.22
closes = closes_from(trend, 0.28)
kline_from_close(ax, closes, 0.5)
xs = np.array([low_x[0], 48])
ys = np.array([low_y[0], low_y[0] + (low_y[1]-low_y[0])*(48-low_x[0])/(low_x[1]-low_x[0])])
ax.plot(xs, ys, color=BLUE, lw=1.8, ls='-', label='原上升趋势线(支撑)')
bx = 34; by = low_y[0] + (low_y[1]-low_y[0])*(34-low_x[0])/(low_x[1]-low_x[0])
ax.scatter([bx], [by], color=RED, zorder=6, s=50)
ax.annotate('有效跌破趋势线\n→支撑变压力\n→卖出离场', xy=(bx, by), xytext=(bx+3, by+3),
            fontsize=9, arrowprops=dict(arrowstyle='->', color='red'))
# after break, line becomes resistance
xs2 = np.array([34, 48]); ys2 = np.array([by, low_y[0] + (low_y[1]-low_y[0])*(48-low_x[0])/(low_x[1]-low_x[0])])
ax.plot(xs2, ys2, color=GREY, lw=1.5, ls='--', label='跌破后转为压力线')
ax.set_title('趋势线被有效突破后：支撑变压力，反弹即卖点', fontsize=12)
ax.legend(loc='upper right', fontsize=8, frameon=False)
ax.set_xticks([])
save(fig, 'vol6-09.png')

# ========== 10 牛熊市特征对比 ==========
fig, axes = plt.subplots(1, 2, figsize=(11, 4.4), dpi=130)
# bull market
np.random.seed(204)
n = 40
base = np.concatenate([np.linspace(8, 18, 25), np.linspace(18, 22, 15)])
closes = closes_from(base, 0.5)
ax = axes[0]
kline_from_close(ax, closes, 0.5)
for nn, col, lab in [(5, RED, '5日'), (10, ORANGE, '10日'), (30, BLUE, '30日')]:
    m = ma(closes, nn)
    ax.plot(np.arange(nn-1, n), m, color=col, lw=1.5, label=lab)
ax.set_title('牛市：低点抬高、均线多头排列\n回调即买点，持股为主', fontsize=10.5, color=RED)
ax.legend(loc='upper left', fontsize=7.5, frameon=False)
ax.set_xticks([]); ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
# bear market
np.random.seed(205)
base2 = np.concatenate([np.linspace(20, 12, 25), np.linspace(12, 8, 15)])
closes2 = closes_from(base2, 0.5)
ax = axes[1]
kline_from_close(ax, closes2, 0.5)
for nn, col, lab in [(5, RED, '5日'), (10, ORANGE, '10日'), (30, BLUE, '30日')]:
    m = ma(closes2, nn)
    ax.plot(np.arange(nn-1, n), m, color=col, lw=1.5, label=lab)
ax.set_title('熊市：高点降低、均线空头排列\n反弹即卖点，持币为主', fontsize=10.5, color=GREEN)
ax.legend(loc='upper right', fontsize=7.5, frameon=False)
ax.set_xticks([]); ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
fig.suptitle('牛熊市判断：均线排列方向+高低点结构，是最直观的大势温度计', fontsize=12, y=1.02)
save(fig, 'vol6-10.png')

# ========== 11 选股标准与时机 ==========
fig, ax = setup((9, 5.2))
ax.axis('off')
ax.set_xlim(0, 10); ax.set_ylim(0, 10)
# left column: standards
ax.text(2.5, 9.2, '选股四大标准', ha='center', fontsize=12, fontweight='bold', color=RED)
std_items = [
    '① 均线多头排列\n5/10/30日向上发散',
    '② 股价站稳均线之上\n回踩不破均线支撑',
    '③ 量能温和放大\n价涨量增，价跌量缩',
    '④ 走势强于大盘\n大盘跌它抗跌，大盘涨它领涨',
]
for i, t in enumerate(std_items):
    ax.text(2.5, 7.8 - i*1.7, t, ha='center', fontsize=9,
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#FFF0F0', edgecolor=RED, alpha=0.8))
# right column: timing
ax.text(7.5, 9.2, '选股最佳时机', ha='center', fontsize=12, fontweight='bold', color=BLUE)
time_items = [
    '① 银山谷/金山谷出现\n均线低位金叉三角',
    '② 回踩均线获得支撑\n缩量回踩后再度放量',
    '③ 突破长期下降趋势线\n放量站上关键压力位',
    '④ 大盘企稳初期\n龙头股率先启动时',
]
for i, t in enumerate(time_items):
    ax.text(7.5, 7.8 - i*1.7, t, ha='center', fontsize=9,
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#F0F4FF', edgecolor=BLUE, alpha=0.8))
ax.set_title('选股技巧：好股票+好时机，缺一不可', fontsize=12)
save(fig, 'vol6-11.png')

# ========== 12 买点信号汇总 ==========
fig, axes = plt.subplots(2, 2, figsize=(10, 6), dpi=130)
np.random.seed(206)
# (a) 蛟龙出海
n = 22
ax = axes[0][0]
base = np.linspace(11, 11, n)
cl = closes_from(base, 0.25); cl[-1] = 13.5
kline_from_close(ax, cl, 0.5)
for nn, col in [(5, RED), (10, ORANGE), (20, BLUE)]:
    m = ma(cl, nn); ax.plot(np.arange(nn-1, n), m, color=col, lw=1.3)
ax.annotate('蛟龙出海\n大阳穿多线', xy=(n-1, 13.5), xytext=(n-12, 14.5), fontsize=8.5,
            arrowprops=dict(arrowstyle='->', color='black'))
ax.set_title('买点①：蛟龙出海', fontsize=10)
ax.set_xticks([]); ax.set_yticks([])
# (b) 回踩均线
ax = axes[0][1]
base2 = np.concatenate([np.linspace(9, 14, 12), np.array([13, 12.5, 13, 14, 14.5])])
cl2 = closes_from(np.concatenate([base2, np.linspace(14.5, 15, 5)]), 0.2)
kline_from_close(ax, cl2, 0.5)
m5 = ma(cl2, 5); ax.plot(np.arange(4, len(cl2)), m5, color=RED, lw=1.3)
ax.annotate('回踩5日线\n缩量企稳→买', xy=(14, 12.5), xytext=(8, 10.5), fontsize=8.5,
            arrowprops=dict(arrowstyle='->', color=BLUE))
ax.set_title('买点②：回踩均线获支撑', fontsize=10)
ax.set_xticks([]); ax.set_yticks([])
# (c) 底部放量长阳
ax = axes[1][0]
base3 = np.concatenate([np.linspace(10, 8.5, 12), np.array([9.5, 11, 12, 12.5, 13])])
cl3 = closes_from(np.concatenate([base3, np.linspace(13, 13.5, 5)]), 0.2)
kline_from_close(ax, cl3, 0.5)
ax.annotate('底部放量长阳\n多头反攻', xy=(13, 11), xytext=(5, 13), fontsize=8.5,
            arrowprops=dict(arrowstyle='->', color=RED))
ax.set_title('买点③：底部放量长阳', fontsize=10)
ax.set_xticks([]); ax.set_yticks([])
# (d) 趋势线突破
ax = axes[1][1]
base4 = np.concatenate([np.linspace(14, 10, 18), np.linspace(10, 13, 8)])
cl4 = closes_from(base4, 0.2)
kline_from_close(ax, cl4, 0.5)
ax.plot([3, 18], [13.5, 10.5], color=GREEN, lw=1.5, ls='--')
ax.annotate('放量突破\n下降趋势线', xy=(20, 11.5), xytext=(15, 14.5), fontsize=8.5,
            arrowprops=dict(arrowstyle='->', color=RED))
ax.set_title('买点④：突破下降趋势线', fontsize=10)
ax.set_xticks([]); ax.set_yticks([])
fig.suptitle('买点信号汇总：四种经典买入形态', fontsize=12, y=1.0)
save(fig, 'vol6-12.png')

# ========== 13 卖点信号汇总 ==========
fig, axes = plt.subplots(2, 2, figsize=(10, 6), dpi=130)
np.random.seed(207)
# (a) 断头铡刀
n = 22
ax = axes[0][0]
base = np.linspace(12, 13, n)
cl = closes_from(base, 0.25); cl[-1] = 10.5
kline_from_close(ax, cl, 0.5)
for nn, col in [(5, RED), (10, ORANGE), (20, BLUE)]:
    m = ma(cl, nn); ax.plot(np.arange(nn-1, n), m, color=col, lw=1.3)
ax.annotate('断头铡刀\n大阴穿多线', xy=(n-1, 10.5), xytext=(n-12, 9), fontsize=8.5,
            arrowprops=dict(arrowstyle='->', color='green'))
ax.set_title('卖点①：断头铡刀', fontsize=10)
ax.set_xticks([]); ax.set_yticks([])
# (b) 跌破下影线
ax = axes[0][1]
base2 = np.concatenate([np.linspace(10, 15, 16), np.linspace(15, 12, 8)])
cl2 = closes_from(base2, 0.2)
kline_from_close(ax, cl2, 0.5)
ax.annotate('高位螺旋桨后\n跌破下影线→卖', xy=(20, 13), xytext=(10, 11), fontsize=8.5,
            arrowprops=dict(arrowstyle='->', color='green'))
ax.set_title('卖点②：跌破螺旋桨下影线', fontsize=10)
ax.set_xticks([]); ax.set_yticks([])
# (c) 顶背离
ax = axes[1][0]
base3 = np.concatenate([np.linspace(10, 14, 12), np.linspace(14, 15, 8), np.linspace(15, 16, 10)])
cl3 = closes_from(base3, 0.2)
kline_from_close(ax, cl3, 0.5)
ax.plot([8, 28], [13.5, 15.8], color=RED, ls='--', lw=1.2)
ax.annotate('股价创新高\n量能/MACD背离', xy=(28, 15.8), xytext=(18, 13), fontsize=8.5,
            arrowprops=dict(arrowstyle='->', color='green'))
ax.set_title('卖点③：量价/MACD顶背离', fontsize=10)
ax.set_xticks([]); ax.set_yticks([])
# (d) 死叉
ax = axes[1][1]
base4 = np.concatenate([np.linspace(10, 16, 18), np.linspace(16, 12, 10)])
cl4 = closes_from(base4, 0.2)
kline_from_close(ax, cl4, 0.5)
m5 = ma(cl4, 5); m10 = ma(cl4, 10)
ax.plot(np.arange(4, len(cl4)), m5, color=RED, lw=1.3)
ax.plot(np.arange(9, len(cl4)), m10, color=BLUE, lw=1.3)
ax.annotate('5日死叉10日\n→趋势转弱', xy=(22, 14), xytext=(12, 11), fontsize=8.5,
            arrowprops=dict(arrowstyle='->', color='green'))
ax.set_title('卖点④：均线死叉', fontsize=10)
ax.set_xticks([]); ax.set_yticks([])
fig.suptitle('卖点信号汇总：四种经典卖出形态', fontsize=12, y=1.0)
save(fig, 'vol6-13.png')

# ========== 14 多指标共振 ==========
fig, axes = plt.subplots(3, 1, figsize=(9, 6.5), dpi=130, gridspec_kw={'height_ratios':[2,1,1]})
np.random.seed(208)
n = 50
base = np.concatenate([np.linspace(12, 9, 18), np.linspace(9, 15, 20), np.linspace(15, 13, 12)])
closes = closes_from(base, 0.3)
ax = axes[0]
kline_from_close(ax, closes, 0.45)
m5 = ma(closes, 5); m10 = ma(closes, 10); m30 = ma(closes, 20)
ax.plot(np.arange(4, n), m5, color=RED, lw=1.3, label='5日')
ax.plot(np.arange(9, n), m10, color=ORANGE, lw=1.3, label='10日')
ax.plot(np.arange(19, n), m30, color=BLUE, lw=1.3, label='30日')
ax.axvline(x=20, color=PURPLE, ls=':', lw=1.5)
ax.annotate('三重共振买点', xy=(20, 10), xytext=(22, 8), fontsize=9, color=PURPLE,
            arrowprops=dict(arrowstyle='->', color=PURPLE))
ax.set_title('多指标共振：K线+均线+MACD同时发出信号，胜率最高', fontsize=11)
ax.legend(loc='upper left', fontsize=7.5, frameon=False, ncol=3)
ax.set_xticks([]); ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
# volume
ax2 = axes[1]
vol = np.concatenate([np.linspace(20, 10, 18), np.linspace(10, 40, 20), np.linspace(40, 25, 12)])
colors = [RED if closes[i] >= (closes[i-1] if i > 0 else closes[i]) else GREEN for i in range(n)]
ax2.bar(range(n), vol, color=colors, width=0.6)
ax2.axvline(x=20, color=PURPLE, ls=':', lw=1.5)
ax2.set_ylabel('成交量', fontsize=8); ax2.set_xticks([])
ax2.spines['top'].set_visible(False); ax2.spines['right'].set_visible(False)
# MACD
ax3 = axes[2]
def ema(data, n):
    k = 2.0/(n+1); out = [data[0]]
    for v in data[1:]: out.append(out[-1] + k*(v-out[-1]))
    return out
e12 = ema(closes, 12); e26 = ema(closes, 26)
dif = [(e12[i]-e26[i])*3 for i in range(n)]
dea = ema(dif, 9)
ax3.axhline(0, color='black', lw=0.8)
for i in range(n):
    bh = dif[i]-dea[i]
    c = RED if bh >= 0 else GREEN
    ax3.bar(i, bh, bottom=0, color=c, width=0.6, alpha=0.7)
ax3.axvline(x=20, color=PURPLE, ls=':', lw=1.5)
ax3.set_ylabel('MACD', fontsize=8); ax3.set_xticks([])
ax3.spines['top'].set_visible(False); ax3.spines['right'].set_visible(False)
save(fig, 'vol6-14.png')

# ========== 15 技术面与基本面结合 ==========
fig, ax = setup((9, 5.2))
ax.axis('off')
ax.set_xlim(0, 10); ax.set_ylim(0, 10)
# center circle
circle = plt.Circle((5, 5.5), 1.3, color='#FFF3E0', ec=ORANGE, lw=2, zorder=5)
ax.add_patch(circle)
ax.text(5, 5.5, '投资决策\n综合判断', ha='center', va='center', fontsize=10, fontweight='bold', zorder=6)
# left: fundamentals
box1 = patches.FancyBboxPatch((0.5, 7.2), 3.2, 2.2, boxstyle='round,pad=0.2',
                               facecolor='#F0F4FF', edgecolor=BLUE, lw=1.5)
ax.add_patch(box1)
ax.text(2.1, 8.3, '基本面（定方向）\n·行业景气度\n·公司业绩/估值\n·政策面/宏观经济\n→判断长期牛熊', ha='center', va='center', fontsize=9)
# right: technicals
box2 = patches.FancyBboxPatch((6.3, 7.2), 3.2, 2.2, boxstyle='round,pad=0.2',
                               facecolor='#FFF0F0', edgecolor=RED, lw=1.5)
ax.add_patch(box2)
ax.text(7.9, 8.3, '技术面（找时机）\n·均线排列/趋势线\n·K线形态/量能\n·MACD/指标信号\n→确定买卖点位', ha='center', va='center', fontsize=9)
# bottom: rule
box3 = patches.FancyBboxPatch((1.5, 1.2), 7, 1.8, boxstyle='round,pad=0.2',
                               facecolor='#F0FFF0', edgecolor=GREEN, lw=1.5)
ax.add_patch(box3)
ax.text(5, 2.1, '原则：方向错了，点位再准也白搭；方向对了，技术面帮你进退自如。\n基本面为主、技术面为辅——矛盾时，技术面服从基本面。',
        ha='center', va='center', fontsize=9.5, color='#333333')
# arrows
ax.annotate('', xy=(4, 6.2), xytext=(2.5, 7.2), arrowprops=dict(arrowstyle='->', color=BLUE, lw=1.5))
ax.annotate('', xy=(6, 6.2), xytext=(7.5, 7.2), arrowprops=dict(arrowstyle='->', color=RED, lw=1.5))
ax.annotate('', xy=(5, 3.0), xytext=(5, 4.2), arrowprops=dict(arrowstyle='->', color=GREEN, lw=1.5))
ax.set_title('综合运用：基本面定方向，技术面找时机', fontsize=12)
save(fig, 'vol6-15.png')

print("VOL6 NEW IMAGES DONE")
