# -*- coding: utf-8 -*-
"""第六册 实战技巧问答 重绘图生成脚本
同花顺风格：阳线#FF4444 阴线#00AA00 白底无坐标轴
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np

plt.rcParams["font.sans-serif"] = ["Microsoft JhengHei"]
plt.rcParams["axes.unicode_minus"] = False

RED = "#FF4444"
GREEN = "#00AA00"
OUT = r"E:\生活\股票操练大全全套\stock-blog\source\images\kxian"
os.makedirs(OUT, exist_ok=True)


def draw_klines(name, opens, closes, highs, lows, title="", show_ma=False,
                ma_periods=(5, 10, 30), figsize=(6.4, 4.0), vol=None):
    """绘制一组K线，红涨绿跌，白底无坐标轴。"""
    n = len(opens)
    fig, ax = plt.subplots(figsize=figsize, dpi=150)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    x = np.arange(n)
    for i in range(n):
        o, c, h, l = opens[i], closes[i], highs[i], lows[i]
        color = RED if c >= o else GREEN
        ax.plot([i, i], [l, h], color=color, linewidth=0.9)
        bottom = min(o, c)
        height = abs(c - o) if abs(c - o) > 0 else (h - l) * 0.02
        ax.bar(i, height, bottom=bottom, width=0.6, color=color, edgecolor=color)
    if show_ma:
        for p, c in zip(ma_periods, ["#333333", "#888888", "#bb8800"]):
            if n >= p:
                ma = []
                for i in range(n):
                    if i < p - 1:
                        ma.append(np.nan)
                    else:
                        ma.append(np.mean(closes[i - p + 1:i + 1]))
                ax.plot(x, ma, color=c, linewidth=1.0, label=f"MA{p}")
    ax.set_xlim(-1, n)
    ax.set_title(title, fontsize=11, color="#333333")
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    if show_ma:
        ax.legend(loc="upper left", fontsize=7, frameon=False)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, name), facecolor="white", bbox_inches="tight")
    plt.close(fig)
    print("saved", name)


def gen_up_down_pattern(seed, n, trend="up"):
    """生成带趋势的K线序列。"""
    rng = np.random.RandomState(seed)
    prices = [10.0]
    for i in range(1, n):
        drift = 0.08 if trend == "up" else (-0.08 if trend == "down" else 0.0)
        prices.append(prices[-1] + drift + rng.normal(0, 0.18))
    opens, closes, highs, lows = [], [], [], []
    for p in prices:
        o = p + rng.normal(0, 0.1)
        c = p + rng.normal(0, 0.12)
        h = max(o, c) + abs(rng.normal(0, 0.12))
        l = min(o, c) - abs(rng.normal(0, 0.12))
        opens.append(o)
        closes.append(c)
        highs.append(h)
        lows.append(l)
    return opens, closes, highs, lows


# ============ 第一章 K线 ============
# v6o-01 大阳线后五种走势示意（超强/强势/一般/偏弱/弱势）
def fig_big_yang_after():
    fig, axes = plt.subplots(1, 5, figsize=(11, 2.6), dpi=150)
    titles = ["超强", "强势", "一般", "偏弱", "弱势"]
    for k, ax in enumerate(axes):
        # 第一根大阳线
        ax.bar(0, 3.0, bottom=5.0, width=0.6, color=RED, edgecolor=RED)
        ax.plot([0, 0], [4.8, 8.2], color=RED, linewidth=0.9)
        # 第二根K线相对位置
        pos = [8.3, 7.2, 6.6, 5.8, 4.9][k]
        if k == 0:
            ax.bar(1, 1.6, bottom=pos, width=0.6, color=RED, edgecolor=RED)
        elif k == 1:
            ax.bar(1, 1.2, bottom=pos, width=0.6, color=RED, edgecolor=RED)
        elif k == 2:
            ax.bar(1, 0.9, bottom=pos, width=0.6, color=RED, edgecolor=RED)
        elif k == 3:
            ax.bar(1, 0.9, bottom=pos, width=0.6, color=GREEN, edgecolor=GREEN)
        else:
            ax.bar(1, 1.4, bottom=pos, width=0.6, color=GREEN, edgecolor=GREEN)
        ax.set_title(titles[k], fontsize=9)
        ax.set_xlim(-0.8, 1.8)
        ax.set_ylim(4.5, 9.2)
        ax.set_xticks([])
        ax.set_yticks([])
        for s in ax.spines.values():
            s.set_visible(False)
    fig.suptitle("大阳线后五种走势：第二根K线位置越高走势越强", fontsize=10, y=1.02)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "v6o-01.png"), facecolor="white", bbox_inches="tight")
    plt.close(fig)
    print("saved v6o-01.png")


# v6o-02 螺旋桨K线
def fig_luoxuanjiang():
    opens, closes, highs, lows = gen_up_down_pattern(7, 30, "up")
    # 中间加一根长上下影线
    i = 22
    opens[i], closes[i] = 12.0, 12.1
    highs[i] = 14.0
    lows[i] = 10.0
    draw_klines("v6o-02.png", opens, closes, highs, lows,
                title="螺旋桨K线：高位长上下影线，见顶信号")


# v6o-03 穿头破脚（顶部抱线）
def fig_chuantou():
    rng = np.random.RandomState(11)
    n = 18
    prices = list(np.linspace(10, 13, 12)) + [13.2, 13.5, 13.1, 12.0, 11.5]
    opens, closes, highs, lows = [], [], [], []
    for p in prices:
        o = p + rng.normal(0, 0.08)
        c = p + rng.normal(0, 0.08)
        opens.append(o); closes.append(c)
        highs.append(max(o, c) + 0.1); lows.append(min(o, c) - 0.1)
    # 第12根大阳线
    opens[11], closes[11] = 12.5, 13.5
    highs[11], lows[11] = 13.6, 12.4
    # 第13根大阴线吞没
    opens[12], closes[12] = 13.4, 12.2
    highs[12], lows[12] = 13.5, 12.1
    draw_klines("v6o-03.png", opens, closes, highs, lows,
                title="穿头破脚（顶部抱线）：大阴线吞没前阳线实体")


# v6o-04 上升三部曲变化图形
def fig_sanbuqu():
    rng = np.random.RandomState(13)
    opens = [10.0, 10.8, 11.2, 11.0, 10.8, 10.6, 10.9, 11.8,
             12.0, 12.3, 12.1, 11.9, 11.7, 12.2, 12.8]
    closes = [10.8, 11.2, 11.0, 10.8, 10.6, 10.4, 11.7, 12.0,
              12.2, 12.0, 11.8, 11.6, 12.1, 12.7, 13.2]
    highs = [c + 0.15 for c in closes]
    lows = [o - 0.15 for o in opens]
    draw_klines("v6o-04.png", opens, closes, highs, lows,
                title="上升三部曲变化图形：大阳线+小阴线整理+大阳线")


# v6o-05 下探上涨形（擎天拄）
def fig_xiatan():
    rng = np.random.RandomState(17)
    opens, closes, highs, lows = gen_up_down_pattern(17, 24, "down")
    # 最后一根大阳线
    opens[-1], closes[-1] = 9.0, 10.8
    highs[-1], lows[-1] = 10.9, 8.9
    opens[-2], closes[-2] = 9.2, 9.1
    highs[-2], lows[-2] = 9.3, 8.8
    draw_klines("v6o-05.png", opens, closes, highs, lows,
                title="下探上涨形（擎天拄）：探底后大阳线拉起")


# v6o-06 高开出逃形
def fig_gaochu():
    rng = np.random.RandomState(19)
    opens, closes, highs, lows = gen_up_down_pattern(19, 20, "up")
    # 高位大阴线
    opens[-1], closes[-1] = 13.5, 11.8
    highs[-1], lows[-1] = 13.6, 11.7
    draw_klines("v6o-06.png", opens, closes, highs, lows,
                title="高开出逃形：高位高开低走大阴线")


# v6o-07 两红夹一黑
def fig_lianghong():
    rng = np.random.RandomState(23)
    opens, closes, highs, lows = gen_up_down_pattern(23, 16, "up")
    # 中间夹一根阴线
    opens[10], closes[10] = 11.5, 11.2
    highs[10], lows[10] = 11.6, 11.1
    opens[9], closes[9] = 10.8, 11.5
    highs[9], lows[9] = 11.6, 10.7
    opens[11], closes[11] = 11.3, 12.0
    highs[11], lows[11] = 12.1, 11.2
    draw_klines("v6o-07.png", opens, closes, highs, lows,
                title="两红夹一黑：两阳夹一阴，看涨信号")


# v6o-08 多头排列 vs 空头排列
def mat_duotou_kongtou():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 3.2), dpi=150)
    for ax, trend, title in [(ax1, "up", "多头排列（看涨）"), (ax2, "down", "空头排列（看跌）")]:
        opens, closes, highs, lows = gen_up_down_pattern(31 if trend == "up" else 41, 40, trend)
        x = np.arange(40)
        for i in range(40):
            o, c, h, l = opens[i], closes[i], highs[i], lows[i]
            color = RED if c >= o else GREEN
            ax.plot([i, i], [l, h], color=color, linewidth=0.8)
            ax.bar(i, max(abs(c - o), 0.05), bottom=min(o, c), width=0.6, color=color)
        for p in (5, 10, 30):
            ma = [np.nan] * (p - 1) + [np.mean(closes[i - p + 1:i + 1]) for i in range(p - 1, 40)]
            ax.plot(x, ma, linewidth=1.0)
        ax.set_title(title, fontsize=10)
        ax.set_xlim(-1, 40); ax.set_xticks([]); ax.set_yticks([])
        for s in ax.spines.values():
            s.set_visible(False)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "v6o-08.png"), facecolor="white", bbox_inches="tight")
    plt.close(fig)
    print("saved v6o-08.png")


# ============ 第二章 技术图形 ============
# v6o-09 岛形反转
def fig_daoxing():
    rng = np.random.RandomState(51)
    n = 40
    closes = list(np.concatenate([
        np.linspace(10, 14, 12),
        np.random.RandomState(2).uniform(13.8, 14.5, 6),
        np.linspace(14, 11, 14),
        np.linspace(11, 10.5, 8)
    ]))
    opens = [c - rng.normal(0, 0.1) for c in closes]
    highs = [max(o, c) + 0.15 for o, c in zip(opens, closes)]
    lows = [min(o, c) - 0.15 for o, c in zip(opens, closes)]
    draw_klines("v6o-09.png", opens, closes, highs, lows,
                title="岛形反转：顶部左右两个反向跳空缺口")


# v6o-10 头肩底
def fig_toujiandi():
    rng = np.random.RandomState(53)
    n = 50
    # 左肩低 -> 头部更低 -> 右肩回升 -> 突破颈线
    closes = np.concatenate([
        np.linspace(12, 10, 8),
        np.random.RandomState(3).uniform(9.8, 10.3, 5),
        np.linspace(10, 8.5, 6),
        np.random.RandomState(4).uniform(8.3, 8.8, 5),
        np.linspace(8.5, 10, 6),
        np.random.RandomState(5).uniform(9.8, 10.3, 5),
        np.linspace(10, 12.5, 15)
    ])
    opens = [c - rng.normal(0, 0.12) for c in closes]
    highs = [max(o, c) + 0.15 for o, c in zip(opens, closes)]
    lows = [min(o, c) - 0.15 for o, c in zip(opens, closes)]
    draw_klines("v6o-10.png", list(opens), list(closes), list(highs), list(lows),
                title="头肩底：左肩-头部-右肩，突破颈线看涨")


# v6o-11 双顶（M头）
def fig_shuangding():
    rng = np.random.RandomState(55)
    n = 45
    closes = np.concatenate([
        np.linspace(10, 13, 10),
        np.random.RandomState(6).uniform(12.8, 13.3, 5),
        np.linspace(13, 11.5, 5),
        np.linspace(11.5, 13.2, 6),
        np.random.RandomState(7).uniform(13.0, 13.4, 4),
        np.linspace(13.2, 10.5, 15)
    ])
    opens = [c - rng.normal(0, 0.1) for c in closes]
    highs = [max(o, c) + 0.12 for o, c in zip(opens, closes)]
    lows = [min(o, c) - 0.12 for o, c in zip(opens, closes)]
    draw_klines("v6o-11.png", list(opens), list(closes), list(highs), list(lows),
                title="双顶（M头）：两次冲高回落，颈线跌破看跌")


# v6o-12 多重顶颈线跌破
def fig_duochongding():
    rng = np.random.RandomState(57)
    n = 45
    closes = np.concatenate([
        np.linspace(10, 12.5, 8),
        np.random.RandomState(8).uniform(12.3, 12.8, 6),
        np.linspace(12.5, 11.5, 4),
        np.random.RandomState(9).uniform(11.4, 12.6, 6),
        np.linspace(12.5, 11.6, 4),
        np.random.RandomState(10).uniform(11.5, 12.5, 5),
        np.linspace(12.3, 10.0, 12)
    ])
    opens = [c - rng.normal(0, 0.1) for c in closes]
    highs = [max(o, c) + 0.12 for o, c in zip(opens, closes)]
    lows = [min(o, c) - 0.12 for o, c in zip(opens, closes)]
    draw_klines("v6o-12.png", list(opens), list(closes), list(highs), list(lows),
                title="多重顶：多次冲高失败，颈线跌破后跌势加速")


# v6o-13 收敛三角形
def fig_shoulian():
    rng = np.random.RandomState(59)
    n = 35
    closes = np.array([12, 11.5, 12.2, 11.8, 12.4, 12.0, 12.5, 12.1, 12.3, 12.0,
                       12.4, 12.2, 12.35, 12.2, 12.3, 12.25, 12.3, 12.27, 12.3,
                       12.28, 12.3, 12.29, 12.3, 12.29, 12.28, 12.27, 12.26, 12.25,
                       12.0, 11.5, 11.0, 10.5, 10.0, 9.5, 9.0], dtype=float)
    opens = closes + np.random.RandomState(11).normal(0, 0.08, n)
    highs = np.maximum(opens, closes) + 0.1
    lows = np.minimum(opens, closes) - 0.1
    draw_klines("v6o-13.png", list(opens), list(closes), list(highs), list(lows),
                title="收敛三角形：波动收窄后向下突破")


# v6o-14 圆顶圆底
def fig_yuanxing():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 3.0), dpi=150)
    rng = np.random.RandomState(61)
    for ax, arr, title in [
        (ax1, np.concatenate([np.linspace(10, 13, 12), np.linspace(13, 10, 12)]), "圆顶"),
        (ax2, np.concatenate([np.linspace(13, 10, 12), np.linspace(10, 13, 12)]), "圆底"),
    ]:
        n = len(arr)
        opens = arr + rng.normal(0, 0.1, n)
        highs = np.maximum(opens, arr) + 0.12
        lows = np.minimum(opens, arr) - 0.12
        x = np.arange(n)
        for i in range(n):
            color = RED if arr[i] >= opens[i] else GREEN
            ax.plot([i, i], [lows[i], highs[i]], color=color, linewidth=0.8)
            ax.bar(i, max(abs(arr[i] - opens[i]), 0.05), bottom=min(arr[i], opens[i]),
                   width=0.6, color=color)
        ax.set_title(title, fontsize=10)
        ax.set_xlim(-1, n); ax.set_xticks([]); ax.set_yticks([])
        for s in ax.spines.values():
            s.set_visible(False)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "v6o-14.png"), facecolor="white", bbox_inches="tight")
    plt.close(fig)
    print("saved v6o-14.png")


# ============ 第三章 均线 ============
# v6o-15 银山谷/金山谷/死亡谷
def fig_gu():
    rng = np.random.RandomState(71)
    n = 60
    closes = np.concatenate([
        np.linspace(12, 9, 15),      # 下跌
        np.linspace(9, 10.5, 8),     # 银山谷反弹
        np.linspace(10.5, 9.8, 6),   # 回抽
        np.linspace(9.8, 11.5, 8),    # 金山谷
        np.linspace(11.5, 14, 15),   # 上涨
        np.linspace(14, 12.5, 8),    # 死亡谷
    ])
    opens = closes + rng.normal(0, 0.15, n)
    highs = np.maximum(opens, closes) + 0.2
    lows = np.minimum(opens, closes) - 0.2
    fig, ax = plt.subplots(figsize=(7, 3.6), dpi=150)
    x = np.arange(n)
    for i in range(n):
        color = RED if closes[i] >= opens[i] else GREEN
        ax.plot([i, i], [lows[i], highs[i]], color=color, linewidth=0.8)
        ax.bar(i, max(abs(closes[i] - opens[i]), 0.05), bottom=min(closes[i], opens[i]),
               width=0.6, color=color)
    for p, c in [(5, "#333"), (10, "#888"), (30, "#bb8800")]:
        ma = [np.nan] * (p - 1) + [np.mean(closes[i - p + 1:i + 1]) for i in range(p - 1, n)]
        ax.plot(x, ma, color=c, linewidth=1.0, label=f"MA{p}")
    ax.annotate("银山谷", xy=(22, 10.3), fontsize=8, color="blue")
    ax.annotate("金山谷", xy=(40, 11.3), fontsize=8, color="red")
    ax.annotate("死亡谷", xy=(55, 13.2), fontsize=8, color="green")
    ax.set_title("银山谷、金山谷与死亡谷（均线交叉形态）", fontsize=10)
    ax.set_xlim(-1, n); ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    ax.legend(loc="upper left", fontsize=7, frameon=False)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "v6o-15.png"), facecolor="white", bbox_inches="tight")
    plt.close(fig)
    print("saved v6o-15.png")


# v6o-16 均线粘合向上发散
def fig_nianhe():
    rng = np.random.RandomState(73)
    n = 50
    closes = np.concatenate([
        np.linspace(10, 10.2, 25) + rng.normal(0, 0.05, 25),  # 粘合
        np.linspace(10.2, 13.5, 25) + rng.normal(0, 0.1, 25)  # 发散向上
    ])
    opens = closes + rng.normal(0, 0.1, n)
    highs = np.maximum(opens, closes) + 0.12
    lows = np.minimum(opens, closes) - 0.12
    fig, ax = plt.subplots(figsize=(7, 3.6), dpi=150)
    x = np.arange(n)
    for i in range(n):
        color = RED if closes[i] >= opens[i] else GREEN
        ax.plot([i, i], [lows[i], highs[i]], color=color, linewidth=0.8)
        ax.bar(i, max(abs(closes[i] - opens[i]), 0.05), bottom=min(closes[i], opens[i]),
               width=0.6, color=color)
    for p, c in [(5, "#333"), (10, "#888"), (30, "#bb8800")]:
        ma = [np.nan] * (p - 1) + [np.mean(closes[i - p + 1:i + 1]) for i in range(p - 1, n)]
        ax.plot(x, ma, color=c, linewidth=1.0, label=f"MA{p}")
    ax.set_title("均线粘合后向上发散：多头启动信号", fontsize=10)
    ax.set_xlim(-1, n); ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    ax.legend(loc="upper left", fontsize=7, frameon=False)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "v6o-16.png"), facecolor="white", bbox_inches="tight")
    plt.close(fig)
    print("saved v6o-16.png")


# v6o-17 黄金交叉与死亡交叉
def fig_jincha():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 3.2), dpi=150)
    for ax, trend, title in [(ax1, "up", "黄金交叉（5日线上穿10日线）"),
                              (ax2, "down", "死亡交叉（5日线下穿10日线）")]:
        opens, closes, highs, lows = gen_up_down_pattern(77 if trend == "up" else 78, 35, trend)
        x = np.arange(35)
        for i in range(35):
            o, c, h, l = opens[i], closes[i], highs[i], lows[i]
            color = RED if c >= o else GREEN
            ax.plot([i, i], [l, h], color=color, linewidth=0.8)
            ax.bar(i, max(abs(c - o), 0.05), bottom=min(o, c), width=0.6, color=color)
        ma5 = [np.nan] * 4 + [np.mean(closes[i - 4:i + 1]) for i in range(4, 35)]
        ma10 = [np.nan] * 9 + [np.mean(closes[i - 9:i + 1]) for i in range(9, 35)]
        ax.plot(x, ma5, color="#333", linewidth=1.0, label="MA5")
        ax.plot(x, ma10, color="#888", linewidth=1.0, label="MA10")
        ax.set_title(title, fontsize=9)
        ax.set_xlim(-1, 35); ax.set_xticks([]); ax.set_yticks([])
        for s in ax.spines.values():
            s.set_visible(False)
        ax.legend(loc="upper left", fontsize=7, frameon=False)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "v6o-17.png"), facecolor="white", bbox_inches="tight")
    plt.close(fig)
    print("saved v6o-17.png")


# v6o-18 上升通道
def fig_tongdao():
    rng = np.random.RandomState(81)
    n = 40
    closes = np.linspace(10, 14, n) + rng.normal(0, 0.2, n)
    opens = closes + rng.normal(0, 0.12, n)
    highs = np.maximum(opens, closes) + 0.25
    lows = np.minimum(opens, closes) - 0.25
    fig, ax = plt.subplots(figsize=(7, 3.6), dpi=150)
    x = np.arange(n)
    for i in range(n):
        color = RED if closes[i] >= opens[i] else GREEN
        ax.plot([i, i], [lows[i], highs[i]], color=color, linewidth=0.8)
        ax.bar(i, max(abs(closes[i] - opens[i]), 0.05), bottom=min(closes[i], opens[i]),
               width=0.6, color=color)
    ax.plot(x, np.linspace(10.5, 14.5, n), "r--", linewidth=1.0, label="上轨线")
    ax.plot(x, np.linspace(9.5, 13.5, n), "g--", linewidth=1.0, label="下轨线")
    ax.set_title("上升通道：上轨阻力、下轨支撑", fontsize=10)
    ax.set_xlim(-1, n); ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    ax.legend(loc="upper left", fontsize=7, frameon=False)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "v6o-18.png"), facecolor="white", bbox_inches="tight")
    plt.close(fig)
    print("saved v6o-18.png")


# v6o-19 支撑线与压力线（反弹遇阻）
def fig_zhiyali():
    rng = np.random.RandomState(83)
    n = 45
    closes = np.concatenate([
        np.linspace(14, 10, 15),
        np.linspace(10, 12.5, 10),
        np.linspace(12.5, 9.5, 20),
    ]) + rng.normal(0, 0.15, 45)
    opens = closes + rng.normal(0, 0.1, 45)
    highs = np.maximum(opens, closes) + 0.2
    lows = np.minimum(opens, closes) - 0.2
    fig, ax = plt.subplots(figsize=(7, 3.6), dpi=150)
    x = np.arange(45)
    for i in range(45):
        color = RED if closes[i] >= opens[i] else GREEN
        ax.plot([i, i], [lows[i], highs[i]], color=color, linewidth=0.8)
        ax.bar(i, max(abs(closes[i] - opens[i]), 0.05), bottom=min(closes[i], opens[i]),
               width=0.6, color=color)
    ax.axhline(y=12.8, color="red", linestyle="--", linewidth=1.0)
    ax.text(1, 13.0, "压力线（反弹高点连线）", fontsize=8, color="red")
    ax.set_title("下降趋势中反弹至压力线遇阻回落", fontsize=10)
    ax.set_xlim(-1, 45); ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "v6o-19.png"), facecolor="white", bbox_inches="tight")
    plt.close(fig)
    print("saved v6o-19.png")


# v6o-20 月K线看大势（牛熊转换）
def fig_yuexian():
    rng = np.random.RandomState(87)
    n = 60
    closes = np.concatenate([
        np.linspace(1500, 2200, 10),   # 2001见顶
        np.linspace(2200, 998, 30),    # 2001-2005大熊
        np.linspace(998, 2700, 20),    # 2005-2006大牛
    ])
    opens = closes + rng.normal(0, 30, n)
    highs = np.maximum(opens, closes) + 40
    lows = np.minimum(opens, closes) - 40
    fig, ax = plt.subplots(figsize=(7, 3.6), dpi=150)
    x = np.arange(n)
    for i in range(n):
        color = RED if closes[i] >= opens[i] else GREEN
        ax.plot([i, i], [lows[i], highs[i]], color=color, linewidth=0.8)
        ax.bar(i, max(abs(closes[i] - opens[i]), 30), bottom=min(closes[i], opens[i]),
               width=0.6, color=color)
    ax.set_title("月K线看大势：2245点大熊至998点反转走牛", fontsize=10)
    ax.set_xlim(-1, n); ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "v6o-20.png"), facecolor="white", bbox_inches="tight")
    plt.close(fig)
    print("saved v6o-20.png")


# v6o-21 主力洗盘 vs 出货
def fig_xipan():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 3.2), dpi=150)
    for ax, trend, title in [(ax1, "up", "洗盘：缩量回档后继续上行"),
                              (ax2, "down", "出货：高位放量后持续下跌")]:
        opens, closes, highs, lows = gen_up_down_pattern(91 if trend == "up" else 92, 30, trend)
        x = np.arange(30)
        for i in range(30):
            o, c, h, l = opens[i], closes[i], highs[i], lows[i]
            color = RED if c >= o else GREEN
            ax.plot([i, i], [l, h], color=color, linewidth=0.8)
            ax.bar(i, max(abs(c - o), 0.05), bottom=min(o, c), width=0.6, color=color)
        ax.set_title(title, fontsize=9)
        ax.set_xlim(-1, 30); ax.set_xticks([]); ax.set_yticks([])
        for s in ax.spines.values():
            s.set_visible(False)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "v6o-21.png"), facecolor="white", bbox_inches="tight")
    plt.close(fig)
    print("saved v6o-21.png")


# v6o-22 假突破（多头陷阱）
def fig_jiatupo():
    rng = np.random.RandomState(93)
    n = 45
    closes = np.concatenate([
        np.linspace(10, 12, 10),
        np.linspace(12, 11.5, 8),
        np.linspace(11.5, 12.5, 5),   # 假突破
        np.linspace(12.5, 9, 22),     # 暴跌
    ])
    opens = closes + rng.normal(0, 0.12, n)
    highs = np.maximum(opens, closes) + 0.2
    lows = np.minimum(opens, closes) - 0.2
    fig, ax = plt.subplots(figsize=(7, 3.6), dpi=150)
    x = np.arange(n)
    for i in range(n):
        color = RED if closes[i] >= opens[i] else GREEN
        ax.plot([i, i], [lows[i], highs[i]], color=color, linewidth=0.8)
        ax.bar(i, max(abs(closes[i] - opens[i]), 0.05), bottom=min(closes[i], opens[i]),
               width=0.6, color=color)
    ax.axhline(y=12.0, color="red", linestyle="--", linewidth=0.8)
    ax.text(1, 12.1, "前高阻力位", fontsize=8, color="red")
    ax.set_title("假突破（多头陷阱）：短暂突破前高后暴跌", fontsize=10)
    ax.set_xlim(-1, n); ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "v6o-22.png"), facecolor="white", bbox_inches="tight")
    plt.close(fig)
    print("saved v6o-22.png")


# v6o-23 牛熊转换点（998点见底）
def fig_niuxiong():
    rng = np.random.RandomState(95)
    n = 50
    closes = np.concatenate([
        np.linspace(1400, 1000, 25) + rng.normal(0, 30, 25),
        np.linspace(1000, 2600, 25) + rng.normal(0, 40, 25),
    ])
    opens = closes + rng.normal(0, 30, n)
    highs = np.maximum(opens, closes) + 50
    lows = np.minimum(opens, closes) - 50
    fig, ax = plt.subplots(figsize=(7, 3.6), dpi=150)
    x = np.arange(n)
    for i in range(n):
        color = RED if closes[i] >= opens[i] else GREEN
        ax.plot([i, i], [lows[i], highs[i]], color=color, linewidth=0.8)
        ax.bar(i, max(abs(closes[i] - opens[i]), 30), bottom=min(closes[i], opens[i]),
               width=0.6, color=color)
    ax.annotate("998点\n大底", xy=(25, 1000), xytext=(32, 1300),
                fontsize=9, color="red",
                arrowprops=dict(arrowstyle="->", color="red"))
    ax.set_title("牛熊转换：998点见底后走大牛市", fontsize=10)
    ax.set_xlim(-1, n); ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "v6o-23.png"), facecolor="white", bbox_inches="tight")
    plt.close(fig)
    print("saved v6o-23.png")


# v6o-24 成交量配合
def fig_chengjiaoliang():
    rng = np.random.RandomState(97)
    n = 40
    closes = np.concatenate([
        np.linspace(10, 10.5, 10) + rng.normal(0, 0.1, 10),
        np.linspace(10.5, 13, 15) + rng.normal(0, 0.15, 15),
        np.linspace(13, 12.5, 15) + rng.normal(0, 0.15, 15),
    ])
    opens = closes + rng.normal(0, 0.1, n)
    highs = np.maximum(opens, closes) + 0.15
    lows = np.minimum(opens, closes) - 0.15
    vols = np.concatenate([
        np.ones(10) * 100,
        np.linspace(100, 500, 15),
        np.linspace(500, 200, 15),
    ])
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7, 4.2), dpi=150,
                                   gridspec_kw={"height_ratios": [3, 1]})
    x = np.arange(n)
    for i in range(n):
        color = RED if closes[i] >= opens[i] else GREEN
        ax1.plot([i, i], [lows[i], highs[i]], color=color, linewidth=0.8)
        ax1.bar(i, max(abs(closes[i] - opens[i]), 0.05), bottom=min(closes[i], opens[i]),
                width=0.6, color=color)
    ax1.set_title("量价配合：上涨放量、回调缩量为健康走势", fontsize=10)
    ax1.set_xlim(-1, n); ax1.set_xticks([]); ax1.set_yticks([])
    for s in ax1.spines.values():
        s.set_visible(False)
    for i in range(n):
        color = RED if closes[i] >= opens[i] else GREEN
        ax2.bar(i, vols[i], width=0.6, color=color, alpha=0.7)
    ax2.set_xlim(-1, n); ax2.set_xticks([]); ax2.set_yticks([])
    for s in ax2.spines.values():
        s.set_visible(False)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "v6o-24.png"), facecolor="white", bbox_inches="tight")
    plt.close(fig)
    print("saved v6o-24.png")


# v6o-25 白马股长线走牛
def fig_baima():
    rng = np.random.RandomState(99)
    n = 80
    closes = np.linspace(8, 30, n) + rng.normal(0, 0.5, n)
    opens = closes + rng.normal(0, 0.2, n)
    highs = np.maximum(opens, closes) + 0.5
    lows = np.minimum(opens, closes) - 0.5
    fig, ax = plt.subplots(figsize=(7, 3.6), dpi=150)
    x = np.arange(n)
    for i in range(n):
        color = RED if closes[i] >= opens[i] else GREEN
        ax.plot([i, i], [lows[i], highs[i]], color=color, linewidth=0.7)
        ax.bar(i, max(abs(closes[i] - opens[i]), 0.1), bottom=min(closes[i], opens[i]),
               width=0.6, color=color)
    for p, c in [(20, "#bb8800"), (60, "#333")]:
        ma = [np.nan] * (p - 1) + [np.mean(closes[i - p + 1:i + 1]) for i in range(p - 1, n)]
        ax.plot(x, ma, color=c, linewidth=1.0, label=f"MA{p}")
    ax.set_title("白马股长线走牛：业绩支撑下慢牛上行", fontsize=10)
    ax.set_xlim(-1, n); ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    ax.legend(loc="upper left", fontsize=7, frameon=False)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "v6o-25.png"), facecolor="white", bbox_inches="tight")
    plt.close(fig)
    print("saved v6o-25.png")


if __name__ == "__main__":
    fig_big_yang_after()
    fig_luoxuanjiang()
    fig_chuantou()
    fig_sanbuqu()
    fig_xiatan()
    fig_gaochu()
    fig_lianghong()
    mat_duotou_kongtou()
    fig_daoxing()
    fig_toujiandi()
    fig_shuangding()
    fig_duochongding()
    fig_shoulian()
    fig_yuanxing()
    fig_gu()
    fig_nianhe()
    fig_jincha()
    fig_tongdao()
    fig_zhiyali()
    fig_yuexian()
    fig_xipan()
    fig_jiatupo()
    fig_niuxiong()
    fig_chengjiaoliang()
    fig_baima()
    print("ALL DONE")
