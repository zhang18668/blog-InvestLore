# -*- coding: utf-8 -*-
"""Generate vol3 stock-selection diagrams (red-up / green-down)."""
import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'FangSong', 'SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
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

# ========== 01 选股系统框架：四张面漏斗 ==========
fig, ax = plt.subplots(figsize=(9, 5), dpi=130)
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')
# Funnel layers
layers = [
    (8.5, 1.2, '基本面（政策·行业·公司质地）', BLUE),
    (6.8, 1.2, '市场面（题材·资金·换手率）', ORANGE),
    (5.1, 1.2, '心理面（情绪·预期·逆人性）', PURPLE),
    (3.4, 1.2, '技术面（K线·均线·量价）', RED),
    (1.7, 1.2, '最终选股标的', GREEN),
]
for y, h, label, color in layers:
    left = 1 + (8.5 - y) * 0.3
    width = 8 - (8.5 - y) * 0.6
    box = FancyBboxPatch((left, y), width, h, boxstyle="round,pad=0.1",
                         facecolor=color, edgecolor=color, alpha=0.85)
    ax.add_patch(box)
    ax.text(5, y + h/2, label, ha='center', va='center', fontsize=11,
            color='white', fontweight='bold')
# Arrows between layers
for i in range(len(layers)-1):
    y1 = layers[i][0]
    y2 = layers[i+1][0] + layers[i+1][1]
    ax.annotate('', xy=(5, y2), xytext=(5, y1),
                arrowprops=dict(arrowstyle='->', color=GREY, lw=1.5))
ax.set_title('选股系统框架：四张面自上而下漏斗筛选', fontsize=13, pad=10)
save(fig, 'vol3-01.png')

# ========== 02 政策面选股流程 ==========
fig, ax = plt.subplots(figsize=(9, 4.5), dpi=130)
ax.set_xlim(0, 10)
ax.set_ylim(0, 6)
ax.axis('off')
steps = [
    (1.5, '高层讲话\n权威社论', BLUE),
    (3.5, '政策方向\n产业扶持', ORANGE),
    (5.5, '受益行业\n板块筛选', PURPLE),
    (7.5, '龙头个股\n标的锁定', RED),
    (9.0, '买点确认\n技术验证', GREEN),
]
for x, label, color in steps:
    circle = plt.Circle((x, 3), 0.55, color=color, alpha=0.85)
    ax.add_patch(circle)
    ax.text(x, 3, label, ha='center', va='center', fontsize=8.5,
            color='white', fontweight='bold')
for i in range(len(steps)-1):
    ax.annotate('', xy=(steps[i+1][0]-0.6, 3), xytext=(steps[i][0]+0.6, 3),
                arrowprops=dict(arrowstyle='->', color=GREY, lw=1.5))
ax.text(5, 5.3, '政策面选股：从宏观政策到具体买点', ha='center', fontsize=12, fontweight='bold')
ax.text(5, 1.0, '核心原则：顺着政策方向选行业，再在行业里找标的，技术面确认买点',
        ha='center', fontsize=9, color=GREY, style='italic')
save(fig, 'vol3-02.png')

# ========== 03 行业生命周期曲线 ==========
fig, ax = setup((9, 4.5))
x = np.linspace(0, 10, 200)
# S-curve: 导入期 -> 成长期 -> 成熟期 -> 衰退期
y = 10 / (1 + np.exp(-(x - 5) * 1.2))
ax.plot(x, y, color=BLUE, linewidth=2.5)
# Annotations
ax.axvspan(0, 2.5, alpha=0.1, color=GREY)
ax.axvspan(2.5, 5.5, alpha=0.1, color=RED)
ax.axvspan(5.5, 8, alpha=0.1, color=ORANGE)
ax.axvspan(8, 10, alpha=0.1, color=GREEN)
ax.text(1.25, 8.5, '导入期\n风险大\n机会多', ha='center', fontsize=9, color=GREY)
ax.text(4, 9.2, '成长期\n最佳投资期\n业绩高增长', ha='center', fontsize=9, color=RED, fontweight='bold')
ax.text(6.75, 7.5, '成熟期\n稳健回报\n龙头为王', ha='center', fontsize=9, color=ORANGE)
ax.text(9, 4, '衰退期\n回避\n夕阳行业', ha='center', fontsize=9, color=GREEN)
ax.set_title('行业生命周期：成长期是最佳选股窗口', fontsize=12)
ax.set_xlabel('时间 →', fontsize=9)
ax.set_ylabel('行业景气度', fontsize=9)
ax.set_xticks([])
save(fig, 'vol3-03.png')

# ========== 04 板块轮动规律 ==========
fig, axes = plt.subplots(3, 1, figsize=(9, 6), dpi=130)
np.random.seed(11)
n = 40
# Sector A: starts first, peaks early
trend_a = np.concatenate([np.linspace(10, 18, 15), np.linspace(18, 12, 25)])
closes_a = closes_from(trend_a, 0.5)
# Sector B: starts after A, peaks later
trend_b = np.concatenate([np.linspace(10, 11, 10), np.linspace(11, 20, 15), np.linspace(20, 14, 15)])
closes_b = closes_from(trend_b, 0.5)
# Sector C: starts last, lagging
trend_c = np.concatenate([np.linspace(10, 10.5, 20), np.linspace(10.5, 17, 12), np.linspace(17, 15, 8)])
closes_c = closes_from(trend_c, 0.5)

for ax, closes, title, color in [
    (axes[0], closes_a, '领涨板块（甲）：先启动先见顶', RED),
    (axes[1], closes_b, '接力板块（乙）：接棒上涨，节奏滞后', ORANGE),
    (axes[2], closes_c, '补涨板块（丙）：最后启动，行情尾声', BLUE),
]:
    kline_from_close(ax, closes, 0.45)
    ax.set_title(title, fontsize=10)
    ax.set_xticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
fig.suptitle('板块轮动规律：领涨→接力→补涨，踏准节奏比死抱更重要', fontsize=12, y=1.01)
save(fig, 'vol3-04.png')

# ========== 05 十大流通股东持股变化 ==========
fig, ax = setup((9, 4.5))
quarters = ['Q1', 'Q2', 'Q3', 'Q4', 'Q1', 'Q2', 'Q3', 'Q4']
# Institutional holdings increasing
inst = [12, 15, 18, 22, 26, 30, 34, 38]
# Retail holdings decreasing
retail = [88, 85, 82, 78, 74, 70, 66, 62]
x = np.arange(len(quarters))
ax.bar(x - 0.2, inst, 0.4, label='机构/大股东持股(%)', color=RED, alpha=0.8)
ax.bar(x + 0.2, retail, 0.4, label='散户持股(%)', color=GREEN, alpha=0.6)
ax.set_xticks(x)
ax.set_xticklabels(quarters)
ax.set_ylabel('持股比例(%)', fontsize=9)
ax.set_title('筹码集中信号：十大流通股东持股持续上升', fontsize=12)
ax.legend(loc='center right', fontsize=8, frameon=False)
ax2 = ax.twinx()
np.random.seed(21)
trend = np.concatenate([np.linspace(10, 11, 4), np.linspace(11, 16, 4)])
closes = closes_from(trend, 0.3)
ax2.plot(x, closes, color=BLUE, linewidth=2, marker='o', markersize=4, label='股价')
ax2.set_ylabel('股价(元)', fontsize=9, color=BLUE)
ax2.tick_params(axis='y', labelcolor=BLUE)
save(fig, 'vol3-05.png')

# ========== 06 大股东易主信号 ==========
fig, ax = setup((9, 4.5))
np.random.seed(31)
n = 50
# Before change: flat/declining
trend = np.concatenate([np.linspace(12, 11, 25), np.linspace(11, 22, 25)])
closes = closes_from(trend, 0.4)
kline_from_close(ax, closes, 0.5)
# Mark the change point
ax.axvline(x=25, color='black', linestyle='--', linewidth=1.5, alpha=0.7)
ax.annotate('大股东易主\n（新大股东入主）', xy=(25, 16), xytext=(10, 19),
            fontsize=9, arrowprops=dict(arrowstyle='->', color='black'),
            bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.8))
ax.set_title('大股东易主：新股东带来新预期，股价步入上升通道', fontsize=12)
ax.set_xticks([])
save(fig, 'vol3-06.png')

# ========== 07 筹码集中度判断 ==========
fig, axes = plt.subplots(1, 2, figsize=(11, 4.2), dpi=130)
np.random.seed(41)
# Left: scattered chips (high volatility, no trend)
n = 40
trend1 = np.array([12 + np.sin(i/3) * 1.5 for i in range(n)])
closes1 = closes_from(trend1, 0.6)
kline_from_close(axes[0], closes1, 0.5)
axes[0].set_title('筹码分散：震荡无序，主力未介入', fontsize=11)
axes[0].set_xticks([])
axes[0].spines['top'].set_visible(False)
axes[0].spines['right'].set_visible(False)
# Right: concentrated chips (steady uptrend)
trend2 = np.linspace(10, 18, n)
closes2 = closes_from(trend2, 0.3)
kline_from_close(axes[1], closes2, 0.5)
axes[1].set_title('筹码集中：稳步推升，主力控盘明显', fontsize=11)
axes[1].set_xticks([])
axes[1].spines['top'].set_visible(False)
axes[1].spines['right'].set_visible(False)
fig.suptitle('筹码集中 vs 分散：走势是最直观的判断', fontsize=12, y=1.02)
save(fig, 'vol3-07.png')

# ========== 08 换手率选股：温和放量 vs 天量出货 ==========
fig, axes = plt.subplots(2, 1, figsize=(9, 5.6), dpi=130, gridspec_kw={'height_ratios':[2,1]})
np.random.seed(51)
n = 40
# Price: steady rise then climax
trend = np.concatenate([np.linspace(10, 14, 25), np.linspace(14, 16, 8), np.linspace(16, 13, 7)])
closes = closes_from(trend, 0.4)
# Volume: mild increase then explosion
vol = np.concatenate([np.linspace(8, 15, 25), np.linspace(15, 45, 8), np.linspace(45, 20, 7)])
ax = axes[0]
kline_from_close(ax, closes, 0.5)
ax.set_title('换手率对比：温和放量可跟踪，骤然天量要警惕出货', fontsize=11)
ax.set_xticks([])
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax2 = axes[1]
colors = [RED if closes[i] >= (closes[i-1] if i > 0 else closes[i]) else GREEN for i in range(n)]
ax2.bar(range(n), vol, color=colors, width=0.6)
ax2.axvspan(0, 24, alpha=0.08, color=BLUE)
ax2.text(12, 42, '温和放量\n(可跟踪)', ha='center', fontsize=8, color=BLUE)
ax2.axvspan(25, 32, alpha=0.1, color=RED)
ax2.text(28.5, 42, '天量换手\n(警惕出货)', ha='center', fontsize=8, color=RED)
ax2.set_ylabel('换手率(%)', fontsize=9)
ax2.set_xticks([])
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
save(fig, 'vol3-08.png')

# ========== 09 题材概念：公布前扬公布后落 ==========
fig, axes = plt.subplots(2, 1, figsize=(9, 5.4), dpi=130, gridspec_kw={'height_ratios':[2,1]})
np.random.seed(61)
n = 50
# Rumor phase: quiet accumulation
# Announcement: gap up then fade
trend = np.concatenate([
    np.linspace(10, 11, 15),      # 朦胧期：悄悄吸筹
    np.linspace(11, 16, 10),      # 传闻扩散：快速拉升
    np.linspace(16, 18, 5),       # 公布前夕：最后冲高
    np.linspace(18, 12, 20),      # 正式公布：见光死
])
closes = closes_from(trend, 0.35)
vol = np.concatenate([
    np.linspace(5, 10, 15),
    np.linspace(10, 25, 10),
    np.linspace(25, 40, 5),
    np.linspace(40, 15, 20),
])
ax = axes[0]
kline_from_close(ax, closes, 0.5)
# Mark phases
ax.axvline(x=25, color='grey', linestyle=':', linewidth=1)
ax.axvline(x=30, color='red', linestyle='--', linewidth=1.5)
ax.text(12, 19, '朦胧吸筹期', ha='center', fontsize=8, color=BLUE)
ax.text(27.5, 19, '传闻扩散期', ha='center', fontsize=8, color=ORANGE)
ax.text(40, 19, '利好公布后\n(见光死)', ha='center', fontsize=8, color=RED, fontweight='bold')
ax.set_title('题材炒作节奏：公布前扬、公布后落', fontsize=11)
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
save(fig, 'vol3-09.png')

# ========== 10 量价齐升 ==========
fig, axes = plt.subplots(2, 1, figsize=(9, 5.4), dpi=130, gridspec_kw={'height_ratios':[2,1]})
np.random.seed(71)
n = 35
trend = np.linspace(10, 16, n)
closes = closes_from(trend, 0.4)
vol = np.linspace(10, 35, n)
ax = axes[0]
kline_from_close(ax, closes, 0.5)
ax.set_title('量价齐升：价创新高、量能同步放大，健康上涨形态', fontsize=11)
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
save(fig, 'vol3-10.png')

# ========== 11 缩量回调 ==========
fig, axes = plt.subplots(2, 1, figsize=(9, 5.4), dpi=130, gridspec_kw={'height_ratios':[2,1]})
np.random.seed(81)
n = 40
# Uptrend then mild pullback on shrinking volume
trend = np.concatenate([
    np.linspace(10, 15, 20),
    np.linspace(15, 13.5, 8),
    np.linspace(13.5, 17, 12),
])
closes = closes_from(trend, 0.35)
vol = np.concatenate([
    np.linspace(15, 30, 20),
    np.linspace(30, 12, 8),
    np.linspace(12, 28, 12),
])
ax = axes[0]
kline_from_close(ax, closes, 0.5)
ax.axvspan(20, 27, alpha=0.1, color=ORANGE)
ax.annotate('缩量回调\n(洗盘特征)', xy=(23, 14.2), xytext=(10, 12),
            fontsize=9, arrowprops=dict(arrowstyle='->', color=ORANGE))
ax.set_title('缩量回调：上涨途中缩量回档，是低吸机会而非反转', fontsize=11)
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
save(fig, 'vol3-11.png')

# ========== 12 突破放量 ==========
fig, axes = plt.subplots(2, 1, figsize=(9, 5.4), dpi=130, gridspec_kw={'height_ratios':[2,1]})
np.random.seed(91)
n = 45
# Consolidation then breakout on huge volume
trend = np.concatenate([
    np.linspace(12, 12.5, 25),   # 横盘整理
    np.linspace(12.5, 13, 3),    # 突破前蓄势
    np.linspace(13, 17, 17),     # 放量突破
])
closes = closes_from(trend, 0.3)
vol = np.concatenate([
    np.linspace(10, 12, 25),
    np.linspace(12, 18, 3),
    np.linspace(18, 45, 17),
])
ax = axes[0]
kline_from_close(ax, closes, 0.5)
ax.axhline(13, color='black', linestyle='--', linewidth=1, alpha=0.7)
ax.text(2, 13.2, '压力位(颈线)', fontsize=8, color='black')
ax.annotate('放量突破颈线\n(买入信号)', xy=(28, 13.5), xytext=(30, 15.5),
            fontsize=9, arrowprops=dict(arrowstyle='->', color=RED),
            bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.8))
ax.set_title('突破放量：横盘后放量突破颈线，是强势启动信号', fontsize=11)
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
save(fig, 'vol3-12.png')

# ========== 13 分散与集中 ==========
fig, axes = plt.subplots(1, 2, figsize=(11, 4.2), dpi=130)
# Left: diversification (5 stocks)
np.random.seed(101)
ax = axes[0]
n = 30
for i, (base, vol, label) in enumerate([
    (10, 0.8, '股票A'), (12, 1.2, '股票B'), (8, 0.6, '股票C'),
    (11, 1.5, '股票D'), (9, 0.9, '股票E'),
]):
    trend = np.linspace(base, base + np.random.uniform(-2, 3), n)
    closes = closes_from(trend, vol)
    ax.plot(range(n), closes, linewidth=1.2, label=label, alpha=0.8)
ax.set_title('分散持仓：5只以上，涨跌互现\n适合稳健型、大资金', fontsize=10)
ax.legend(fontsize=7, frameon=False, loc='upper left')
ax.set_xticks([])
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
# Right: concentration (1-2 stocks)
np.random.seed(102)
ax = axes[1]
trend1 = np.linspace(10, 20, n)
closes1 = closes_from(trend1, 0.5)
trend2 = np.linspace(15, 28, n)
closes2 = closes_from(trend2, 0.5)
ax.plot(range(n), closes1, linewidth=1.5, color=RED, label='核心持仓1', alpha=0.9)
ax.plot(range(n), closes2, linewidth=1.5, color=ORANGE, label='核心持仓2', alpha=0.9)
ax.set_title('集中持仓：1-3只，重仓出击\n适合激进型、小资金', fontsize=10)
ax.legend(fontsize=7, frameon=False, loc='upper left')
ax.set_xticks([])
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
fig.suptitle('分散与集中：根据资金量、性格、经验选择持仓策略', fontsize=12, y=1.02)
save(fig, 'vol3-13.png')

# ========== 14 先给自己定性 ==========
fig, ax = plt.subplots(figsize=(9, 5), dpi=130)
ax.set_xlim(0, 10)
ax.set_ylim(0, 8)
ax.axis('off')
# Center circle
circle = plt.Circle((5, 4), 1.2, color=BLUE, alpha=0.15)
ax.add_patch(circle)
ax.text(5, 4, '我是谁？\n先定性自己', ha='center', va='center',
        fontsize=11, fontweight='bold', color=BLUE)
# Four quadrants
items = [
    (2, 6.5, '风险承受力\n低→蓝筹/高→题材', GREEN),
    (8, 6.5, '资金规模\n小→集中/大→分散', ORANGE),
    (2, 1.5, '看盘时间\n少→长线/多→短线', PURPLE),
    (8, 1.5, '熟悉领域\n只在能力圈内选股', RED),
]
for x, y, label, color in items:
    box = FancyBboxPatch((x-1.3, y-0.6), 2.6, 1.2, boxstyle="round,pad=0.1",
                        facecolor=color, alpha=0.2, edgecolor=color, linewidth=1.5)
    ax.add_patch(box)
    ax.text(x, y, label, ha='center', va='center', fontsize=9, color=color, fontweight='bold')
    # Arrow to center
    ax.annotate('', xy=(5, 4), xytext=(x, y),
                arrowprops=dict(arrowstyle='->', color=color, lw=1, alpha=0.5))
ax.set_title('选股第一步：先给"自己"定性，再谈选什么股', fontsize=13, pad=10)
save(fig, 'vol3-14.png')

# ========== 15 选股纪律总结 ==========
fig, ax = plt.subplots(figsize=(9, 5), dpi=130)
ax.set_xlim(0, 10)
ax.set_ylim(0, 7)
ax.axis('off')
rules = [
    (1, 5.5, '✓ 不追高：涨高了不追，等回调或突破确认', GREEN),
    (1, 4.2, '✓ 强势优先：只选上升趋势中的股票', RED),
    (1, 2.9, '✓ 弱势回避：下降趋势的股票不碰', GREY),
    (1, 1.6, '✓ 候选池小而熟：3-5只足矣，不天天换', BLUE),
    (5.5, 5.5, '✗ 不追涨杀跌：情绪驱动的操作最易亏', RED),
    (5.5, 4.2, '✗ 不贪心：目标达到就走，不幻想最高点', ORANGE),
    (5.5, 2.9, '✗ 不恐惧：该买时要敢下手，错过比套牢更痛', PURPLE),
    (5.5, 1.6, '✗ 不频繁交易：手续费和失误率会吃掉利润', BROWN),
]
for x, y, label, color in rules:
    ax.text(x, y, label, fontsize=10, va='center', color=color)
ax.set_title('选股纪律：八条铁律，贴在屏幕旁', fontsize=13, pad=10)
save(fig, 'vol3-15.png')

print("ALL VOL3 DONE")
