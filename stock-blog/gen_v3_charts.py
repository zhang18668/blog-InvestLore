# -*- coding: utf-8 -*-
"""
第三册 选股方法专辑 - 同花顺风格K线重绘脚本
阳线 #FF4444 (红涨)  阴线 #00AA00 (绿跌)
白底无坐标轴
"""
import os, math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch

# ---------- 全局样式 ----------
plt.rcParams["font.sans-serif"] = ["Microsoft JhengHei", "SimHei", "Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False

UP = "#FF4444"    # 阳线 红
DN = "#00AA00"    # 阴线 绿
OUT = r"E:\生活\股票操练大全全套\stock-blog\source\images\kxian"
os.makedirs(OUT, exist_ok=True)

rng = np.random.default_rng(20260922)


def save(fig, name):
    path = os.path.join(OUT, name)
    fig.savefig(path, dpi=150, bbox_inches="tight", pad_inches=0.15,
                facecolor="white", edgecolor="none")
    plt.close(fig)
    print("saved:", name)


def draw_candles(ax, opens, closes, highs, lows, width=0.6):
    """在 ax 上画一组K线"""
    n = len(opens)
    for i in range(n):
        o, c, h, l = opens[i], closes[i], highs[i], lows[i]
        color = UP if c >= o else DN
        # 影线
        ax.plot([i, i], [l, h], color=color, linewidth=1.0, zorder=2)
        # 实体
        bottom = min(o, c)
        height = max(abs(c - o), 0.02)
        rect = mpatches.Rectangle((i - width / 2, bottom), width, height,
                                  facecolor=color, edgecolor=color, zorder=3)
        ax.add_patch(rect)
    ax.set_xlim(-1, n)
    ax.axis("off")


def gen_series(n, start=10.0, drift=0.0, vol=0.3, seed=None):
    """生成一组随机K线数据"""
    if seed is not None:
        r = np.random.default_rng(seed)
    else:
        r = rng
    closes = np.zeros(n)
    closes[0] = start
    for i in range(1, n):
        closes[i] = closes[i - 1] + drift + r.normal(0, vol)
    opens = np.zeros(n)
    opens[0] = start
    for i in range(1, n):
        opens[i] = closes[i - 1] + r.normal(0, vol * 0.3)
    highs = np.maximum(opens, closes) + np.abs(r.normal(0, vol * 0.4, n))
    lows = np.minimum(opens, closes) - np.abs(r.normal(0, vol * 0.4, n))
    return opens.tolist(), closes.tolist(), highs.tolist(), lows.tolist()


def ma(data, period):
    """简单移动平均"""
    result = [np.nan] * len(data)
    for i in range(period - 1, len(data)):
        result[i] = sum(data[i - period + 1:i + 1]) / period
    return result


def plot_ma(ax, closes, period, color="#333333", style="-", lw=1.2):
    m = ma(closes, period)
    xs = list(range(len(m)))
    ax.plot(xs, m, color=color, linestyle=style, linewidth=lw, zorder=1)


# ============================================================
# 图1: 早晨十字星 vs 早晨之星 对比
# ============================================================
def chart_01():
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.2))

    # 左: 早晨十字星 (大跌 + 十字星 + 大阳)
    o1, c1, h1, l1 = [], [], [], []
    # 下跌段
    base = 15.0
    for i in range(6):
        o = base - i * 0.6
        c = o - 0.8
        o1.append(o); c1.append(c)
        h1.append(o + 0.15); l1.append(c - 0.2)
    # 十字星
    o = c1[-1]; c = c1[-1] + 0.05
    o1.append(o); c1.append(c); h1.append(o + 0.5); l1.append(o - 0.5)
    # 大阳
    o = c1[-1]; c = o + 2.5
    o1.append(o); c1.append(c); h1.append(c + 0.1); l1.append(o - 0.1)
    # 续涨
    for i in range(3):
        o = c1[-1]; c = o + 1.2
        o1.append(o); c1.append(c); h1.append(c + 0.15); l1.append(o - 0.1)

    ax = axes[0]
    draw_candles(ax, o1, c1, h1, l1)
    ax.annotate("十字星", xy=(6, h1[6]), xytext=(4, h1[6] + 1.5),
                fontsize=11, ha="center",
                arrowprops=dict(arrowstyle="->", color="black"))
    ax.set_title("早晨十字星（见底信号更可靠）", fontsize=12)

    # 右: 早晨之星 (大跌 + 小阴/小阳 + 大阳)
    o2, c2, h2, l2 = [], [], [], []
    base = 15.0
    for i in range(6):
        o = base - i * 0.6
        c = o - 0.8
        o2.append(o); c2.append(c)
        h2.append(o + 0.15); l2.append(c - 0.2)
    # 小阳线
    o = c2[-1]; c = o + 0.3
    o2.append(o); c2.append(c); h2.append(c + 0.2); l2.append(o - 0.2)
    # 大阳
    o = c2[-1]; c = o + 2.2
    o2.append(o); c2.append(c); h2.append(c + 0.1); l2.append(o - 0.1)
    for i in range(3):
        o = c2[-1]; c = o + 1.0
        o2.append(o); c2.append(c); h2.append(c + 0.15); l2.append(o - 0.1)

    ax = axes[1]
    draw_candles(ax, o2, c2, h2, l2)
    ax.annotate("小阳线", xy=(6, h2[6]), xytext=(4, h2[6] + 1.5),
                fontsize=11, ha="center",
                arrowprops=dict(arrowstyle="->", color="black"))
    ax.set_title("早晨之星（见底信号）", fontsize=12)

    fig.suptitle("习题69  早晨十字星 vs 早晨之星  同条件下优先选早晨十字星",
                 fontsize=13, y=1.02)
    save(fig, "v3o-01.png")


# ============================================================
# 图2: 光头光脚大阳线 vs 带上影线大阳线
# ============================================================
def chart_02():
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.2))

    # 光头光脚大阳
    o, c, h, l = [], [], [], []
    base = 10.0
    for i in range(8):
        oo = base + i * 0.3
        cc = oo + 0.15
        o.append(oo); c.append(cc); h.append(cc); l.append(oo)
    # 光头光脚大阳
    oo = c[-1]; cc = oo + 3.0
    o.append(oo); c.append(cc); h.append(cc); l.append(oo)
    ax = axes[0]
    draw_candles(ax, o, c, h, l)
    ax.annotate("光头光脚大阳线\n多方上攻气势很盛", xy=(8, c[8]), xytext=(5, c[8] + 2),
                fontsize=10, ha="center",
                arrowprops=dict(arrowstyle="->", color="black"))
    ax.set_title("光头光脚大阳线（强势）", fontsize=12)

    # 带上影线大阳
    o2, c2, h2, l2 = [], [], [], []
    for i in range(8):
        oo = base + i * 0.3
        cc = oo + 0.15
        o2.append(oo); c2.append(cc); h2.append(cc); l2.append(oo)
    oo = c2[-1]; cc = oo + 2.5; hh = cc + 1.0
    o2.append(oo); c2.append(cc); h2.append(hh); l2.append(oo)
    ax = axes[1]
    draw_candles(ax, o2, c2, h2, l2)
    ax.annotate("带上影线大阳线\n多方底气不足", xy=(8, h2[8]), xytext=(5, h2[8] + 1.5),
                fontsize=10, ha="center",
                arrowprops=dict(arrowstyle="->", color="black"))
    ax.set_title("带上影线大阳线（次强）", fontsize=12)

    fig.suptitle("习题69  大阳线选股：光头光脚优于带上影线", fontsize=13, y=1.02)
    save(fig, "v3o-02.png")


# ============================================================
# 图3: 下探上涨形
# ============================================================
def chart_03():
    fig, ax = plt.subplots(figsize=(9, 4.5))
    o, c, h, l = [], [], [], []
    # 底部震荡
    base = 10.0
    for i in range(10):
        oo = base + np.sin(i * 0.8) * 0.4
        cc = oo + np.random.choice([-0.3, 0.3])
        o.append(oo); c.append(cc)
        h.append(max(oo, cc) + 0.2); l.append(min(oo, cc) - 0.2)
    # 下探大阴
    oo = c[-1]; cc = oo - 2.0
    o.append(oo); c.append(cc); h.append(oo + 0.1); l.append(cc - 0.3)
    # 大阳吞没
    oo = c[-1]; cc = oo + 3.5
    o.append(oo); c.append(cc); h.append(cc + 0.1); l.append(oo - 0.1)
    # 续涨
    for i in range(6):
        oo = c[-1]; cc = oo + 0.8
        o.append(oo); c.append(cc); h.append(cc + 0.2); l.append(oo - 0.1)

    closes = c
    draw_candles(ax, o, c, h, l)
    plot_ma(ax, closes, 5, "#666666", "--", 1.0)
    plot_ma(ax, closes, 30, "#333333", "-", 1.5)
    ax.annotate("下探上涨形\n均线开始向上发散\n主力洗盘动作", xy=(11, c[11]),
                xytext=(6, c[11] + 3), fontsize=10, ha="center",
                arrowprops=dict(arrowstyle="->", color="black"))
    ax.set_title("下探上涨形：均线向上发散时出现，洗盘后股价上涨", fontsize=12)
    save(fig, "v3o-03.png")


# ============================================================
# 图4: 徐缓上升形
# ============================================================
def chart_04():
    fig, ax = plt.subplots(figsize=(9, 4.5))
    o, c, h, l = [], [], [], []
    base = 10.0
    # 底部
    for i in range(8):
        oo = base + np.sin(i * 0.5) * 0.3
        cc = oo + np.random.choice([-0.2, 0.25])
        o.append(oo); c.append(cc); h.append(max(oo, cc) + 0.2); l.append(min(oo, cc) - 0.2)
    # 徐缓上升：连续小阳
    for i in range(12):
        oo = c[-1]; cc = oo + 0.35
        o.append(oo); c.append(cc); h.append(cc + 0.15); l.append(oo - 0.05)
    # 大阳加速
    oo = c[-1]; cc = oo + 2.5
    o.append(oo); c.append(cc); h.append(cc + 0.1); l.append(oo - 0.1)
    for i in range(4):
        oo = c[-1]; cc = oo + 0.6
        o.append(oo); c.append(cc); h.append(cc + 0.15); l.append(oo - 0.1)

    closes = c
    draw_candles(ax, o, c, h, l)
    plot_ma(ax, closes, 5, "#666666", "--", 1.0)
    plot_ma(ax, closes, 30, "#333333", "-", 1.5)
    ax.annotate("徐缓上升形\n均线多头排列\n股价向上攀升意料之中", xy=(18, c[18]),
                xytext=(12, c[18] + 2.5), fontsize=10, ha="center",
                arrowprops=dict(arrowstyle="->", color="black"))
    ax.set_title("徐缓上升形：均线多头排列，连续小阳后大阳加速", fontsize=12)
    save(fig, "v3o-04.png")


# ============================================================
# 图5: 潜伏底
# ============================================================
def chart_05():
    fig, ax = plt.subplots(figsize=(9, 4.5))
    o, c, h, l = [], [], [], []
    base = 12.0
    # 下跌
    for i in range(8):
        oo = base + i * 0.5
        cc = oo - 1.2
        o.append(oo); c.append(cc); h.append(oo + 0.1); l.append(cc - 0.2)
    # 潜伏底：长时间窄幅震荡
    bottom = c[-1]
    top = bottom + 1.5
    for i in range(20):
        center = (bottom + top) / 2
        oo = center + np.random.uniform(-0.3, 0.3)
        cc = center + np.random.uniform(-0.3, 0.3)
        o.append(oo); c.append(cc)
        h.append(max(oo, cc) + 0.25); l.append(min(oo, cc) - 0.25)
    # 突破上边线
    oo = c[-1]; cc = top + 2.0
    o.append(oo); c.append(cc); h.append(cc + 0.1); l.append(oo - 0.1)
    for i in range(4):
        oo = c[-1]; cc = oo + 1.0
        o.append(oo); c.append(cc); h.append(cc + 0.15); l.append(oo - 0.1)

    n = len(o)
    # 画上下边线
    ax.axhline(y=top, color="blue", linestyle="--", linewidth=1, xmin=0.25, xmax=0.95)
    ax.axhline(y=bottom, color="blue", linestyle="--", linewidth=1, xmin=0.25, xmax=0.95)
    ax.text(22, top + 0.2, "上边线", fontsize=9, color="blue")
    ax.text(22, bottom - 0.5, "下边线", fontsize=9, color="blue")

    draw_candles(ax, o, c, h, l)
    ax.annotate("潜伏底：长期窄幅震荡\n放巨量突破上边线后大涨", xy=(28, c[28]),
                xytext=(18, c[28] + 2), fontsize=10, ha="center",
                arrowprops=dict(arrowstyle="->", color="black"))
    ax.set_title("潜伏底：不鸣则已一鸣惊人，放巨量突破压力线大幅上扬", fontsize=12)
    save(fig, "v3o-05.png")


# ============================================================
# 图6: 头肩底
# ============================================================
def chart_06():
    fig, ax = plt.subplots(figsize=(9, 4.5))
    o, c, h, l = [], [], [], []
    # 左肩
    prices = [12, 11.5, 11, 10.5, 10, 10.8, 11.5]
    # 头部
    prices += [11, 10, 9, 8, 8.5, 9.5, 10.5]
    # 右肩
    prices += [11, 10.5, 10, 10.3, 10.8, 11.5]
    # 突破颈线
    prices += [12, 12.5, 13, 13.5, 14]

    for i, p in enumerate(prices):
        oo = p + np.random.uniform(-0.2, 0.2)
        cc = p + np.random.uniform(-0.2, 0.2)
        o.append(oo); c.append(cc)
        h.append(max(oo, cc) + 0.2); l.append(min(oo, cc) - 0.2)

    draw_candles(ax, o, c, h, l)
    # 颈线
    neck_y = 11.5
    ax.plot([3, 15], [neck_y, neck_y], "b--", linewidth=1.2)
    ax.text(14, neck_y + 0.3, "颈线", fontsize=10, color="blue")
    ax.annotate("左肩", xy=(3, 10), fontsize=10, ha="center")
    ax.annotate("头部", xy=(10, 8), fontsize=10, ha="center")
    ax.annotate("右肩", xy=(15, 10.5), fontsize=10, ha="center")
    ax.set_title("头肩底：突破颈线后回抽确认，买进信号", fontsize=12)
    save(fig, "v3o-06.png")


# ============================================================
# 图7: 双底(W底)
# ============================================================
def chart_07():
    fig, ax = plt.subplots(figsize=(9, 4.5))
    o, c, h, l = [], [], [], []
    prices = [12, 11, 10, 9.5, 10, 11, 11.5, 11, 10, 9.5, 10, 11, 11.5, 12.5, 13, 13.5, 14]
    for i, p in enumerate(prices):
        oo = p + np.random.uniform(-0.15, 0.15)
        cc = p + np.random.uniform(-0.15, 0.15)
        o.append(oo); c.append(cc)
        h.append(max(oo, cc) + 0.2); l.append(min(oo, cc) - 0.2)

    draw_candles(ax, o, c, h, l)
    neck_y = 11.5
    ax.plot([5, 12], [neck_y, neck_y], "b--", linewidth=1.2)
    ax.text(10, neck_y + 0.3, "颈线", fontsize=10, color="blue")
    ax.annotate("第一个底", xy=(3, 9.5), fontsize=10, ha="center")
    ax.annotate("第二个底", xy=(9, 9.5), fontsize=10, ha="center")
    ax.set_title("双底(W底)：第二个底放量突破颈线，买进信号", fontsize=12)
    save(fig, "v3o-07.png")


# ============================================================
# 图8: 新股高开低走 vs 低开高走
# ============================================================
def chart_08():
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.2))

    # 高开低走
    o, c, h, l = [], [], [], []
    o.append(20); c.append(22); h.append(22.5); l.append(19.5)
    o.append(22); c.append(20.5); h.append(22.2); l.append(20)
    for i in range(8):
        oo = c[-1]; cc = oo - np.random.uniform(0.3, 0.8)
        o.append(oo); c.append(cc); h.append(oo + 0.1); l.append(cc - 0.2)
    ax = axes[0]
    draw_candles(ax, o, c, h, l)
    ax.set_title("众人看好 → 高开低走\n（浦发银行式走势）", fontsize=11)

    # 低开高走
    o2, c2, h2, l2 = [], [], [], []
    o2.append(18); c2.append(16.5); h2.append(18.5); l2.append(16)
    o2.append(16.5); c2.append(18); h2.append(18.2); l2.append(16.2)
    for i in range(8):
        oo = c2[-1]; cc = oo + np.random.uniform(0.3, 0.8)
        o2.append(oo); c2.append(cc); h2.append(cc + 0.2); l2.append(oo - 0.1)
    ax = axes[1]
    draw_candles(ax, o2, c2, h2, l2)
    ax.set_title("众人看淡 → 低开高走\n（凯迪电力式走势）", fontsize=11)

    fig.suptitle("习题83  新股炒作：众人看好的不能买，众人看坏的才关注", fontsize=13, y=1.02)
    save(fig, "v3o-08.png")


# ============================================================
# 图9: 股东人数变化与股价关系
# ============================================================
def chart_09():
    fig, ax1 = plt.subplots(figsize=(9, 4.5))
    # 股价先跌后涨
    o, c, h, l = [], [], [], []
    base = 15.0
    for i in range(12):
        oo = base - i * 0.3
        cc = oo - 0.5
        o.append(oo); c.append(cc); h.append(oo + 0.1); l.append(cc - 0.2)
    for i in range(12):
        oo = c[-1]; cc = oo + 0.6
        o.append(oo); c.append(cc); h.append(cc + 0.2); l.append(oo - 0.1)
    draw_candles(ax1, o, c, h, l)
    ax1.set_title("习题47  股东人数减少→筹码集中→股价上涨", fontsize=12)

    # 标注股东人数变化
    ax1.annotate("股东人数\n持续减少\n筹码集中", xy=(8, c[8]),
                xytext=(4, c[8] + 4), fontsize=10, ha="center",
                arrowprops=dict(arrowstyle="->", color="black"))
    ax1.annotate("股东人数\n极度分散\n股价低迷", xy=(16, c[16]),
                xytext=(18, c[16] - 4), fontsize=10, ha="center",
                arrowprops=dict(arrowstyle="->", color="black"))
    save(fig, "v3o-09.png")


# ============================================================
# 图10: 板块轮动示意
# ============================================================
def chart_10():
    fig, ax = plt.subplots(figsize=(9, 4.5))
    sectors = ["科技", "金融", "地产", "医药", "能源", "消费", "周期"]
    # 板块轮动曲线
    x = np.arange(7)
    values = [3, 1, 2, 4, 1, 2, 3]
    colors = [UP if v > 2 else DN for v in values]
    bars = ax.bar(x, values, color=colors, width=0.6)
    ax.set_xticks(x)
    ax.set_xticklabels(sectors, fontsize=11)
    ax.set_ylabel("阶段涨幅", fontsize=10)
    ax.set_title("习题35  板块轮动：资金从一个板块流向另一个板块", fontsize=12)
    ax.axis("on")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    save(fig, "v3o-10.png")


# ============================================================
# 图11: 30日均线操作策略
# ============================================================
def chart_11():
    fig, axes = plt.subplots(2, 2, figsize=(10, 6))

    # (1) 大盘向上 + 30日均线向上 + 早晨十字星 → 积极买进
    ax = axes[0][0]
    o, c, h, l = [], [], [], []
    for i in range(10):
        oo = 10 + i * 0.3; cc = oo + 0.2
        o.append(oo); c.append(cc); h.append(cc + 0.1); l.append(oo - 0.05)
    # 早晨十字星
    oo = c[-1]; cc = oo - 1.5
    o.append(oo); c.append(cc); h.append(oo + 0.1); l.append(cc - 0.2)
    oo = c[-1]; cc = c[-1]; hh = cc + 0.5
    o.append(oo); c.append(cc); h.append(hh); l.append(cc - 0.5)
    oo = c[-1]; cc = oo + 1.5
    o.append(oo); c.append(cc); h.append(cc + 0.1); l.append(oo - 0.1)
    draw_candles(ax, o, c, h, l)
    plot_ma(ax, c, 5, "#333", "--", 1)
    ax.set_title("(1) 大盘↑ 30日线↑ → 积极买进", fontsize=10)

    # (2) 大盘向上 + 30日均线向下 + 早晨十字星 → 尝试性少量
    ax = axes[0][1]
    o, c, h, l = [], [], [], []
    for i in range(10):
        oo = 12 - i * 0.3; cc = oo - 0.2
        o.append(oo); c.append(cc); h.append(oo + 0.1); l.append(cc - 0.1)
    oo = c[-1]; cc = c[-1]; hh = cc + 0.5
    o.append(oo); c.append(cc); h.append(hh); l.append(cc - 0.5)
    oo = c[-1]; cc = oo + 1.2
    o.append(oo); c.append(cc); h.append(cc + 0.1); l.append(oo - 0.1)
    draw_candles(ax, o, c, h, l)
    ax.set_title("(2) 大盘↑ 30日线↓ → 少量买进", fontsize=10)

    # (3) 大盘向下 + 30日均线向上 → 尝试性少量
    ax = axes[1][0]
    o, c, h, l = [], [], [], []
    for i in range(8):
        oo = 10 + i * 0.2; cc = oo + 0.15
        o.append(oo); c.append(cc); h.append(cc + 0.1); l.append(oo - 0.05)
    for i in range(6):
        oo = c[-1]; cc = oo - 0.4
        o.append(oo); c.append(cc); h.append(oo + 0.1); l.append(cc - 0.1)
    oo = c[-1]; cc = c[-1]; hh = cc + 0.5
    o.append(oo); c.append(cc); h.append(hh); l.append(cc - 0.5)
    oo = c[-1]; cc = oo + 1.0
    o.append(oo); c.append(cc); h.append(cc + 0.1); l.append(oo - 0.1)
    draw_candles(ax, o, c, h, l)
    ax.set_title("(3) 大盘↓ 30日线↑ → 少量/观望", fontsize=10)

    # (4) 大盘向下 + 30日均线向下 → 持币观望
    ax = axes[1][1]
    o, c, h, l = [], [], [], []
    for i in range(14):
        oo = 13 - i * 0.3; cc = oo - 0.3
        o.append(oo); c.append(cc); h.append(oo + 0.1); l.append(cc - 0.1)
    oo = c[-1]; cc = c[-1]; hh = cc + 0.4
    o.append(oo); c.append(cc); h.append(hh); l.append(cc - 0.4)
    oo = c[-1]; cc = oo + 0.8
    o.append(oo); c.append(cc); h.append(cc + 0.1); l.append(oo - 0.1)
    draw_candles(ax, o, c, h, l)
    ax.set_title("(4) 大盘↓ 30日线↓ → 持币观望", fontsize=10)

    fig.suptitle("习题70  早晨十字星操作策略一览表（大盘走势 × 30日均线 × K线信号）",
                 fontsize=12, y=1.0)
    save(fig, "v3o-11.png")


# ============================================================
# 图12: 短线/中线/长线黑马对比
# ============================================================
def chart_12():
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.8))

    # 短线黑马: 大起大落
    ax = axes[0]
    o, c, h, l = [], [], [], []
    base = 10.0
    for i in range(6):
        oo = base + np.random.uniform(-0.3, 0.3)
        cc = oo + np.random.choice([-0.5, 0.6])
        o.append(oo); c.append(cc); h.append(max(oo, cc) + 0.3); l.append(min(oo, cc) - 0.3)
    for i in range(4):
        oo = c[-1]; cc = oo + 1.5
        o.append(oo); c.append(cc); h.append(cc + 0.2); l.append(oo - 0.1)
    for i in range(4):
        oo = c[-1]; cc = oo - 1.0
        o.append(oo); c.append(cc); h.append(oo + 0.2); l.append(cc - 0.1)
    draw_candles(ax, o, c, h, l)
    ax.set_title("短线黑马\n大起大落 暴涨暴跌", fontsize=10)

    # 中线黑马: 周而复始
    ax = axes[1]
    o, c, h, l = [], [], [], []
    base = 10.0
    for cycle in range(2):
        for i in range(6):
            oo = base + i * 0.5; cc = oo + 0.3
            o.append(oo); c.append(cc); h.append(cc + 0.15); l.append(oo - 0.05)
        for i in range(4):
            oo = c[-1]; cc = oo - 0.8
            o.append(oo); c.append(cc); h.append(oo + 0.1); l.append(cc - 0.1)
        base = c[-1] + 2
    draw_candles(ax, o, c, h, l)
    ax.set_title("中线黑马\n周而复始 周期循环", fontsize=10)

    # 长线黑马: 长期向上
    ax = axes[2]
    o, c, h, l = [], [], [], []
    base = 10.0
    for i in range(24):
        oo = base + i * 0.25 + np.random.uniform(-0.2, 0.2)
        cc = oo + np.random.uniform(-0.1, 0.4)
        o.append(oo); c.append(cc); h.append(max(oo, cc) + 0.2); l.append(min(oo, cc) - 0.2)
    draw_candles(ax, o, c, h, l)
    ax.set_title("长线黑马\n长期走牛 不断新高", fontsize=10)

    fig.suptitle("习题90  短线黑马 / 中线黑马 / 长线黑马 走势对比", fontsize=13, y=1.05)
    save(fig, "v3o-12.png")


# ============================================================
# 图13: 政策面选股示意
# ============================================================
def chart_13():
    fig, ax = plt.subplots(figsize=(9, 4.5))
    # 政策利好后股价走势
    o, c, h, l = [], [], [], []
    base = 10.0
    for i in range(8):
        oo = base + np.random.uniform(-0.3, 0.3)
        cc = oo + np.random.uniform(-0.3, 0.2)
        o.append(oo); c.append(cc); h.append(max(oo, cc) + 0.2); l.append(min(oo, cc) - 0.2)
    # 政策利好发布
    oo = c[-1]; cc = oo + 2.0
    o.append(oo); c.append(cc); h.append(cc + 0.1); l.append(oo - 0.1)
    for i in range(10):
        oo = c[-1]; cc = oo + np.random.uniform(0.2, 0.8)
        o.append(oo); c.append(cc); h.append(cc + 0.15); l.append(oo - 0.1)

    draw_candles(ax, o, c, h, l)
    ax.axvline(x=8, color="blue", linestyle="--", linewidth=1.5)
    ax.text(8.2, max(c) + 1, "国家产业政策\n利好发布", fontsize=10, color="blue")
    ax.annotate("政策面选股：紧跟国家产业政策\n优先选择政策扶持行业", xy=(12, c[12]),
                xytext=(4, c[12] + 4), fontsize=10, ha="center",
                arrowprops=dict(arrowstyle="->", color="black"))
    ax.set_title("习题1  政策面选股：从国家经济政策取向中寻找投资机会", fontsize=12)
    save(fig, "v3o-13.png")


# ============================================================
# 图14: 死亡板块
# ============================================================
def chart_14():
    fig, ax = plt.subplots(figsize=(9, 4.5))
    o, c, h, l = [], [], [], []
    base = 20.0
    # 长期阴跌
    for i in range(24):
        oo = base - i * 0.35
        cc = oo - np.random.uniform(0.1, 0.5)
        o.append(oo); c.append(cc); h.append(oo + 0.05); l.append(cc - 0.15)
    draw_candles(ax, o, c, h, l)
    ax.annotate("死亡板块：长期无人问津\n股价持续下跌 反弹无力", xy=(12, c[12]),
                xytext=(8, c[12] + 5), fontsize=10, ha="center",
                arrowprops=dict(arrowstyle="->", color="black"))
    ax.set_title("习题62  死亡板块：从死亡板块中寻找投资机会（冷门反转）", fontsize=12)
    save(fig, "v3o-14.png")


# ============================================================
# 图15: 送配转增股选股
# ============================================================
def chart_15():
    fig, ax = plt.subplots(figsize=(9, 4.5))
    o, c, h, l = [], [], [], []
    base = 15.0
    for i in range(10):
        oo = base + i * 0.2 + np.random.uniform(-0.2, 0.2)
        cc = oo + np.random.uniform(-0.1, 0.3)
        o.append(oo); c.append(cc); h.append(max(oo, cc) + 0.2); l.append(min(oo, cc) - 0.2)
    # 除权缺口
    oo = c[-1]; cc = oo * 0.6
    o.append(oo); c.append(cc); h.append(oo); l.append(cc)
    # 填权走势
    for i in range(8):
        oo = c[-1]; cc = oo + np.random.uniform(0.2, 0.7)
        o.append(oo); c.append(cc); h.append(cc + 0.15); l.append(oo - 0.1)
    draw_candles(ax, o, c, h, l)
    ax.annotate("除权缺口", xy=(10, c[10]), xytext=(10, c[10] + 2),
                fontsize=10, ha="center",
                arrowprops=dict(arrowstyle="->", color="black"))
    ax.annotate("填权行情\n高送转+业绩增长=牛股", xy=(15, c[15]),
                xytext=(15, c[15] + 3), fontsize=10, ha="center",
                arrowprops=dict(arrowstyle="->", color="black"))
    ax.set_title("习题63  从送配转增股中寻找投资机会（填权走势）", fontsize=12)
    save(fig, "v3o-15.png")


# ============================================================
# 图16: 大股东变动
# ============================================================
def chart_16():
    fig, ax = plt.subplots(figsize=(9, 4.5))
    o, c, h, l = [], [], [], []
    base = 10.0
    for i in range(10):
        oo = base + np.random.uniform(-0.3, 0.3)
        cc = oo + np.random.uniform(-0.3, 0.2)
        o.append(oo); c.append(cc); h.append(max(oo, cc) + 0.2); l.append(min(oo, cc) - 0.2)
    # 大股东入主
    oo = c[-1]; cc = oo + 1.5
    o.append(oo); c.append(cc); h.append(cc + 0.1); l.append(oo - 0.1)
    for i in range(10):
        oo = c[-1]; cc = oo + np.random.uniform(0.1, 0.7)
        o.append(oo); c.append(cc); h.append(cc + 0.15); l.append(oo - 0.1)
    draw_candles(ax, o, c, h, l)
    ax.axvline(x=10, color="blue", linestyle="--", linewidth=1.5)
    ax.text(10.2, max(c) + 1, "大股东\n变更/增持", fontsize=10, color="blue")
    ax.set_title("习题51  从大股东变动中寻找投资机会", fontsize=12)
    save(fig, "v3o-16.png")


# ============================================================
# 主函数
# ============================================================
if __name__ == "__main__":
    chart_01()
    chart_02()
    chart_03()
    chart_04()
    chart_05()
    chart_06()
    chart_07()
    chart_08()
    chart_09()
    chart_10()
    chart_11()
    chart_12()
    chart_13()
    chart_14()
    chart_15()
    chart_16()
    print("ALL DONE")
