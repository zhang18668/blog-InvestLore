# -*- coding: utf-8 -*-
"""第五册 赢家操作示例 同花顺风格红涨绿跌重绘图"""
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
MA5 = '#FF8C00'   # 5周/日均线 橙
MA10 = '#1E90FF'  # 10周/日均线 蓝
MA30 = '#9370DB'  # 30日均线 紫

def draw_kline(ax, x, o, c, h, l, width=0.45):
    color = UP if c >= o else DN
    ax.plot([x, x], [l, h], color=color, linewidth=1.4)
    bottom = min(o, c)
    height = max(abs(c - o), 0.04)
    rect = patches.Rectangle((x - width/2, bottom), width, height,
                             facecolor=color, edgecolor=color, linewidth=0.8)
    ax.add_patch(rect)

def draw_seq(ax, xs, seq, width=0.45):
    """seq: list of (o,c,h,l)"""
    for x, (o, c, h, l) in zip(xs, seq):
        draw_kline(ax, x, o, c, h, l, width)

def ma_line(ax, xs, ys, color, label=None, lw=1.6, ls='-'):
    ax.plot(xs, ys, color=color, linewidth=lw, linestyle=ls, label=label, zorder=5)

def setup(ax, xlim, ylim):
    ax.set_xlim(xlim); ax.set_ylim(ylim); ax.axis('off')

def save(fig, name):
    p = os.path.join(OUT, name)
    fig.savefig(p, dpi=150, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close(fig)
    print("saved", name)

def annot(ax, x, y, txt, dx=0.3, dy=0.3, fs=9, color='black'):
    ax.annotate(txt, xy=(x, y), xytext=(x+dx, y+dy), fontsize=fs, color=color,
                arrowprops=dict(arrowstyle='->', color=color, lw=1.0))

# ============ v5o-01 七步操作法总图（图8核心） ============
fig, ax = plt.subplots(figsize=(7, 4.2))
# 构造：底部横盘→大阳线起步→沿5周线爬升→螺旋桨→阴跌跌破→5周下穿10周
np.random.seed(1)
n = 40
price = 10 + np.zeros(n)
# 阶段1 底部横盘 0-12
price[:13] = np.linspace(10, 9.5, 13) + np.random.normal(0, 0.15, 13)
# 阶段2 拉升 13-26
price[13:27] = np.linspace(10, 22, 14) + np.random.normal(0, 0.3, 14)
# 阶段3 顶部螺旋桨 27-29
price[27:30] = [22.5, 21.5, 22.8]
# 阶段4 阴跌 30-40
price[30:] = np.linspace(21, 12, 10) + np.random.normal(0, 0.3, 10)
xs = np.arange(n)
seq = []
for i in range(n):
    c = price[i]
    o = c + np.random.uniform(-0.5, 0.5)
    h = max(o, c) + abs(np.random.normal(0.3, 0.1))
    l = min(o, c) - abs(np.random.normal(0.3, 0.1))
    seq.append((o, c, h, l))
# 第13根改成大阳线起步
seq[12] = (9.3, 12.5, 12.8, 9.1)
# 第27根螺旋桨
seq[27] = (21.8, 22.2, 25.5, 19.0)
draw_seq(ax, xs, seq)
ma5 = np.convolve(price, np.ones(5)/5, mode='valid')
ma10 = np.convolve(price, np.ones(10)/10, mode='valid')
ma_line(ax, xs[4:], ma5, MA5, lw=1.5)
ma_line(ax, xs[9:], ma10, MA10, lw=1.5)
annot(ax, 12, 12.5, '①大阳线收5周线上方 买进/持股待涨', dx=-9, dy=6, fs=8.5)
annot(ax, 20, 18, '②沿5周线爬升 一路持股做多', dx=2, dy=4, fs=8.5)
annot(ax, 27, 25.5, '③螺旋桨出现 分批卖出', dx=3, dy=0.5, fs=8.5)
annot(ax, 30, 19, '④跌破螺旋桨下影线 全部抛空', dx=1.5, dy=-4, fs=8.5)
annot(ax, 36, 15, '⑥5周下穿10周 抛弃幻想停损离场', dx=-11, dy=-4, fs=8.5)
setup(ax, (-1, 41), (7, 27))
ax.set_title('图8 重点图形共同特征与七步操作法示意图', fontsize=11)
save(fig, 'v5o-01.png')

# ============ v5o-02 大阳线起步（第一特征） ============
fig, ax = plt.subplots(figsize=(5.5, 3.2))
seq = []
for i in range(10):
    c = 10 + np.random.uniform(-0.4, 0.4)
    o = c + np.random.uniform(-0.3, 0.3)
    seq.append((o, c, max(o,c)+0.4, min(o,c)-0.4))
seq.append((9.2, 12.6, 13.0, 9.0))  # 大阳线
draw_seq(ax, np.arange(11), seq)
ma = np.array([10+i*0.05 for i in range(11)])
ma_line(ax, np.arange(11), ma, MA5)
annot(ax, 10, 13.0, '①大阳线收于5周均线上方\n买进或持股待涨', dx=-4.5, dy=0.8, fs=9)
setup(ax, (-1, 12), (8.5, 14))
ax.set_title('第一特征：低位大阳线起步', fontsize=11)
save(fig, 'v5o-02.png')

# ============ v5o-03 沿5周均线爬升（第二特征+②） ============
fig, ax = plt.subplots(figsize=(5.5, 3.2))
xs = np.arange(18)
price = np.linspace(10, 20, 18) + np.random.normal(0, 0.4, 18)
seq = [(p+np.random.uniform(-0.4,0.4), p, p+0.5, p-0.5) for p in price]
draw_seq(ax, xs, seq)
ma = np.linspace(9.5, 19.5, 18)
ma_line(ax, xs, ma, MA5)
annot(ax, 9, 15, '②沿5周均线往上爬升\n一路持股做多', dx=-3, dy=-3, fs=9)
setup(ax, (-1, 19), (8, 22))
ax.set_title('第二特征：沿5周均线爬升', fontsize=11)
save(fig, 'v5o-03.png')

# ============ v5o-04 螺旋桨见顶（第三特征+③） ============
fig, ax = plt.subplots(figsize=(5.5, 3.2))
xs = np.arange(14)
price = np.linspace(10, 21, 14) + np.random.normal(0, 0.35, 14)
seq = [(p+np.random.uniform(-0.3,0.3), p, p+0.5, p-0.5) for p in price]
seq[-1] = (21.2, 21.5, 25.0, 18.5)  # 螺旋桨
draw_seq(ax, xs, seq)
annot(ax, 13, 25, '③螺旋桨K线\n分批卖出，留鱼头鱼尾给他人', dx=-6, dy=0, fs=9)
setup(ax, (-1, 15), (8, 26))
ax.set_title('第三特征：高位螺旋桨', fontsize=11)
save(fig, 'v5o-04.png')

# ============ v5o-05 跌破螺旋桨下影线（第四特征+④） ============
fig, ax = plt.subplots(figsize=(5.5, 3.2))
seq = [(21.2,21.5,25.0,18.5), (20,18.5,21,17.8)]
xs = [0,1]
# 前置小K线
pre = [(20,20.5,21,19.5)]*2
seq = pre + seq
draw_seq(ax, np.arange(4), seq)
annot(ax, 1, 25, '③螺旋桨', dx=-1.5, dy=0.5, fs=9)
annot(ax, 3, 17.8, '④阴线跌破螺旋桨下影线\n全部抛空出局', dx=-3.5, dy=-2.5, fs=9)
setup(ax, (-1, 4.5), (16, 26))
ax.set_title('第四特征：跌破螺旋桨下影线', fontsize=11)
save(fig, 'v5o-05.png')

# ============ v5o-06 5周下穿10周（第五特征+⑥⑦） ============
fig, ax = plt.subplots(figsize=(5.5, 3.2))
xs = np.arange(20)
price = np.concatenate([np.linspace(22,18,8), np.linspace(18,12,12)]) + np.random.normal(0,0.3,20)
seq = [(p+np.random.uniform(-0.3,0.3),p,p+0.4,p-0.4) for p in price]
draw_seq(ax, xs, seq)
ma5 = np.convolve(price, np.ones(5)/5, mode='valid')
ma10 = np.convolve(price, np.ones(10)/10, mode='valid')
ma_line(ax, xs[4:], ma5, MA5)
ma_line(ax, xs[9:], ma10, MA10)
annot(ax, 10, 16, '⑤5周均线调头向下\n抓紧出货', dx=0.5, dy=-2, fs=9)
annot(ax, 15, 13, '⑥5周下穿10周且10周调头向下\n抛弃幻想，及时停损', dx=-7, dy=0.5, fs=9)
setup(ax, (-1, 21), (10, 23))
ax.set_title('第五特征：5周均线下穿10周均线', fontsize=11)
save(fig, 'v5o-06.png')

# ============ v5o-07 矩形箱体（图10/11） ============
fig, ax = plt.subplots(figsize=(6, 3.4))
np.random.seed(7)
n = 26
top, bot = 15, 12
price = []
for i in range(n):
    t = i % 6
    if t < 3:
        price.append(12 + (t*1.0) + np.random.uniform(-0.2,0.2))
    else:
        price.append(15 - ((t-3)*1.0) + np.random.uniform(-0.2,0.2))
seq = [(p+np.random.uniform(-0.25,0.25), p, p+0.35, p-0.35) for p in price]
xs = np.arange(n)
draw_seq(ax, xs, seq)
ax.axhline(15.3, color='gray', ls='--', lw=1.2)
ax.axhline(11.7, color='gray', ls='--', lw=1.2)
ax.text(25.5, 15.3, '上边线(压力)', fontsize=8, va='bottom')
ax.text(25.5, 11.7, '下边线(支撑)', fontsize=8, va='top')
setup(ax, (-1, 29), (11, 16.5))
ax.set_title('矩形箱体：在前一高点与前一低点之间来回震荡', fontsize=10.5)
save(fig, 'v5o-07.png')

# ============ v5o-08 矩形跌破下边线→卖出（图12） ============
fig, ax = plt.subplots(figsize=(6, 3.4))
np.random.seed(8)
n = 30
price = [12+(i%5)*0.7 if i%5<3 else 15-((i%5-3)*0.7) for i in range(24)]
price = [p+np.random.uniform(-0.2,0.2) for p in price]
price += [11.6, 10.8, 9.5, 8.8, 8.0, 7.2]
seq = [(p+np.random.uniform(-0.25,0.25), p, p+0.35, p-0.35) for p in price]
xs = np.arange(len(price))
draw_seq(ax, xs, seq)
ax.axhline(15.3, color='gray', ls='--', lw=1.1)
ax.axhline(11.7, color='gray', ls='--', lw=1.1)
annot(ax, 25, 10.8, '跌破矩形下边线\n立即抛空离场', dx=-6, dy=-2, fs=9)
setup(ax, (-1, len(price)), (6, 16.5))
ax.set_title('图12 矩形向下突破：跌破支撑线后卖出', fontsize=10.5)
save(fig, 'v5o-08.png')

# ============ v5o-09 矩形假突破→停损（图13） ============
fig, ax = plt.subplots(figsize=(6, 3.4))
np.random.seed(9)
price = [12+(i%5)*0.7 if i%5<3 else 15-((i%5-3)*0.7) for i in range(22)]
price = [p+np.random.uniform(-0.2,0.2) for p in price]
price += [15.6, 16.6, 15.2, 13.5, 12.0, 10.5]  # 假突破上边线再跌回
seq = [(p+np.random.uniform(-0.25,0.25), p, p+0.35, p-0.35) for p in price]
xs = np.arange(len(price))
draw_seq(ax, xs, seq)
ax.axhline(15.3, color='gray', ls='--', lw=1.1)
ax.axhline(11.7, color='gray', ls='--', lw=1.1)
annot(ax, 23, 16.6, '假突破上边线', dx=-5, dy=0.5, fs=9)
annot(ax, 26, 13.5, '大阴线跌回矩形内\n立即停损离场', dx=-6, dy=-2.5, fs=9)
setup(ax, (-1, len(price)), (9, 18))
ax.set_title('图13 矩形假突破：突破上边线后跌回，停损离场', fontsize=10.5)
save(fig, 'v5o-09.png')

# ============ v5o-10 断头铡刀（图17/18） ============
fig, ax = plt.subplots(figsize=(6, 3.4))
xs = np.arange(16)
price = np.concatenate([np.linspace(18,21,10), np.linspace(21,12,6)]) + np.random.normal(0,0.25,16)
seq = [(p+np.random.uniform(-0.25,0.25),p,p+0.3,p-0.3) for p in price]
seq[10] = (21, 15.5, 21.3, 15.2)  # 断头铡刀
draw_seq(ax, xs, seq)
ma5 = np.convolve(price, np.ones(5)/5, mode='valid')
ma10 = np.convolve(price, np.ones(10)/10, mode='valid')
ma_line(ax, xs[4:], ma5, MA5)
ma_line(ax, xs[9:], ma10, MA10)
annot(ax, 10, 15.5, '断头铡刀：一根长阴线\n同时切断多根均线，坚决退出', dx=-8, dy=-1.5, fs=9)
setup(ax, (-1, 17), (10, 22.5))
ax.set_title('断头铡刀：典型做空信号，杀伤力不可小视', fontsize=10.5)
save(fig, 'v5o-10.png')

# ============ v5o-11 周均线向下发散（图19/20） ============
fig, ax = plt.subplots(figsize=(6, 3.4))
xs = np.arange(20)
price = np.concatenate([np.linspace(20,22,8), np.linspace(22,10,12)]) + np.random.normal(0,0.4,20)
seq = [(p+np.random.uniform(-0.3,0.3),p,p+0.4,p-0.4) for p in price]
draw_seq(ax, xs, seq)
ma5 = np.convolve(price, np.ones(5)/5, mode='valid')
ma10 = np.convolve(price, np.ones(10)/10, mode='valid')
ma30 = np.convolve(price, np.ones(15)/15, mode='valid')
ma_line(ax, xs[4:], ma5, MA5)
ma_line(ax, xs[9:], ma10, MA10)
ma_line(ax, xs[14:], ma30, MA30)
annot(ax, 15, 13, '周均线向下发散\n犹如重磅炸弹，躲之不及', dx=-8, dy=0.5, fs=9)
setup(ax, (-1, 21), (8, 23.5))
ax.set_title('周均线向下发散：飞流直下，多方体无完肤', fontsize=10.5)
save(fig, 'v5o-11.png')

# ============ v5o-12 银山谷（信号1） ============
fig, ax = plt.subplots(figsize=(6, 3.2))
xs = np.arange(22)
price = np.concatenate([np.linspace(15,11,9), np.linspace(11,16,13)]) + np.random.normal(0,0.3,22)
seq = [(p+np.random.uniform(-0.3,0.3),p,p+0.4,p-0.4) for p in price]
draw_seq(ax, xs, seq)
ma5 = np.convolve(price, np.ones(5)/5, mode='valid')
ma10 = np.convolve(price, np.ones(10)/10, mode='valid')
ma30 = np.convolve(price, np.ones(15)/15, mode='valid')
ma_line(ax, xs[4:], ma5, MA5)
ma_line(ax, xs[9:], ma10, MA10)
ma_line(ax, xs[14:], ma30, MA30)
annot(ax, 11, 11.5, '银山谷：5日/10日/30日均线\n低位交叉向上，激进者积极做多', dx=-2, dy=1.5, fs=9)
setup(ax, (-1, 23), (9, 17.5))
ax.set_title('银山谷：见底做多信号（激进型）', fontsize=10.5)
save(fig, 'v5o-12.png')

# ============ v5o-13 金山谷（信号6） ============
fig, ax = plt.subplots(figsize=(6, 3.2))
xs = np.arange(26)
price = np.concatenate([np.linspace(15,11,8), np.linspace(11,13.5,5),
                        np.linspace(13.5,12,3), np.linspace(12,18,10)]) + np.random.normal(0,0.25,26)
seq = [(p+np.random.uniform(-0.25,0.25),p,p+0.35,p-0.35) for p in price]
draw_seq(ax, xs, seq)
ma5 = np.convolve(price, np.ones(5)/5, mode='valid')
ma10 = np.convolve(price, np.ones(10)/10, mode='valid')
ma30 = np.convolve(price, np.ones(15)/15, mode='valid')
ma_line(ax, xs[4:], ma5, MA5)
ma_line(ax, xs[9:], ma10, MA10)
ma_line(ax, xs[14:], ma30, MA30)
annot(ax, 19, 13.5, '金山谷：银山谷之后再次出现\n稳健型投资者买进', dx=-4, dy=2, fs=9)
setup(ax, (-1, 27), (10, 19))
ax.set_title('金山谷：多头确认信号（稳健型）', fontsize=10.5)
save(fig, 'v5o-13.png')

# ============ v5o-14 死亡谷（信号9） ============
fig, ax = plt.subplots(figsize=(6, 3.2))
xs = np.arange(24)
price = np.concatenate([np.linspace(11,16,10), np.linspace(16,10,14)]) + np.random.normal(0,0.3,24)
seq = [(p+np.random.uniform(-0.3,0.3),p,p+0.4,p-0.4) for p in price]
draw_seq(ax, xs, seq)
ma5 = np.convolve(price, np.ones(5)/5, mode='valid')
ma10 = np.convolve(price, np.ones(10)/10, mode='valid')
ma30 = np.convolve(price, np.ones(15)/15, mode='valid')
ma_line(ax, xs[4:], ma5, MA5)
ma_line(ax, xs[9:], ma10, MA10)
ma_line(ax, xs[14:], ma30, MA30)
annot(ax, 13, 14, '死亡谷：高位三均线交叉向下\n果断抛空离场，保住胜利成果', dx=-3, dy=1.5, fs=9)
setup(ax, (-1, 25), (9, 17.5))
ax.set_title('死亡谷：见顶做空信号', fontsize=10.5)
save(fig, 'v5o-14.png')

# ============ v5o-15 多头排列 ============
fig, ax = plt.subplots(figsize=(6, 3.2))
xs = np.arange(20)
price = np.linspace(10, 20, 20) + np.random.normal(0,0.35,20)
seq = [(p+np.random.uniform(-0.3,0.3),p,p+0.4,p-0.4) for p in price]
draw_seq(ax, xs, seq)
ma5 = np.linspace(11, 19, 20)
ma10 = np.linspace(10.5, 18, 20)
ma30 = np.linspace(9.5, 16.5, 20)
ma_line(ax, xs, ma5, MA5, '5日均线')
ma_line(ax, xs, ma10, MA10, '10日均线')
ma_line(ax, xs, ma30, MA30, '30日均线')
ax.legend(loc='upper left', fontsize=8)
annot(ax, 10, 15, '多头排列：短期均线在上\n长期均线在下，向上发散\n增仓跟进', dx=0.5, dy=-3, fs=9)
setup(ax, (-1, 21), (8, 21.5))
ax.set_title('多头排列：强势上升格局', fontsize=10.5)
save(fig, 'v5o-15.png')

# ============ v5o-16 空头排列 ============
fig, ax = plt.subplots(figsize=(6, 3.2))
xs = np.arange(20)
price = np.linspace(20, 10, 20) + np.random.normal(0,0.35,20)
seq = [(p+np.random.uniform(-0.3,0.3),p,p+0.4,p-0.4) for p in price]
draw_seq(ax, xs, seq)
ma5 = np.linspace(19, 11, 20)
ma10 = np.linspace(19.5, 12, 20)
ma30 = np.linspace(20.5, 13.5, 20)
ma_line(ax, xs, ma5, MA5, '5日均线')
ma_line(ax, xs, ma10, MA10, '10日均线')
ma_line(ax, xs, ma30, MA30, '30日均线')
ax.legend(loc='upper right', fontsize=8)
annot(ax, 8, 15, '空头排列：短期均线在下\n长期均线在上，向下发散\n持币观望是上策', dx=0.5, dy=1.5, fs=9)
setup(ax, (-1, 21), (8, 21.5))
ax.set_title('空头排列：弱势下跌格局', fontsize=10.5)
save(fig, 'v5o-16.png')

# ============ v5o-17 再次交叉向上发散形（信号4/7） ============
fig, ax = plt.subplots(figsize=(6, 3.2))
xs = np.arange(24)
price = np.concatenate([np.linspace(14,11,7), np.linspace(11,12.5,4),
                        np.linspace(12.5,11.5,3), np.linspace(11.5,17,10)]) + np.random.normal(0,0.25,24)
seq = [(p+np.random.uniform(-0.25,0.25),p,p+0.35,p-0.35) for p in price]
draw_seq(ax, xs, seq)
ma5 = np.convolve(price, np.ones(5)/5, mode='valid')
ma10 = np.convolve(price, np.ones(10)/10, mode='valid')
ma30 = np.convolve(price, np.ones(15)/15, mode='valid')
ma_line(ax, xs[4:], ma5, MA5)
ma_line(ax, xs[9:], ma10, MA10)
ma_line(ax, xs[14:], ma30, MA30)
annot(ax, 16, 13, '再次交叉向上发散形\n挑选后来居上的股票买进', dx=-3, dy=1.5, fs=9)
setup(ax, (-1, 25), (10, 18))
ax.set_title('再次交叉向上发散形：加码做多信号', fontsize=10.5)
save(fig, 'v5o-17.png')

# ============ v5o-18 上山爬坡形（信号8） ============
fig, ax = plt.subplots(figsize=(6, 3.2))
xs = np.arange(22)
price = np.linspace(10, 18, 22) + np.random.normal(0,0.2,22)
seq = [(p+np.random.uniform(-0.2,0.2),p,p+0.3,p-0.3) for p in price]
draw_seq(ax, xs, seq)
ma5 = np.linspace(9.5, 17.5, 22)
ma10 = np.linspace(9.2, 17, 22)
ma30 = np.linspace(8.8, 16.2, 22)
ma_line(ax, xs, ma5, MA5)
ma_line(ax, xs, ma10, MA10)
ma_line(ax, xs, ma30, MA30)
annot(ax, 11, 14, '上山爬坡形：均线沿山坡向上\n继续持股待涨', dx=-3, dy=-2, fs=9)
setup(ax, (-1, 23), (8, 19))
ax.set_title('上山爬坡形：稳健上升', fontsize=10.5)
save(fig, 'v5o-18.png')

# ============ v5o-19 两黑夹一红（信号3） ============
fig, ax = plt.subplots(figsize=(5, 3.0))
xs = np.arange(12)
price = np.linspace(10, 17, 12) + np.random.normal(0,0.3,12)
seq = [(p+np.random.uniform(-0.3,0.3),p,p+0.4,p-0.4) for p in price]
seq[8] = (16.5,17.2,17.5,16.3)   # 红
seq[7] = (16.2,15.6,16.5,15.4)   # 黑
seq[9] = (17.2,16.3,17.4,16.0)   # 黑
draw_seq(ax, xs, seq)
annot(ax, 8, 17.5, '两黑夹一红\n短期乖离率过大\n分批卖出涨幅过大的股票', dx=-4, dy=0.5, fs=9)
setup(ax, (-1, 13), (9, 19))
ax.set_title('两黑夹一红：见顶信号', fontsize=10.5)
save(fig, 'v5o-19.png')

# ============ v5o-20 双顶（信号11） ============
fig, ax = plt.subplots(figsize=(6, 3.2))
xs = np.arange(24)
price = np.concatenate([np.linspace(10,18,7), np.linspace(18,15,4),
                        np.linspace(15,18.5,4), np.linspace(18.5,11,9)]) + np.random.normal(0,0.3,24)
seq = [(p+np.random.uniform(-0.3,0.3),p,p+0.4,p-0.4) for p in price]
draw_seq(ax, xs, seq)
ax.axhline(18, color='gray', ls='--', lw=1.0)
annot(ax, 6, 18.3, '第一个顶', dx=-1, dy=0.3, fs=9)
annot(ax, 15, 18.8, '第二个顶(双顶嫌疑)\n大阴线吞许多K线\n分批卖出甚至全部抛空', dx=-4, dy=-2.5, fs=9)
setup(ax, (-1, 25), (9, 20))
ax.set_title('双顶：头部形成，卖出信号', fontsize=10.5)
save(fig, 'v5o-20.png')

# ============ v5o-21 上升趋势线支撑 ============
fig, ax = plt.subplots(figsize=(6, 3.2))
xs = np.arange(20)
price = np.linspace(10, 19, 20) + np.random.normal(0,0.4,20)
seq = [(p+np.random.uniform(-0.35,0.35),p,p+0.5,p-0.5) for p in price]
draw_seq(ax, xs, seq)
ax.plot([1, 19], [9.5, 18.5], color='blue', lw=1.6)
annot(ax, 10, 13.5, '上升趋势线：勇于看多加做多\n回踩趋势线不破即可持股', dx=-3, dy=-2, fs=9)
setup(ax, (-1, 21), (8, 20.5))
ax.set_title('上升趋势线：支撑有效，持股做多', fontsize=10.5)
save(fig, 'v5o-21.png')

# ============ v5o-22 下降趋势线压制 ============
fig, ax = plt.subplots(figsize=(6, 3.2))
xs = np.arange(20)
price = np.linspace(19, 10, 20) + np.random.normal(0,0.4,20)
seq = [(p+np.random.uniform(-0.35,0.35),p,p+0.5,p-0.5) for p in price]
draw_seq(ax, xs, seq)
ax.plot([1, 19], [18.5, 11.5], color='red', lw=1.6)
annot(ax, 10, 16, '下降趋势线：坚定看空加做空\n反弹至趋势线下方即卖出', dx=-3, dy=1.5, fs=9)
setup(ax, (-1, 21), (8.5, 20))
ax.set_title('下降趋势线：压制有效，持币做空', fontsize=10.5)
save(fig, 'v5o-22.png')

# ============ v5o-23 空头陷阱（图41） ============
fig, ax = plt.subplots(figsize=(6, 3.2))
xs = np.arange(24)
price = np.concatenate([np.linspace(11,15,10), np.linspace(15,12.5,4),
                        np.linspace(12.5,18,10)]) + np.random.normal(0,0.3,24)
seq = [(p+np.random.uniform(-0.3,0.3),p,p+0.4,p-0.4) for p in price]
draw_seq(ax, xs, seq)
ma30 = np.linspace(10.5, 17.5, 24)
ma_line(ax, xs, ma30, MA30)
annot(ax, 13, 12.5, '空头陷阱：长期均线向上\n股价短暂下跌后再度回升\n不可盲目看空', dx=-3, dy=-2.5, fs=9)
setup(ax, (-1, 25), (10, 19))
ax.set_title('空头陷阱：下跌是假象，趋势仍向上', fontsize=10.5)
save(fig, 'v5o-23.png')

# ============ v5o-24 多头陷阱（图42） ============
fig, ax = plt.subplots(figsize=(6, 3.2))
xs = np.arange(24)
price = np.concatenate([np.linspace(18,14,10), np.linspace(14,16.5,4),
                        np.linspace(16.5,11,10)]) + np.random.normal(0,0.3,24)
seq = [(p+np.random.uniform(-0.3,0.3),p,p+0.4,p-0.4) for p in price]
draw_seq(ax, xs, seq)
ma30 = np.linspace(18.5, 11.5, 24)
ma_line(ax, xs, ma30, MA30)
annot(ax, 13, 16.5, '多头陷阱：长期均线向下\n股价短暂上涨后再度大跌\n不可盲目看多', dx=-3, dy=1, fs=9)
setup(ax, (-1, 25), (10, 19.5))
ax.set_title('多头陷阱：上涨是假象，趋势仍向下', fontsize=10.5)
save(fig, 'v5o-24.png')

# ============ v5o-25 下降覆盖线+断头铡刀（图44） ============
fig, ax = plt.subplots(figsize=(6, 3.2))
xs = np.arange(18)
price = np.concatenate([np.linspace(10,19,11), np.linspace(19,12,7)]) + np.random.normal(0,0.3,18)
seq = [(p+np.random.uniform(-0.3,0.3),p,p+0.4,p-0.4) for p in price]
seq[12] = (18.8,16.5,19.2,16.2)  # 下降覆盖线/断头铡刀
draw_seq(ax, xs, seq)
ma5 = np.convolve(price, np.ones(5)/5, mode='valid')
ma10 = np.convolve(price, np.ones(10)/10, mode='valid')
ma_line(ax, xs[4:], ma5, MA5)
ma_line(ax, xs[9:], ma10, MA10)
annot(ax, 12, 16.5, '下降覆盖线→断头铡刀\n多方形势已不妙\n多翻空离场', dx=-7, dy=-1.5, fs=9)
setup(ax, (-1, 19), (10, 20))
ax.set_title('下降覆盖线后现断头铡刀：跌势确立', fontsize=10.5)
save(fig, 'v5o-25.png')

# ============ v5o-26 趋势线综合画法（图47/48） ============
fig, ax = plt.subplots(figsize=(7, 3.6))
xs = np.arange(30)
np.random.seed(2)
price = np.concatenate([np.linspace(10,16,8), np.linspace(16,13,5),
                        np.linspace(13,18,5), np.linspace(18,10,12)]) + np.random.normal(0,0.4,30)
seq = [(p+np.random.uniform(-0.35,0.35),p,p+0.5,p-0.5) for p in price]
draw_seq(ax, xs, seq)
ax.plot([2, 12], [10.5, 15.5], color='blue', lw=1.6)
ax.plot([15, 29], [17.5, 11.5], color='red', lw=1.6)
ax.text(6, 13, '上升趋势线', color='blue', fontsize=9, rotation=20)
ax.text(22, 15, '下降趋势线', color='red', fontsize=9, rotation=-20)
annot(ax, 18, 15.5, '趋势线相交处变盘\n线之上做多，线之下做空', dx=0.5, dy=-3, fs=9)
setup(ax, (-1, 31), (9, 19))
ax.set_title('上升趋势线与下降趋势线：炒股"交通规则"', fontsize=10.5)
save(fig, 'v5o-26.png')

# ============ v5o-27 螺旋桨特写 ============
fig, ax = plt.subplots(figsize=(3.5, 3.2))
draw_kline(ax, 0, 10, 10.5, 13.5, 7.0, width=0.5)
annot(ax, 0, 13.5, '螺旋桨：\n实体小，上下影线长\n高位见顶信号', dx=-2.5, dy=0, fs=9)
setup(ax, (-3, 2), (6, 14.5))
ax.set_title('螺旋桨K线', fontsize=11)
save(fig, 'v5o-27.png')

# ============ v5o-28 银山谷vs死亡谷 对照 ============
fig, axes = plt.subplots(1, 2, figsize=(8, 3.2))
# 左：银山谷
ax = axes[0]
xs = np.arange(18)
p = np.concatenate([np.linspace(14,10,7), np.linspace(10,15,11)]) + np.random.normal(0,0.25,18)
sq = [(q+np.random.uniform(-0.25,0.25),q,q+0.3,q-0.3) for q in p]
draw_seq(ax, xs, sq)
m5 = np.convolve(p, np.ones(5)/5, mode='valid')
m10 = np.convolve(p, np.ones(10)/10, mode='valid')
ma_line(ax, xs[4:], m5, MA5); ma_line(ax, xs[9:], m10, MA10)
ax.set_title('银山谷（买）', fontsize=10)
setup(ax, (-1, 19), (9, 16))
# 右：死亡谷
ax = axes[1]
p2 = np.concatenate([np.linspace(10,15,7), np.linspace(15,10,11)]) + np.random.normal(0,0.25,18)
sq2 = [(q+np.random.uniform(-0.25,0.25),q,q+0.3,q-0.3) for q in p2]
draw_seq(ax, xs, sq2)
m5 = np.convolve(p2, np.ones(5)/5, mode='valid')
m10 = np.convolve(p2, np.ones(10)/10, mode='valid')
ma_line(ax, xs[4:], m5, MA5); ma_line(ax, xs[9:], m10, MA10)
ax.set_title('死亡谷（卖）', fontsize=10)
setup(ax, (-1, 19), (9, 16))
fig.suptitle('银山谷与死亡谷：底部金叉 vs 顶部死叉', fontsize=11)
save(fig, 'v5o-28.png')

print("ALL DONE")
