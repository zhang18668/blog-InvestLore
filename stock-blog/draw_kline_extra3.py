import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'FangSong', 'SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

OUT = r'E:\生活\股票操练大全全套\stock-blog\source\images\kxian'
os.makedirs(OUT, exist_ok=True)

RED = '#FF4444'
GREEN = '#00AA00'

def draw_kline(ax, x, o, c, h, l, width=0.3):
    color = RED if c >= o else GREEN
    ax.plot([x, x], [l, h], color=color, linewidth=1.5)
    bottom = min(o, c)
    height = abs(c - o)
    if height < 0.01:
        height = 0.01
    rect = patches.Rectangle((x - width/2, bottom), width, height,
                              facecolor=color, edgecolor=color, linewidth=1)
    ax.add_patch(rect)

def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close(fig)
    print(f'Saved {name}')

def new_fig(w=4, h=3):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(-0.5, 5.5)
    ax.set_ylim(0, 10)
    ax.axis('off')
    return fig, ax

# v1o-54: 连续跳空三阳线 (3根跳空高开阳线)
fig, ax = new_fig(4, 3)
base = 2.0
for i in range(3):
    o = base + i*0.8
    c = o + 0.6
    h = c + 0.2
    l = o - 0.1
    draw_kline(ax, i+1, o, c, h, l)
save(fig, 'v1o-54.png')

# v1o-55: 连续跳空三阴线 (3根跳空低开阴线)
fig, ax = new_fig(4, 3)
base = 8.0
for i in range(3):
    o = base - i*0.8
    c = o - 0.6
    h = o + 0.1
    l = c - 0.2
    draw_kline(ax, i+1, o, c, h, l)
save(fig, 'v1o-55.png')

# v1o-56: 跳空上扬形 (跳空阳线+阴线不补缺口)
fig, ax = new_fig(4, 3)
draw_kline(ax, 1, 3, 3.5, 3.7, 2.8)  # 前一根
draw_kline(ax, 2, 4.0, 5.0, 5.2, 3.9)  # 跳空阳线
draw_kline(ax, 3, 4.8, 4.2, 4.9, 4.0)  # 阴线不补缺口
save(fig, 'v1o-56.png')

# v1o-57: 下档五阳线 (下跌后连续5根小阳线)
fig, ax = new_fig(4, 3)
draw_kline(ax, 1, 8, 7, 8.2, 6.8)  # 大阴线
for i in range(5):
    o = 4.5 + i*0.15
    c = o + 0.3
    h = c + 0.15
    l = o - 0.1
    draw_kline(ax, i+2, o, c, h, l)
save(fig, 'v1o-57.png')

# v1o-58: 高开出逃形 (高开大阴线)
fig, ax = new_fig(4, 3)
draw_kline(ax, 1, 5, 5.5, 5.7, 4.8)  # 前一根阳线
draw_kline(ax, 2, 7.0, 4.5, 7.2, 4.3)  # 高开低走大阴线
save(fig, 'v1o-58.png')

# v1o-59: 下探上涨形 (低开高走大阳线)
fig, ax = new_fig(4, 3)
draw_kline(ax, 1, 4, 4.5, 4.7, 3.8)  # 前一根
draw_kline(ax, 2, 3.0, 6.0, 6.2, 2.8)  # 低开高走大阳线
save(fig, 'v1o-59.png')

# v1o-60: 双飞乌鸦 (阳线后两根高开低走阴线)
fig, ax = new_fig(4, 3)
draw_kline(ax, 1, 3, 5, 5.2, 2.8)  # 大阳线
draw_kline(ax, 2, 5.5, 4.8, 5.7, 4.6)  # 第一根阴线
draw_kline(ax, 3, 5.3, 4.0, 5.5, 3.8)  # 第二根阴线吞没第一根
save(fig, 'v1o-60.png')

# v1o-61: 三只乌鸦 (高位连续3根阴线)
fig, ax = new_fig(4, 3)
draw_kline(ax, 1, 6, 5.2, 6.2, 5.0)
draw_kline(ax, 2, 5.0, 4.2, 5.2, 4.0)
draw_kline(ax, 3, 4.0, 3.2, 4.2, 3.0)
save(fig, 'v1o-61.png')

# v1o-62: 下跌三连阴 (连续3根大阴线)
fig, ax = new_fig(4, 3)
draw_kline(ax, 1, 8, 6.5, 8.2, 6.3)
draw_kline(ax, 2, 6.3, 4.8, 6.5, 4.6)
draw_kline(ax, 3, 4.6, 2.5, 4.8, 2.3)
save(fig, 'v1o-62.png')

# v1o-63: 下降覆盖线 (穿头破脚阴线+阳线+阴线深入阳线)
fig, ax = new_fig(4, 3)
draw_kline(ax, 1, 4, 6, 6.2, 3.8)  # 大阳线
draw_kline(ax, 2, 6.5, 3.5, 6.7, 3.3)  # 穿头破脚阴线
draw_kline(ax, 3, 3.8, 4.5, 4.7, 3.6)  # 小阳线
draw_kline(ax, 4, 4.8, 3.0, 5.0, 2.8)  # 阴线深入阳线
save(fig, 'v1o-63.png')

# v1o-64: 阳线跛脚形 (3根以上阳线，后两根低开且收盘更低)
fig, ax = new_fig(4, 3)
draw_kline(ax, 1, 2, 4, 4.2, 1.8)
draw_kline(ax, 2, 3.5, 5, 5.2, 3.3)
draw_kline(ax, 3, 4.2, 4.8, 5.0, 4.0)  # 低开但收盘低于前一根
save(fig, 'v1o-64.png')

# v1o-65: 倒三阳 (3根阳线但股价一天比一天低)
fig, ax = new_fig(4, 3)
draw_kline(ax, 1, 7, 8, 8.2, 6.8)
draw_kline(ax, 2, 6.5, 7.2, 7.4, 6.3)
draw_kline(ax, 3, 5.8, 6.5, 6.7, 5.6)
save(fig, 'v1o-65.png')

# v1o-66: 加速度线 (上涨时先慢后快)
fig, ax = new_fig(5, 3)
draw_kline(ax, 1, 2, 2.5, 2.6, 1.9)
draw_kline(ax, 2, 2.5, 3.0, 3.1, 2.4)
draw_kline(ax, 3, 3.0, 3.8, 3.9, 2.9)
draw_kline(ax, 4, 3.8, 5.2, 5.4, 3.7)
draw_kline(ax, 5, 5.2, 7.5, 7.8, 5.0)
save(fig, 'v1o-66.png')

# v1o-67: 弧形线 (底部逐渐抬高的抛物线)
fig, ax = new_fig(5, 3)
draw_kline(ax, 1, 3, 3.2, 3.4, 2.8)
draw_kline(ax, 2, 3.1, 3.5, 3.7, 2.9)
draw_kline(ax, 3, 3.4, 3.8, 4.0, 3.2)
draw_kline(ax, 4, 3.7, 4.5, 4.7, 3.5)
draw_kline(ax, 5, 4.3, 5.5, 5.8, 4.1)
save(fig, 'v1o-67.png')

# v1o-68: 镊子线 (三根K线最高价相同)
fig, ax = new_fig(4, 3)
draw_kline(ax, 1, 3, 5, 6, 2.8)  # 大阳线
draw_kline(ax, 2, 4.5, 5.2, 6, 4.3)  # 小K线最高价=6
draw_kline(ax, 3, 5.5, 3.5, 6, 3.3)  # 大阴线最高价=6
save(fig, 'v1o-68.png')

# v1o-69: 尽头线 (长上影线后小K线完全在上影线范围内)
fig, ax = new_fig(4, 3)
draw_kline(ax, 1, 3, 5, 7, 2.8)  # 长上影阳线
draw_kline(ax, 2, 5.5, 6.0, 6.5, 5.3)  # 小K线在上影线范围内
save(fig, 'v1o-69.png')

# v1o-70: 搓揉线 (T字线+倒T字线)
fig, ax = new_fig(4, 3)
draw_kline(ax, 1, 5, 5, 5.5, 3)  # T字线
draw_kline(ax, 2, 5, 5, 7, 4.5)  # 倒T字线
save(fig, 'v1o-70.png')

# v1o-71: 小阳线
fig, ax = new_fig(2, 2)
draw_kline(ax, 1, 4.5, 5.2, 5.5, 4.3)
save(fig, 'v1o-71.png')

# v1o-72: 小阴线
fig, ax = new_fig(2, 2)
draw_kline(ax, 1, 5.5, 4.8, 5.7, 4.6)
save(fig, 'v1o-72.png')

# v1o-73: 十字线
fig, ax = new_fig(2, 2)
draw_kline(ax, 1, 5, 5, 6.5, 3.5)
save(fig, 'v1o-73.png')

# v1o-74: 升势停顿 (3根阳线，第三根很短)
fig, ax = new_fig(4, 3)
draw_kline(ax, 1, 2, 4, 4.2, 1.8)
draw_kline(ax, 2, 4, 6, 6.2, 3.8)
draw_kline(ax, 3, 6, 6.3, 6.8, 5.8)
save(fig, 'v1o-74.png')

print('All done!')
