# -*- coding: utf-8 -*-
"""Generate Tonghuashun-style K-line illustrations for articles 8/9/10."""
import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'FangSong', 'SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

OUT = r"E:\生活\股票操练大全全套\stock-blog\source\images\kxian"
os.makedirs(OUT, exist_ok=True)

RED = '#FF4444'
GREEN = '#00AA00'


def draw_kline(ax, x, o, c, h, l, width=0.3):
    color = RED if c >= o else GREEN
    ax.plot([x, x], [l, h], color=color, linewidth=1.2)
    bottom = min(o, c)
    height = abs(c - o)
    if height < 0.02:
        height = 0.02
    rect = patches.Rectangle((x - width / 2, bottom), width, height,
                             facecolor=color, edgecolor=color, linewidth=1)
    ax.add_patch(rect)


def new_fig(figsize=(5, 3), sub=False):
    if sub:
        fig, axes = plt.subplots(1, 2, figsize=figsize)
        for ax in axes:
            ax.axis('off')
        return fig, axes
    fig, ax = plt.subplots(figsize=figsize)
    ax.axis('off')
    return fig, ax


def save_fig(fig, name):
    path = os.path.join(OUT, name)
    plt.savefig(path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print("saved", path)


def set_lims(ax, xs, pad=1.0):
    ax.set_xlim(min(xs) - pad, max(xs) + pad)


# ============ 篇8 ============

# kx08-01 冉冉上升形: 9 small candles, slight upward slope, mostly small yang
def kx08_01():
    fig, ax = new_fig()
    # base prices drifting up slowly
    data = [
        # o, c, h, l  (small yang 7, small yin 2)
        (10.00, 10.15, 10.20, 9.95),
        (10.15, 10.10, 10.25, 10.05),
        (10.10, 10.28, 10.32, 10.08),
        (10.28, 10.40, 10.45, 10.22),
        (10.40, 10.35, 10.48, 10.30),
        (10.35, 10.55, 10.60, 10.32),
        (10.55, 10.70, 10.75, 10.50),
        (10.70, 10.85, 10.90, 10.65),
        (10.85, 11.05, 11.12, 10.80),
    ]
    for i, (o, c, h, l) in enumerate(data):
        draw_kline(ax, i + 1, o, c, h, l)
    set_lims(ax, range(1, len(data) + 1))
    ax.set_ylim(9.8, 11.3)
    save_fig(fig, "kx08-01.png")


# kx08-02 绵绵阴跌形: 9 small candles, slight downward slope, mostly small yin
def kx08_02():
    fig, ax = new_fig()
    data = [
        (11.00, 10.85, 11.05, 10.80),
        (10.85, 10.90, 10.95, 10.78),
        (10.90, 10.72, 10.92, 10.68),
        (10.72, 10.60, 10.78, 10.55),
        (10.60, 10.65, 10.72, 10.55),
        (10.65, 10.48, 10.68, 10.45),
        (10.48, 10.35, 10.52, 10.30),
        (10.35, 10.20, 10.40, 10.15),
        (10.20, 10.05, 10.25, 10.00),
    ]
    for i, (o, c, h, l) in enumerate(data):
        draw_kline(ax, i + 1, o, c, h, l)
    set_lims(ax, range(1, len(data) + 1))
    ax.set_ylim(9.9, 11.2)
    save_fig(fig, "kx08-02.png")


# kx08-03 徐缓上升形: few small yang then 1-2 big yang
def kx08_03():
    fig, ax = new_fig()
    data = [
        (10.00, 10.15, 10.20, 9.95),
        (10.15, 10.28, 10.33, 10.10),
        (10.28, 10.42, 10.48, 10.24),
        (10.42, 10.55, 10.62, 10.38),
        (10.55, 10.70, 10.78, 10.50),
        # big yang
        (10.70, 11.45, 11.55, 10.68),
        # another big yang
        (11.45, 12.10, 12.25, 11.40),
    ]
    for i, (o, c, h, l) in enumerate(data):
        draw_kline(ax, i + 1, o, c, h, l)
    set_lims(ax, range(1, len(data) + 1))
    ax.set_ylim(9.8, 12.5)
    save_fig(fig, "kx08-03.png")


# kx08-04 上升抵抗形: continuous high opens, yang with few yin but yin close > prev close
def kx08_04():
    fig, ax = new_fig()
    # each candle opens higher than previous close; even yin closes above prev close
    closes = [10.20, 10.45, 10.60, 10.85, 11.00, 11.30, 11.55, 11.80, 12.10]
    opens = [10.05, 10.35, 10.55, 10.75, 10.95, 11.20, 11.50, 11.70, 12.00]
    # make 2 yin candles (close < open) but still above prev close
    # index 3: open 10.85, close 10.78 (yin, but close 10.78 > prev close 10.60)
    # index 6: open 11.60, close 11.50 (yin, but close 11.50 > prev close 11.30)
    opens = [10.05, 10.35, 10.55, 10.85, 11.00, 11.25, 11.60, 11.85, 12.05]
    closes = [10.20, 10.45, 10.60, 10.78, 11.05, 11.30, 11.50, 11.85, 12.15]
    for i in range(9):
        o = opens[i]
        c = closes[i]
        h = max(o, c) + 0.12
        l = min(o, c) - 0.10
        draw_kline(ax, i + 1, o, c, h, l)
    set_lims(ax, range(1, 10))
    ax.set_ylim(9.9, 12.4)
    save_fig(fig, "kx08-04.png")


# kx08-05 稳步上涨形: many yang with few small yin, steady up
def kx08_05():
    fig, ax = new_fig()
    data = [
        (10.00, 10.30, 10.38, 9.95),
        (10.30, 10.55, 10.62, 10.25),
        (10.55, 10.45, 10.65, 10.40),  # small yin
        (10.45, 10.85, 10.95, 10.42),
        (10.85, 11.10, 11.20, 10.80),
        (11.10, 11.00, 11.20, 10.95),  # small yin
        (11.00, 11.45, 11.55, 10.95),
        (11.45, 11.75, 11.85, 11.40),
        (11.75, 11.65, 11.85, 11.60),  # small yin
        (11.65, 12.10, 12.20, 11.60),
        (12.10, 12.45, 12.55, 12.05),
    ]
    for i, (o, c, h, l) in enumerate(data):
        draw_kline(ax, i + 1, o, c, h, l)
    set_lims(ax, range(1, len(data) + 1))
    ax.set_ylim(9.8, 12.8)
    save_fig(fig, "kx08-05.png")


# ============ 篇9 ============

# kx09-01 高位并排阳线 vs 低位并排阳线
def kx09_01():
    fig, axes = new_fig(figsize=(8, 3), sub=True)
    ax1, ax2 = axes

    # left: high position parallel yang - rising then two parallel gap-up yang
    data1 = [
        (10.00, 10.30, 10.38, 9.95),
        (10.30, 10.60, 10.68, 10.25),
        (10.60, 10.90, 10.98, 10.55),
        # gap up: open 11.15
        (11.15, 11.45, 11.55, 11.10),
        # parallel same open
        (11.15, 11.50, 11.60, 11.10),
    ]
    for i, (o, c, h, l) in enumerate(data1):
        draw_kline(ax1, i + 1, o, c, h, l, width=0.35)
    set_lims(ax1, range(1, len(data1) + 1))
    ax1.set_ylim(9.8, 11.8)
    ax1.set_title("高位并排阳线", fontsize=11)

    # right: low position parallel yang - decline then gap-down yang + parallel yang
    data2 = [
        (12.00, 11.70, 12.05, 11.65),
        (11.70, 11.40, 11.75, 11.35),
        (11.40, 11.10, 11.45, 11.05),
        # gap down open
        (10.85, 11.15, 11.25, 10.80),
        # parallel
        (10.85, 11.20, 11.30, 10.80),
    ]
    for i, (o, c, h, l) in enumerate(data2):
        draw_kline(ax2, i + 1, o, c, h, l, width=0.35)
    set_lims(ax2, range(1, len(data2) + 1))
    ax2.set_ylim(10.6, 12.2)
    ax2.set_title("低位并排阳线", fontsize=11)
    save_fig(fig, "kx09-01.png")


# kx09-02 上档盘旋形: rise then sideways small candles
def kx09_02():
    fig, ax = new_fig()
    data = [
        (10.00, 10.55, 10.65, 9.95),
        (10.55, 11.10, 11.20, 10.50),
        # sideways small candles
        (11.10, 11.20, 11.30, 11.00),
        (11.20, 11.12, 11.28, 11.02),
        (11.12, 11.25, 11.35, 11.08),
        (11.25, 11.18, 11.32, 11.05),
        (11.18, 11.30, 11.40, 11.10),
        (11.30, 11.22, 11.38, 11.12),
        (11.22, 11.35, 11.45, 11.15),
    ]
    for i, (o, c, h, l) in enumerate(data):
        draw_kline(ax, i + 1, o, c, h, l)
    set_lims(ax, range(1, len(data) + 1))
    ax.set_ylim(9.8, 11.6)
    save_fig(fig, "kx09-02.png")


# kx09-03 多方尖兵 vs 空方尖兵
def kx09_03():
    fig, axes = new_fig(figsize=(8, 3), sub=True)
    ax1, ax2 = axes

    # left: 多方尖兵 - rise, long upper shadow, pullback, then break through upper shadow
    data1 = [
        (10.00, 10.20, 10.28, 9.95),
        (10.20, 10.45, 10.55, 10.15),
        # probe with long upper shadow (yang body, long wick)
        (10.45, 10.60, 11.30, 10.40),
        # pullback
        (10.60, 10.45, 10.65, 10.35),
        (10.45, 10.70, 10.80, 10.40),
        # break through upper shadow
        (10.70, 11.45, 11.60, 10.65),
    ]
    for i, (o, c, h, l) in enumerate(data1):
        draw_kline(ax1, i + 1, o, c, h, l, width=0.35)
    set_lims(ax1, range(1, len(data1) + 1))
    ax1.set_ylim(9.8, 11.8)
    ax1.set_title("多方尖兵", fontsize=11)

    # right: 空方尖兵 - decline, long lower shadow, bounce, then break through lower shadow
    data2 = [
        (12.00, 11.80, 12.05, 11.75),
        (11.80, 11.55, 11.85, 11.50),
        # probe with long lower shadow (yin body, long wick)
        (11.55, 11.40, 11.60, 10.70),
        # bounce
        (11.40, 11.55, 11.65, 11.35),
        (11.55, 11.30, 11.60, 11.25),
        # break through lower shadow
        (11.30, 10.55, 11.35, 10.40),
    ]
    for i, (o, c, h, l) in enumerate(data2):
        draw_kline(ax2, i + 1, o, c, h, l, width=0.35)
    set_lims(ax2, range(1, len(data2) + 1))
    ax2.set_ylim(10.2, 12.2)
    ax2.set_title("空方尖兵", fontsize=11)
    save_fig(fig, "kx09-03.png")


# kx09-04 上涨二颗星 vs 下跌三颗星
def kx09_04():
    fig, axes = new_fig(figsize=(8, 3), sub=True)
    ax1, ax2 = axes

    # left: 上涨二颗星 - big yang then 2 small stars above
    data1 = [
        (10.00, 10.30, 10.38, 9.95),
        (10.30, 10.60, 10.68, 10.25),
        (10.60, 11.30, 11.45, 10.55),  # big yang
        (11.30, 11.40, 11.55, 11.25),  # small star
        (11.40, 11.35, 11.52, 11.20),  # small star
    ]
    for i, (o, c, h, l) in enumerate(data1):
        draw_kline(ax1, i + 1, o, c, h, l, width=0.35)
    set_lims(ax1, range(1, len(data1) + 1))
    ax1.set_ylim(9.8, 11.8)
    ax1.set_title("上涨二颗星", fontsize=11)

    # right: 下跌三颗星 - decline then 3 small stars
    data2 = [
        (12.00, 11.70, 12.05, 11.65),
        (11.70, 11.30, 11.75, 11.25),
        (11.30, 10.70, 11.35, 10.60),  # big yin
        (10.70, 10.60, 10.78, 10.50),  # small star
        (10.60, 10.65, 10.75, 10.52),  # small star
        (10.65, 10.55, 10.72, 10.45),  # small star
    ]
    for i, (o, c, h, l) in enumerate(data2):
        draw_kline(ax2, i + 1, o, c, h, l, width=0.35)
    set_lims(ax2, range(1, len(data2) + 1))
    ax2.set_ylim(10.2, 12.2)
    ax2.set_title("下跌三颗星", fontsize=11)
    save_fig(fig, "kx09-04.png")


# kx09-05 连续跳空三阳线: 3 gap-up yang lines
def kx09_05():
    fig, ax = new_fig()
    data = [
        (10.00, 10.30, 10.38, 9.95),
        # gap up 1
        (10.60, 10.95, 11.05, 10.55),
        # gap up 2
        (11.25, 11.60, 11.70, 11.20),
        # gap up 3
        (11.90, 12.25, 12.40, 11.85),
    ]
    for i, (o, c, h, l) in enumerate(data):
        draw_kline(ax, i + 1, o, c, h, l, width=0.35)
    set_lims(ax, range(1, len(data) + 1))
    ax.set_ylim(9.8, 12.6)
    save_fig(fig, "kx09-05.png")


# kx09-06 跳空上扬形: gap-up yang then yin, gap not filled
def kx09_06():
    fig, ax = new_fig()
    data = [
        (10.00, 10.30, 10.38, 9.95),
        (10.30, 10.55, 10.65, 10.25),
        # gap up yang
        (10.90, 11.40, 11.55, 10.85),
        # yin, close near gap, gap not filled (low > prev close 10.55)
        (11.35, 10.95, 11.45, 10.80),
        # resume up
        (10.95, 11.50, 11.65, 10.90),
    ]
    for i, (o, c, h, l) in enumerate(data):
        draw_kline(ax, i + 1, o, c, h, l, width=0.35)
    set_lims(ax, range(1, len(data) + 1))
    ax.set_ylim(9.8, 11.9)
    save_fig(fig, "kx09-06.png")


# ============ 篇10 ============

# kx10-01 下降覆盖线: rise then long yin covering previous yang
def kx10_01():
    fig, ax = new_fig()
    data = [
        (10.00, 10.30, 10.38, 9.95),
        (10.30, 10.65, 10.75, 10.25),
        # 穿头破脚 yin (opens above prev high, closes below prev low)
        (10.80, 10.20, 10.85, 10.10),
        # yang
        (10.20, 10.55, 10.70, 10.15),
        # low-close yin deep into yang
        (10.50, 10.05, 10.55, 9.95),
    ]
    for i, (o, c, h, l) in enumerate(data):
        draw_kline(ax, i + 1, o, c, h, l, width=0.35)
    set_lims(ax, range(1, len(data) + 1))
    ax.set_ylim(9.8, 11.0)
    save_fig(fig, "kx10-01.png")


# kx10-02 加速度线: 3 increasingly long yang (rising acceleration)
def kx10_02():
    fig, ax = new_fig()
    data = [
        (10.00, 10.15, 10.22, 9.95),
        (10.15, 10.35, 10.45, 10.10),
        # increasingly big yang
        (10.35, 10.85, 10.95, 10.30),
        (10.85, 11.60, 11.75, 10.80),
        (11.60, 12.60, 12.80, 11.55),
    ]
    for i, (o, c, h, l) in enumerate(data):
        draw_kline(ax, i + 1, o, c, h, l, width=0.35)
    set_lims(ax, range(1, len(data) + 1))
    ax.set_ylim(9.8, 13.0)
    save_fig(fig, "kx10-02.png")


# kx10-03 弧形线: arc bottom
def kx10_03():
    fig, ax = new_fig()
    # arc bottom: start low, dip, then rise slowly forming parabola
    data = [
        (10.50, 10.30, 10.55, 10.25),
        (10.30, 10.10, 10.35, 10.05),
        (10.10, 9.95, 10.15, 9.85),
        (9.95, 9.85, 10.00, 9.75),
        (9.85, 9.90, 10.05, 9.75),
        (9.90, 10.05, 10.20, 9.85),
        (10.05, 10.25, 10.40, 10.00),
        (10.25, 10.50, 10.65, 10.20),
        (10.50, 10.80, 10.95, 10.45),
        (10.80, 11.15, 11.30, 10.75),
    ]
    for i, (o, c, h, l) in enumerate(data):
        draw_kline(ax, i + 1, o, c, h, l, width=0.35)
    set_lims(ax, range(1, len(data) + 1))
    ax.set_ylim(9.5, 11.5)
    save_fig(fig, "kx10-03.png")


# kx10-04 镊子线: 3 candles, high prices nearly same
def kx10_04():
    fig, ax = new_fig()
    # top tweezers: three candles, highs at same level, middle candle at top
    data = [
        (10.00, 10.40, 10.70, 9.95),   # yang, high 10.70
        (10.40, 10.55, 10.70, 10.30),  # middle candle, high 10.70
        (10.55, 10.20, 10.70, 10.10),  # yin, high 10.70
    ]
    for i, (o, c, h, l) in enumerate(data):
        draw_kline(ax, i + 1, o, c, h, l, width=0.4)
    set_lims(ax, range(1, len(data) + 1))
    ax.set_ylim(9.8, 11.0)
    save_fig(fig, "kx10-04.png")


# kx10-05 尽头线 vs 搓揉线
def kx10_05():
    fig, axes = new_fig(figsize=(8, 3), sub=True)
    ax1, ax2 = axes

    # left: 尽头线 - long yang with upper shadow, then small candle fully within upper shadow
    data1 = [
        (10.00, 10.30, 10.38, 9.95),
        (10.30, 10.55, 10.62, 10.25),
        # long yang with long upper shadow
        (10.55, 11.20, 11.80, 10.50),
        # small candle fully within upper shadow range (11.20~11.80)
        (11.40, 11.50, 11.55, 11.35),
    ]
    for i, (o, c, h, l) in enumerate(data1):
        draw_kline(ax1, i + 1, o, c, h, l, width=0.35)
    set_lims(ax1, range(1, len(data1) + 1))
    ax1.set_ylim(9.8, 12.0)
    ax1.set_title("尽头线", fontsize=11)

    # right: 搓揉线 - T字线 then 倒T字线
    data2 = [
        (10.00, 10.30, 10.38, 9.95),
        (10.30, 10.55, 10.62, 10.25),
        # T字线: open=close, long lower shadow
        (10.60, 10.60, 10.68, 10.00),
        # 倒T字线: open=close, long upper shadow
        (10.62, 10.62, 11.20, 10.55),
    ]
    for i, (o, c, h, l) in enumerate(data2):
        draw_kline(ax2, i + 1, o, c, h, l, width=0.35)
    set_lims(ax2, range(1, len(data2) + 1))
    ax2.set_ylim(9.8, 11.4)
    ax2.set_title("搓揉线", fontsize=11)
    save_fig(fig, "kx10-05.png")


if __name__ == "__main__":
    kx08_01()
    kx08_02()
    kx08_03()
    kx08_04()
    kx08_05()
    kx09_01()
    kx09_02()
    kx09_03()
    kx09_04()
    kx09_05()
    kx09_06()
    kx10_01()
    kx10_02()
    kx10_03()
    kx10_04()
    kx10_05()
    print("ALL DONE")
