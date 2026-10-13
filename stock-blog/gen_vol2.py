# -*- coding: utf-8 -*-
"""Generate vol2 technical-indicator diagrams (red-up / green-down)."""
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

# ---------- helper: build a synthetic close series ----------
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

# ========== 01 多头排列 vs 空头排列 ==========
fig, axes = plt.subplots(1, 2, figsize=(11, 4.2), dpi=130)
# bull
n = 40
trend = np.linspace(10, 22, n)
closes = closes_from(trend, 0.8)
x = np.arange(n)
for ax, title, cc, color in [
    (axes[0], '多头排列（短上长下，向上）', closes, RED),
]:
    kline_from_close(ax, cc, 0.55)
    for nn, col, lab in [(5, RED, '5日线'), (10, ORANGE, '10日线'), (30, BLUE, '30日线')]:
        ma = np.convolve(cc, np.ones(nn)/nn, mode='valid')
        ax.plot(np.arange(nn-1, n), ma, color=col, linewidth=1.6, label=lab)
    ax.set_title(title, fontsize=12)
    ax.legend(loc='upper left', fontsize=8, frameon=False)
    ax.set_xticks([]); ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
# bear
trend2 = np.linspace(22, 10, n)
closes2 = closes_from(trend2, 0.8)
kline_from_close(axes[1], closes2, 0.55)
for nn, col, lab in [(5, RED, '5日线'), (10, ORANGE, '10日线'), (30, BLUE, '30日线')]:
    ma = np.convolve(closes2, np.ones(nn)/nn, mode='valid')
    axes[1].plot(np.arange(nn-1, n), ma, color=col, linewidth=1.6, label=lab)
axes[1].set_title('空头排列（长上短下，向下）', fontsize=12)
axes[1].legend(loc='upper right', fontsize=8, frameon=False)
axes[1].set_xticks([]); axes[1].spines['top'].set_visible(False); axes[1].spines['right'].set_visible(False)
fig.suptitle('均线的多头排列与空头排列', fontsize=13, y=1.02)
save(fig, 'vol2-01.png')

# ========== 02 金叉 死叉 ==========
fig, axes = plt.subplots(1, 2, figsize=(11, 4.2), dpi=130)
# golden cross: bottom turning up
n=50
base = np.concatenate([np.linspace(15,9,20), np.linspace(9,18,30)])
closes = closes_from(base, 0.7)
short = np.convolve(closes, np.ones(5)/5, mode='valid')
long_ = np.convolve(closes, np.ones(20)/20, mode='valid')
ax = axes[0]
kline_from_close(ax, closes, 0.5)
ax.plot(np.arange(4,n), short, color=RED, linewidth=1.6, label='短期均线')
ax.plot(np.arange(19,n), long_, color=BLUE, linewidth=1.6, label='长期均线')
# find cross
cross_x = None
for i in range(1,len(short)):
    si = i+4; li = i+19
    if si < n and li < n:
        if short[i-1] <= long_[i-1] and short[i] > long_[i]:
            cross_x = si; cross_y = short[i]
if cross_x:
    ax.scatter([cross_x],[cross_y], color='black', zorder=5, s=40)
    ax.annotate('黄金交叉\n(买入)', xy=(cross_x, cross_y), xytext=(cross_x+6, cross_y-4),
                fontsize=9, arrowprops=dict(arrowstyle='->', color='black'))
ax.set_title('黄金交叉：短均线上穿长均线', fontsize=12)
ax.legend(loc='upper left', fontsize=8, frameon=False)
ax.set_xticks([]); ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
# dead cross
base2 = np.concatenate([np.linspace(10,18,20), np.linspace(18,9,30)])
closes2 = closes_from(base2, 0.7)
short2 = np.convolve(closes2, np.ones(5)/5, mode='valid')
long2 = np.convolve(closes2, np.ones(20)/20, mode='valid')
ax = axes[1]
kline_from_close(ax, closes2, 0.5)
ax.plot(np.arange(4,n), short2, color=RED, linewidth=1.6, label='短期均线')
ax.plot(np.arange(19,n), long2, color=BLUE, linewidth=1.6, label='长期均线')
cross_x=None
for i in range(1,len(short2)):
    si=i+4; li=i+19
    if si<n and li<n:
        if short2[i-1] >= long2[i-1] and short2[i] < long2[i]:
            cross_x=si; cross_y=short2[i]
if cross_x:
    ax.scatter([cross_x],[cross_y], color='black', zorder=5, s=40)
    ax.annotate('死亡交叉\n(卖出)', xy=(cross_x,cross_y), xytext=(cross_x+6,cross_y+3),
                fontsize=9, arrowprops=dict(arrowstyle='->', color='black'))
ax.set_title('死亡交叉：短均线下穿长均线', fontsize=12)
ax.legend(loc='upper right', fontsize=8, frameon=False)
ax.set_xticks([]); ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
save(fig, 'vol2-02.png')

# ========== 03 银山谷/金山谷/死亡谷 ==========
fig, ax = setup((9,4.6))
base = np.concatenate([np.linspace(14,9,15), np.linspace(9,12,10), np.linspace(12,9.5,8), np.linspace(9.5,18,19)])
n=len(base)
closes = closes_from(base,0.55)
kline_from_close(ax, closes, 0.45)
ma5 = np.convolve(closes, np.ones(5)/5, mode='valid')
ma10 = np.convolve(closes, np.ones(10)/10, mode='valid')
ma30 = np.convolve(closes, np.ones(20)/20, mode='valid')
ax.plot(np.arange(4,n), ma5, color=RED, linewidth=1.5, label='5日')
ax.plot(np.arange(9,n), ma10, color=ORANGE, linewidth=1.5, label='10日')
ax.plot(np.arange(19,n), ma30, color=BLUE, linewidth=1.5, label='30日')
ax.annotate('银山谷(初次探路)', xy=(16,9.2), xytext=(8,6.5), fontsize=9,
            arrowprops=dict(arrowstyle='->', color='black'))
ax.annotate('金山谷(二次确认)', xy=(40,10.2), xytext=(38,6.5), fontsize=9,
            arrowprops=dict(arrowstyle='->', color='black'))
ax.set_title('银山谷与金山谷：三线在低位先后向上交叉', fontsize=12)
ax.legend(loc='upper left', fontsize=8, frameon=False)
ax.set_xticks([])
save(fig, 'vol2-03.png')

# ========== 04 蛟龙出海 vs 断头铡刀 ==========
fig, axes = plt.subplots(1,2, figsize=(11,4.2), dpi=130)
np.random.seed(3)
n=25
base=np.linspace(12,11,n)
closes=closes_from(base,0.3)
# final big yang line crosses above all
closes[-1]=13.5
ax=axes[0]
kline_from_close(ax, closes,0.5)
for nn,col,lab in [(5,RED,'5日'),(10,ORANGE,'10日'),(20,BLUE,'20日')]:
    ma=np.convolve(closes,np.ones(nn)/nn,mode='valid')
    ax.plot(np.arange(nn-1,n),ma,color=col,linewidth=1.4,label=lab)
ax.axhline(11,color='grey',ls=':',lw=0.8)
ax.annotate('蛟龙出海：一根大阳线\n同时上穿多根均线', xy=(n-1,13.5), xytext=(n-12,14.5),
            fontsize=9, arrowprops=dict(arrowstyle='->', color='black'))
ax.set_title('蛟龙出海（放量买入信号）', fontsize=12)
ax.legend(loc='upper left',fontsize=8,frameon=False); ax.set_xticks([])
ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
# 断头铡刀
np.random.seed(5)
base=np.linspace(12,13,n)
closes2=closes_from(base,0.3)
closes2[-1]=10.5
ax=axes[1]
kline_from_close(ax, closes2,0.5)
for nn,col,lab in [(5,RED,'5日'),(10,ORANGE,'10日'),(20,BLUE,'20日')]:
    ma=np.convolve(closes2,np.ones(nn)/nn,mode='valid')
    ax.plot(np.arange(nn-1,n),ma,color=col,linewidth=1.4,label=lab)
ax.annotate('断头铡刀：一根大阴线\n同时下穿多根均线', xy=(n-1,10.5), xytext=(n-12,9),
            fontsize=9, arrowprops=dict(arrowstyle='->', color='black'))
ax.set_title('断头铡刀（止损卖出信号）', fontsize=12)
ax.legend(loc='upper right',fontsize=8,frameon=False); ax.set_xticks([])
ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
save(fig,'vol2-04.png')

# ========== 05 上升/下降趋势线 ==========
fig, axes = plt.subplots(1,2, figsize=(11,4.4), dpi=130)
np.random.seed(11)
n=45
# uptrend: two rising lows
low_x=[5, 25]; low_y=[8, 12]
trend=np.array([low_y[0]+(low_y[1]-low_y[0])*i/(n-1) for i in range(n)])+np.array([1.5*np.sin(i/3.0) for i in range(n)])
closes=closes_from(trend,0.25)
ax=axes[0]
kline_from_close(ax,closes,0.5)
ax.plot([low_x[0],low_x[1]],[low_y[0],low_y[1]],color=BLUE,lw=2,label='上升趋势线(支撑线)')
ax.scatter(low_x,low_y,color='black',zorder=5)
ax.annotate('连接两个依次抬高的低点', xy=(15,9.5), fontsize=9, color=BLUE)
ax.set_title('上升趋势线：低点抬高，起支撑作用', fontsize=11)
ax.legend(loc='upper left',fontsize=8,frameon=False); ax.set_xticks([])
ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
# downtrend
np.random.seed(13)
high_x=[5,25]; high_y=[16,11]
trend=np.array([high_y[0]+(high_y[1]-high_y[0])*i/(n-1) for i in range(n)])-np.array([1.5*np.sin(i/3.0) for i in range(n)])
closes2=closes_from(trend,0.25)
ax=axes[1]
kline_from_close(ax,closes2,0.5)
ax.plot([high_x[0],high_x[1]],[high_y[0],high_y[1]],color=GREEN,lw=2,label='下降趋势线(压力线)')
ax.scatter(high_x,high_y,color='black',zorder=5)
ax.annotate('连接两个依次降低的高点', xy=(12,14.5), fontsize=9, color=GREEN)
ax.set_title('下降趋势线：高点降低，起压制作用', fontsize=11)
ax.legend(loc='upper right',fontsize=8,frameon=False); ax.set_xticks([])
ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
save(fig,'vol2-05.png')

# ========== 06 趋势线突破后 支撑变压力 ==========
fig, ax = setup((9,4.6))
np.random.seed(21)
n=55
low_x=[8,22]; low_y=[8,11]
trend=np.array([low_y[0]+(low_y[1]-low_y[0])*i/(n-1) for i in range(n)])+np.array([1.2*np.sin(i/2.5) for i in range(n)])
# after break, drop
for i in range(35,n):
    trend[i]=11.5-(i-35)*0.25
closes=closes_from(trend,0.3)
kline_from_close(ax,closes,0.5)
# original support line extended
xs=np.array([low_x[0],48]); ys=np.array([low_y[0], low_y[0]+(low_y[1]-low_y[0])*(48-low_x[0])/(low_x[1]-low_x[0])])
ax.plot(xs,ys,color=BLUE,lw=1.6,ls='-',label='原上升趋势线(支撑)')
# broken point
bx=35; by=low_y[0]+(low_y[1]-low_y[0])*(35-low_x[0])/(low_x[1]-low_x[0])
ax.scatter([bx],[by],color='red',zorder=6,s=50)
ax.annotate('有效跌破\n支撑变压力', xy=(bx,by), xytext=(bx+4,by+2.5), fontsize=9,
            arrowprops=dict(arrowstyle='->', color='red'))
ax.axhline(by, xmin=0.6, xmax=0.98, color=GREY, ls=':', lw=1)
ax.set_title('趋势线被有效突破后：支撑线转为压力线', fontsize=12)
ax.legend(loc='upper left',fontsize=8,frameon=False); ax.set_xticks([])
save(fig,'vol2-06.png')

# ========== 07 量价：逐渐放量上涨 / 逐渐缩量下跌 ==========
fig, axes = plt.subplots(2,1, figsize=(9,5.6), dpi=130, gridspec_kw={'height_ratios':[2,1]})
np.random.seed(31)
n=35
trend=np.linspace(10,16,n)
closes=closes_from(trend,0.5)
vol=np.linspace(10,40,n)
ax=axes[0]
kline_from_close(ax,closes,0.5)
ax.set_title('逐渐放量推升：价涨量增，涨势有资金跟进', fontsize=11)
ax.set_xticks([])
ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
ax2=axes[1]
colors=[RED if closes[i]>= (closes[i-1] if i>0 else closes[i]) else GREEN for i in range(n)]
ax2.bar(range(n), vol, color=colors, width=0.6)
ax2.set_ylabel('成交量', fontsize=9)
ax2.set_xticks([])
ax2.spines['top'].set_visible(False); ax2.spines['right'].set_visible(False)
save(fig,'vol2-07.png')

# ========== 08 量价背离 ==========
fig, axes = plt.subplots(2,1, figsize=(9,5.6), dpi=130, gridspec_kw={'height_ratios':[2,1]})
np.random.seed(41)
n=40
# price makes higher high but volume shrinks
trend=np.concatenate([np.linspace(10,15,18), np.linspace(15,17,10), np.linspace(17,18,12)])
closes=closes_from(trend,0.5)
vol=np.concatenate([np.linspace(35,45,18), np.linspace(45,30,10), np.linspace(30,15,12)])
ax=axes[0]
kline_from_close(ax,closes,0.5)
ax.plot([8,28],[14.5,17.5],color='red',lw=1.2,ls='--')
ax.set_title('顶背离：股价一浪高过一浪，成交量却一浪比一浪小', fontsize=11)
ax.set_xticks([])
ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
ax2=axes[1]
colors=[RED if closes[i]>= (closes[i-1] if i>0 else closes[i]) else GREEN for i in range(n)]
ax2.bar(range(n),vol,color=colors,width=0.6)
ax2.plot([8,28],[42,16],color='red',lw=1.2,ls='--')
ax2.set_ylabel('成交量',fontsize=9); ax2.set_xticks([])
ax2.spines['top'].set_visible(False); ax2.spines['right'].set_visible(False)
save(fig,'vol2-08.png')

# ========== 09 MACD 金叉死叉 + O轴 ==========
fig, ax = setup((9,4.6))
np.random.seed(51)
n=60
price_trend=np.concatenate([np.linspace(12,9,18),np.linspace(9,11,12),np.linspace(11,15,18),np.linspace(15,12,12)])
closes=closes_from(price_trend,0.3)
ema12=ema(closes,12); ema26=ema(closes,26)
dif=[(ema12[i]-ema26[i])*3 for i in range(n)]
dea=ema(dif,9)
ax.axhline(0,color='black',lw=1)
ax.plot(range(n),dif,color='white',lw=1.6,label='DIF(快线)', markeredgecolor='black')
ax.plot(range(n),dif,color='black',lw=1.6)
ax.plot(range(n),dea,color='orange',lw=1.6,label='DEA(慢线)')
# bars
for i in range(n):
    bh=dif[i]-dea[i]
    c=RED if bh>=0 else GREEN
    ax.bar(i, bh, bottom=0, color=c, width=0.6, alpha=0.7)
# annotate crosses
for i in range(1,n):
    if dif[i-1]<=dea[i-1] and dif[i]>dea[i]:
        ax.annotate('金叉', xy=(i,dif[i]), xytext=(i-3,dif[i]+0.8), fontsize=9, color='red',
                    arrowprops=dict(arrowstyle='->',color='red'))
    if dif[i-1]>=dea[i-1] and dif[i]<dea[i]:
        ax.annotate('死叉', xy=(i,dif[i]), xytext=(i-3,dif[i]-1.2), fontsize=9, color='green',
                    arrowprops=dict(arrowstyle='->',color='green'))
ax.text(2,1.2,'O轴上方=多头市场',fontsize=8,color='red')
ax.text(2,-1.6,'O轴下方=空头市场',fontsize=8,color='green')
ax.set_title('MACD：DIF/DEA金叉死叉与O轴多空分界', fontsize=12)
ax.legend(loc='upper left',fontsize=8,frameon=False)
ax.set_xticks([])
save(fig,'vol2-09.png')

# ========== 10 MACD 顶背离 / 底背离 ==========
fig, axes = plt.subplots(2,1, figsize=(9,5.4), dpi=130, gridspec_kw={'height_ratios':[1.3,1]})
np.random.seed(61)
n=50
# price higher highs, DIF lower highs
trend=np.concatenate([np.linspace(12,15,15),np.linspace(15,13.5,8),np.linspace(13.5,17,19),np.linspace(17,15,8)])
closes=closes_from(trend,0.35)
ema12=ema(closes,12); ema26=ema(closes,26)
dif=[(ema12[i]-ema26[i])*3 for i in range(n)]
ax=axes[0]
kline_from_close(ax,closes,0.45)
ax.plot([10,35],[14.5,16.8],color='red',ls='--',lw=1.2)
ax.set_title('顶背离：股价逐波走高，DIF/MACD却逐波走低', fontsize=11)
ax.set_xticks([]); ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
ax2=axes[1]
ax2.plot(range(n),dif,color='black',lw=1.4)
ax2.axhline(0,color='grey',lw=0.8)
ax2.plot([12,37],[1.2,0.2],color='red',ls='--',lw=1.2)
ax2.set_ylabel('DIF',fontsize=9); ax2.set_xticks([])
ax2.spines['top'].set_visible(False); ax2.spines['right'].set_visible(False)
save(fig,'vol2-10.png')

# ========== 11 MACD 红绿柱缩放 ==========
fig, axes = plt.subplots(2,1, figsize=(9,5.4), dpi=130, gridspec_kw={'height_ratios':[1.3,1]})
np.random.seed(71)
n=45
trend=np.concatenate([np.linspace(10,16,20),np.linspace(16,14,25)])
closes=closes_from(trend,0.4)
ema12=ema(closes,12); ema26=ema(closes,26)
dif=[(ema12[i]-ema26[i])*2.5 for i in range(n)]
dea=ema(dif,9)
ax=axes[0]
kline_from_close(ax,closes,0.45)
ax.set_title('红柱由多转少：多方气势衰减，股价随时可能下跌', fontsize=11)
ax.set_xticks([]); ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
ax2=axes[1]
ax2.axhline(0,color='black',lw=0.8)
for i in range(n):
    bh=dif[i]-dea[i]
    c=RED if bh>=0 else GREEN
    ax2.bar(i,bh,bottom=0,color=c,width=0.6,alpha=0.8)
ax2.set_ylabel('MACD柱',fontsize=9); ax2.set_xticks([])
ax2.spines['top'].set_visible(False); ax2.spines['right'].set_visible(False)
save(fig,'vol2-11.png')

# ========== 12 BIAS 正乖离/负乖离 超买超卖 ==========
fig, axes = plt.subplots(2,1, figsize=(9,5.4), dpi=130, gridspec_kw={'height_ratios':[1.3,1]})
np.random.seed(81)
n=55
trend=np.concatenate([np.linspace(10,13,15),np.linspace(13,10.5,10),np.linspace(10.5,14,15),np.linspace(14,11.5,15)])
closes=closes_from(trend,0.35)
closes=np.array(closes)
ma10=np.convolve(closes,np.ones(10)/10,mode='valid')
bias=[(closes[i]-(closes[max(0,i-9):i+1].mean()))/(closes[max(0,i-9):i+1].mean())*100 for i in range(n)]
ax=axes[0]
kline_from_close(ax,closes,0.45)
ax.set_title('乖离率：股价远离均线（正乖离过大易回调，负乖离过大易反弹）', fontsize=11)
ax.set_xticks([]); ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
ax2=axes[1]
ax2.axhline(0,color='black',lw=0.8)
ax2.plot(range(n),bias,color='black',lw=1.4)
ax2.axhline(8,color='red',ls='--',lw=1,label='超买区(正乖离过大)')
ax2.axhline(-8,color='green',ls='--',lw=1,label='超卖区(负乖离过大)')
ax2.set_ylabel('BIAS(%)',fontsize=9); ax2.set_xticks([])
ax2.legend(loc='upper left',fontsize=8,frameon=False)
ax2.spines['top'].set_visible(False); ax2.spines['right'].set_visible(False)
save(fig,'vol2-12.png')

print("ALL DONE")
