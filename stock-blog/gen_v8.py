# -*- coding: utf-8 -*-
"""Generate workbook (v8) rule & winner-operation diagrams (red-up / green-down)."""
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


def ema(data, n):
    k = 2.0 / (n + 1)
    out = [data[0]]
    for v in data[1:]:
        out.append(out[-1] + k * (v - out[-1]))
    return out


# ========== v8-01 一看二慢三通过 总纲 ==========
fig, ax = plt.subplots(figsize=(9, 3.4), dpi=130)
ax.axis('off')
steps = [('一看', '先看大势\n均线排列定多空', BLUE),
         ('二慢', '信号出现\n慢半拍等确认', ORANGE),
         ('三通过', '共振确认\n才动手买卖', GREEN)]
for i, (big, small, c) in enumerate(steps):
    x = 0.6 + i * 3.2
    box = patches.FancyBboxPatch((x, 0.8), 2.6, 1.6, boxstyle="round,pad=0.08",
                                 facecolor=c, edgecolor='black', alpha=0.85)
    ax.add_patch(box)
    ax.text(x+0.55, 1.6, big, ha='center', va='center', fontsize=15, color='white', fontweight='bold')
    ax.text(x+1.65, 1.6, small, ha='center', va='center', fontsize=9.5, color='white')
    if i < 2:
        ax.annotate('', xy=(x+3.05, 1.6), xytext=(x+2.65, 1.6),
                    arrowprops=dict(arrowstyle='->', lw=2, color='black'))
ax.set_xlim(0, 10.6); ax.set_ylim(0.4, 2.8)
ax.set_title('七字经总纲：一看、二慢、三通过', fontsize=13)
save(fig, 'v8-01.png')

# ========== v8-02 买入口诀对应K线 ==========
fig, axes = plt.subplots(1, 3, figsize=(11, 3.8), dpi=130)
np.random.seed(2)
cases = [('看涨吞没', 'engulf'), ('早晨之星', 'morning'), ('锤头线(低位)', 'hammer')]
for ax, (title, kind) in zip(axes, cases):
    n = 10
    base = np.linspace(13, 10, n)
    closes = closes_from(base, 0.3)
    kline_from_close(ax, closes, 0.5)
    if kind == 'engulf':
        o1, c1 = 10.2, 9.9
        o2, c2 = 9.7, 11.0
        draw_kline(ax, 8, o1, c1, 10.4, 9.6, 0.5)
        draw_kline(ax, 9, o2, c2, 11.2, 9.6, 0.5)
    elif kind == 'morning':
        draw_kline(ax, 7, 10.3, 9.9, 10.4, 9.7, 0.45)
        draw_kline(ax, 8, 9.9, 9.85, 10.0, 9.7, 0.45)
        draw_kline(ax, 9, 9.7, 10.8, 11.0, 9.6, 0.45)
    else:
        draw_kline(ax, 9, 10.1, 10.2, 10.3, 9.3, 0.5)
    ax.set_title(title, fontsize=11)
    ax.set_xticks([]); ax.set_yticks([])
    ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
fig.suptitle('买入口诀对应的经典K线形态（出现在低位/底部）', fontsize=12, y=1.03)
save(fig, 'v8-02.png')

# ========== v8-03 卖出口诀对应K线 ==========
fig, axes = plt.subplots(1, 3, figsize=(11, 3.8), dpi=130)
np.random.seed(3)
cases = [('看跌吞没', 'engulf'), ('黄昏之星', 'evening'), ('射击之星(高位)', 'shoot')]
for ax, (title, kind) in zip(axes, cases):
    n = 10
    base = np.linspace(10, 13, n)
    closes = closes_from(base, 0.3)
    kline_from_close(ax, closes, 0.5)
    if kind == 'engulf':
        draw_kline(ax, 8, 12.8, 13.1, 13.3, 12.7, 0.5)
        draw_kline(ax, 9, 13.2, 11.9, 13.3, 11.7, 0.5)
    elif kind == 'evening':
        draw_kline(ax, 7, 12.7, 13.2, 13.4, 12.6, 0.45)
        draw_kline(ax, 8, 13.2, 13.25, 13.4, 13.1, 0.45)
        draw_kline(ax, 9, 13.1, 12.0, 13.3, 11.9, 0.45)
    else:
        draw_kline(ax, 9, 12.9, 13.0, 14.3, 12.8, 0.5)
    ax.set_title(title, fontsize=11)
    ax.set_xticks([]); ax.set_yticks([])
    ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
fig.suptitle('卖出口诀对应的经典K线形态（出现在高位/顶部）', fontsize=12, y=1.03)
save(fig, 'v8-03.png')

# ========== v8-04 赢家七步操作路径 ==========
fig, ax = plt.subplots(figsize=(10, 3.6), dpi=130)
ax.axis('off')
steps = [('①观察', '看大势\n定多空', BLUE),
         ('②等待', '等信号\n不追高', ORANGE),
         ('③试探', '小仓位\n试错', PURPLE),
         ('④加仓', '确认后\n顺势加', RED),
         ('⑤持有', '趋势在\n安心拿', GREEN),
         ('⑥预警', '见顶信号\n先警觉', '#E67E22'),
         ('⑦离场', '共振逃顶\n落袋', '#C0392B')]
for i, (big, small, c) in enumerate(steps):
    x = 0.3 + i * 1.45
    box = patches.FancyBboxPatch((x, 0.9), 1.25, 1.5, boxstyle="round,pad=0.05",
                                 facecolor=c, edgecolor='black', alpha=0.88)
    ax.add_patch(box)
    ax.text(x+0.62, 1.9, big, ha='center', va='center', fontsize=10.5, color='white', fontweight='bold')
    ax.text(x+0.62, 1.25, small, ha='center', va='center', fontsize=7.5, color='white')
    if i < 6:
        ax.annotate('', xy=(x+1.45, 1.65), xytext=(x+1.27, 1.65),
                    arrowprops=dict(arrowstyle='->', lw=1.3, color='black'))
ax.set_xlim(0, 10.6); ax.set_ylim(0.5, 2.8)
ax.set_title('赢家七步操作路径：观察→等待→试探→加仓→持有→预警→离场', fontsize=12)
save(fig, 'v8-04.png')

# ========== v8-05 信号强弱排序 ==========
fig, ax = setup((9, 4.4))
labels = ['1个信号', '2个信号', '3个信号', '4个及以上']
probs = [60, 70, 80, 88]
bars = ax.bar(labels, probs, color=[GREY, ORANGE, RED, '#C0392B'], width=0.6)
for b, p in zip(bars, probs):
    ax.text(b.get_x()+b.get_width()/2, p+1.5, f'约{p}%', ha='center', fontsize=10)
ax.set_ylim(0, 100)
ax.set_ylabel('见顶/见底判断胜率（示意）', fontsize=9)
ax.set_title('信号强弱排序：信号越多、相互越独立，判断胜率越高', fontsize=12)
save(fig, 'v8-05.png')

# ========== v8-06 矩形真突破 ==========
fig, ax = setup((9, 4.6))
np.random.seed(11)
n = 34
box_top, box_bot = 13.0, 11.0
base = np.concatenate([np.linspace(11, 13, 6), np.full(16, 12.0), np.linspace(13.0, 16, 12)])
base = np.array(base, dtype=float)
base[6:22] = [12.8, 11.2, 12.9, 11.1, 12.7, 11.3, 12.9, 11.2, 12.8, 11.1, 12.9, 11.3, 12.8, 11.2, 12.9, 11.1]
closes = closes_from(base, 0.18)
kline_from_close(ax, closes, 0.5)
ax.axhline(box_top, color=RED, ls='--', lw=1)
ax.axhline(box_bot, color=GREEN, ls='--', lw=1)
ax.annotate('放量向上突破箱顶\n回踩不破 → 真突破', xy=(24, 13.5), xytext=(20, 14.6), fontsize=9,
            arrowprops=dict(arrowstyle='->', color=RED))
ax.set_title('矩形整理真突破：放量过箱顶、回踩不破', fontsize=12)
ax.set_xticks([])
save(fig, 'v8-06.png')

# ========== v8-07 矩形假突破 ==========
fig, ax = setup((9, 4.6))
np.random.seed(12)
n = 34
base = np.concatenate([np.linspace(11, 13, 6), np.full(16, 12.0), np.linspace(13.0, 11.2, 12)])
base = np.array(base, dtype=float)
base[6:22] = [12.8, 11.2, 12.9, 11.1, 12.7, 11.3, 12.9, 11.2, 12.8, 11.1, 12.9, 11.3, 12.8, 11.2, 12.9, 11.1]
base[21] = 13.6  # false breakout
closes = closes_from(base, 0.18)
kline_from_close(ax, closes, 0.5)
ax.axhline(13.0, color=RED, ls='--', lw=1)
ax.axhline(11.0, color=GREEN, ls='--', lw=1)
ax.annotate('无量假突破：刺破箱顶\n很快跌回箱内 → 假突破', xy=(21, 13.6), xytext=(12, 14.6), fontsize=9,
            arrowprops=dict(arrowstyle='->', color=GREEN))
ax.set_title('矩形整理假突破：无量刺破箱顶、迅速回落', fontsize=12)
ax.set_xticks([])
save(fig, 'v8-07.png')

# ========== v8-08 断头铡刀 ==========
fig, ax = setup((9, 4.6))
np.random.seed(14)
n = 24
base = np.linspace(12, 12.6, n)
closes = closes_from(base, 0.25)
closes[-1] = 10.6  # big yin crossing all MAs
kline_from_close(ax, closes, 0.5)
for nn, col, lab in [(5, RED, '5日'), (10, ORANGE, '10日'), (20, BLUE, '20日')]:
    ma = np.convolve(closes, np.ones(nn)/nn, mode='valid')
    ax.plot(np.arange(nn-1, n), ma, color=col, lw=1.4, label=lab)
ax.annotate('断头铡刀：一根大阴线\n同时下穿多根均线', xy=(n-1, 10.6), xytext=(6, 9.6), fontsize=9.5,
            arrowprops=dict(arrowstyle='->', color=GREEN))
ax.set_title('断头铡刀：典型止损卖出信号', fontsize=12)
ax.legend(loc='upper left', fontsize=8, frameon=False)
ax.set_xticks([])
save(fig, 'v8-08.png')

# ========== v8-09 多头排列中信号有效性 ==========
fig, ax = setup((9, 4.6))
np.random.seed(16)
n = 32
base = np.concatenate([np.linspace(10, 15, 22), np.linspace(15, 15.8, 10)])
closes = closes_from(base, 0.25)
closes[14] = 14.2; closes[15] = 15.4; closes[16] = 14.5
kline_from_close(ax, closes, 0.5)
for nn, col, lab in [(5, RED, '5日'), (10, ORANGE, '10日'), (20, BLUE, '20日')]:
    ma = np.convolve(closes, np.ones(nn)/nn, mode='valid')
    ax.plot(np.arange(nn-1, n), ma, color=col, lw=1.3, label=lab)
ax.annotate('多头排列中：见多信号有效\n见顶信号多为洗盘', xy=(15, 15.4), xytext=(2, 16.4), fontsize=9,
            arrowprops=dict(arrowstyle='->', color=RED))
ax.set_title('多头排列：做多信号可信，见顶信号要留一日', fontsize=12)
ax.legend(loc='upper left', fontsize=8, frameon=False)
ax.set_xticks([])
save(fig, 'v8-09.png')

# ========== v8-10 空头排列中信号有效性 ==========
fig, ax = setup((9, 4.6))
np.random.seed(18)
n = 32
base = np.concatenate([np.linspace(15, 10, 22), np.linspace(10, 9.5, 10)])
closes = closes_from(base, 0.25)
closes[14] = 10.6; closes[15] = 9.6; closes[16] = 10.4
kline_from_close(ax, closes, 0.5)
for nn, col, lab in [(5, RED, '5日'), (10, ORANGE, '10日'), (20, BLUE, '20日')]:
    ma = np.convolve(closes, np.ones(nn)/nn, mode='valid')
    ax.plot(np.arange(nn-1, n), ma, color=col, lw=1.3, label=lab)
ax.annotate('空头排列中：见顶信号有效\n见底信号多为陷阱', xy=(15, 9.6), xytext=(2, 8.4), fontsize=9,
            arrowprops=dict(arrowstyle='->', color=GREEN))
ax.set_title('空头排列：做空/止损信号可信，见底信号不抄', fontsize=12)
ax.legend(loc='upper right', fontsize=8, frameon=False)
ax.set_xticks([])
save(fig, 'v8-10.png')

# ========== v8-11 矩形整理形态 ==========
fig, ax = setup((9, 4.4))
np.random.seed(20)
n = 28
base = np.concatenate([np.linspace(10, 12.5, 5),
                       [12.7, 11.3, 12.8, 11.2, 12.7, 11.3, 12.8, 11.2, 12.7, 11.3, 12.8, 11.2],
                       np.linspace(11.2, 12.5, 11)])
base = np.array(base, dtype=float)[:n]
closes = closes_from(base, 0.15)
kline_from_close(ax, closes, 0.5)
ax.axhline(12.8, color=GREY, ls='--', lw=1)
ax.axhline(11.2, color=GREY, ls='--', lw=1)
ax.text(0.5, 12.95, '矩形上沿（压力）', fontsize=8.5, color=GREY)
ax.text(0.5, 10.85, '矩形下沿（支撑）', fontsize=8.5, color=GREY)
ax.set_title('矩形（箱体）整理：上有压力、下有支撑，反复拉锯', fontsize=12)
ax.set_xticks([])
save(fig, 'v8-11.png')

# ========== v8-12 断头铡刀失败信号 ==========
fig, ax = setup((9, 4.6))
np.random.seed(22)
n = 26
base = np.concatenate([np.linspace(12, 12.4, 12), np.linspace(12.4, 14, 14)])
closes = closes_from(base, 0.2)
closes[12] = 11.0  # fake guillotine
kline_from_close(ax, closes, 0.5)
for nn, col, lab in [(5, RED, '5日'), (10, ORANGE, '10日'), (20, BLUE, '20日')]:
    ma = np.convolve(closes, np.ones(nn)/nn, mode='valid')
    ax.plot(np.arange(nn-1, n), ma, color=col, lw=1.3, label=lab)
ax.annotate('失败信号：无量下穿\n很快收回、反向上攻', xy=(12, 11.0), xytext=(2, 9.6), fontsize=9,
            arrowprops=dict(arrowstyle='->', color=ORANGE))
ax.set_title('断头铡刀失败：缩量假跌破、次日收回（洗盘）', fontsize=12)
ax.legend(loc='upper left', fontsize=8, frameon=False)
ax.set_xticks([])
save(fig, 'v8-12.png')

# ========== v8-13 多空排列与信号概率 ==========
fig, ax = setup((9, 4.4))
cats = ['多头排列\n见顶信号', '多头排列\n见底信号', '空头排列\n见底信号', '空头排列\n见顶信号']
eff = [35, 80, 30, 82]
bars = ax.bar(cats, eff, color=[ORANGE, RED, ORANGE, GREEN], width=0.6)
for b, p in zip(bars, eff):
    ax.text(b.get_x()+b.get_width()/2, p+1.5, f'约{p}%', ha='center', fontsize=9.5)
ax.set_ylim(0, 100)
ax.set_ylabel('信号有效概率（示意）', fontsize=9)
ax.set_title('同一信号在不同均线排列下的有效概率天差地别', fontsize=12)
save(fig, 'v8-13.png')

# ========== v8-14 易错点：口诀误用 ==========
fig, axes = plt.subplots(1, 2, figsize=(11, 4.2), dpi=130)
np.random.seed(24)
# left: low position "hammer" that is just noise
n = 12
base = np.linspace(12, 11, n)
closes = closes_from(base, 0.4)
kline_from_close(axes[0], closes, 0.5)
draw_kline(axes[0], 11, 11.1, 11.15, 11.2, 10.3, 0.5)
axes[0].annotate('低位单根"锤头"\n无量能/均线配合 → 不可靠', xy=(11, 10.6), xytext=(2, 9.6), fontsize=9,
                 arrowprops=dict(arrowstyle='->', color=ORANGE))
axes[0].set_title('易错：只背口诀、不看位置与共振', fontsize=11)
axes[0].set_xticks([]); axes[0].set_yticks([])
axes[0].spines['top'].set_visible(False); axes[0].spines['right'].set_visible(False)
# right: correct
np.random.seed(25)
base2 = np.concatenate([np.linspace(14, 10, 10), np.linspace(10, 11.5, 8)])
closes2 = closes_from(base2, 0.25)
kline_from_close(axes[1], closes2, 0.5)
ma20 = np.convolve(closes2, np.ones(10)/10, mode='valid')
axes[1].plot(np.arange(9, 18), ma20, color=BLUE, lw=1.4, label='均线走平向上')
axes[1].annotate('底部+均线走平+信号共振\n→ 才是高胜率买点', xy=(15, 11.3), xytext=(4, 12.6), fontsize=9,
                arrowprops=dict(arrowstyle='->', color=GREEN))
axes[1].set_title('正确：口诀要配位置、量能、均线共振', fontsize=11)
axes[1].legend(loc='upper left', fontsize=8, frameon=False)
axes[1].set_xticks([]); axes[1].set_yticks([])
axes[1].spines['top'].set_visible(False); axes[1].spines['right'].set_visible(False)
save(fig, 'v8-14.png')

# ========== v8-15 赢家操作流程图 ==========
fig, ax = plt.subplots(figsize=(9, 3.2), dpi=130)
ax.axis('off')
steps = ['看大势定多空', '等信号不追', '试探小仓', '确认加仓', '趋势内持有', '见顶预警', '共振离场']
colors = [BLUE, ORANGE, PURPLE, RED, GREEN, '#E67E22', '#C0392B']
for i, (s, c) in enumerate(zip(steps, colors)):
    x = 0.4 + i * 1.42
    box = patches.FancyBboxPatch((x, 1.2), 1.25, 1.0, boxstyle="round,pad=0.05",
                                 facecolor=c, edgecolor='black', alpha=0.85)
    ax.add_patch(box)
    ax.text(x+0.62, 1.7, s, ha='center', va='center', fontsize=8.5, color='white')
    if i < 6:
        ax.annotate('', xy=(x+1.42, 1.7), xytext=(x+1.27, 1.7),
                    arrowprops=dict(arrowstyle='->', lw=1.3, color='black'))
ax.set_xlim(0, 10.4); ax.set_ylim(0.8, 2.6)
ax.set_title('赢家完整操作流程：从观察到离场的闭环', fontsize=12)
save(fig, 'v8-15.png')

print("V8 ALL DONE")
