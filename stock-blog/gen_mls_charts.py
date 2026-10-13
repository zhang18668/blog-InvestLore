# -*- coding: utf-8 -*-
"""《股票大作手回忆录》配套概念插图：同花顺风格 红涨绿跌"""
import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'FangSong', 'SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False
import matplotlib.pyplot as plt
import numpy as np
import os

OUT = r"E:\生活\股票操练大全全套\stock-blog\source\images\mls"
os.makedirs(OUT, exist_ok=True)

UP = '#FF4444'
DN = '#00AA00'
GRID = '#cfd8dc'
INK = '#37474f'

def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close(fig)
    print('saved', name)

def base_ax(ax, title):
    ax.set_facecolor('#fafafa')
    for s in ['top','right']:
        ax.spines[s].set_visible(False)
    for s in ['left','bottom']:
        ax.spines[s].set_color('#90a4ae')
    ax.tick_params(colors='#78909c', labelsize=8)
    ax.set_title(title, fontsize=12, color=INK, pad=10, fontweight='bold')

# 1. 最小阻力线：价格像河水一样顺着阻力最小的方向流动
fig, ax = plt.subplots(figsize=(6.2, 3.4))
base_ax(ax, '图1  最小阻力线：顺着河流的方向游，不要逆流')
x = np.linspace(0, 10, 200)
y = 2 + 0.75*x + 0.5*np.sin(x*1.3)
ax.plot(x, y, color=UP, lw=2.2)
# 阻力线（上升趋势线）
ax.plot([0,10],[2, 9.5], color=INK, lw=1.4, ls='--')
ax.annotate('最小阻力方向（上升趋势）', xy=(6.5, 7.2), xytext=(1.2, 8.6),
            fontsize=9, color=UP,
            arrowprops=dict(arrowstyle='->', color=UP, lw=1.3))
ax.annotate('逆势做多空气，\n迟早被趋势吞没', xy=(8, 4.2), xytext=(5.5, 2.4),
            fontsize=8.5, color=DN)
ax.set_xlim(0,10); ax.set_ylim(1,10); ax.set_xticks([]); ax.set_yticks([])
save(fig, 'mls-01-least-resistance.png')

# 2. 关键点（pivotal point）：在长期盘整后突破时才出手
fig, ax = plt.subplots(figsize=(6.2, 3.4))
base_ax(ax, '图2  关键点：横有多长，竖有多高，突破才动手')
x = np.arange(30)
base = np.concatenate([np.linspace(5,5,18), np.linspace(5,9.5,12)])
noise = np.array([0.15*np.random.randn() for _ in x])
y = base + noise
ax.plot(x, y, color=INK, lw=1.6)
ax.axhline(5.4, color=DN, ls='--', lw=1.2)
ax.text(0.2, 5.55, '关键点（颈线）', fontsize=8.5, color=DN)
ax.scatter([18],[y[18]], color=UP, s=45, zorder=5)
ax.annotate('突破关键点\n开始建仓', xy=(18,y[18]), xytext=(19.5,6.6),
            fontsize=9, color=UP, arrowprops=dict(arrowstyle='->', color=UP, lw=1.2))
ax.text(4, 4.3, '长期横盘蓄势\n此时不动手', fontsize=8.5, color='#78909c')
ax.set_xlim(-0.5,30); ax.set_ylim(3.5,10.5); ax.set_xticks([]); ax.set_yticks([])
save(fig, 'mls-02-pivot.png')

# 3. 金字塔加码：底仓最大，越涨越加得越少
fig, ax = plt.subplots(figsize=(5.6, 3.6))
base_ax(ax, '图3  金字塔式加码：首笔最大，顺势递减加码')
levels = ['第四次加码\n(最小)', '第三次加码', '第二次加码', '首次建仓\n(最大)']
widths = [0.5, 1.0, 1.6, 2.3]
colors = ['#ffcdd2', '#ef9a9a', '#e57373', UP]
for i,(lv,w,c) in enumerate(zip(levels,widths,colors)):
    ax.barh(i, w, height=0.7, left=(2.3-w)/2, color=c, edgecolor='white')
    ax.text(2.3/2, i, lv, ha='center', va='center', fontsize=8.5,
            color='white' if i>=2 else INK, fontweight='bold')
ax.set_xlim(0,2.3); ax.set_ylim(-0.6,3.6); ax.set_xticks([]); ax.set_yticks([])
ax.text(1.15, -0.35, '价格 → 越来越高，仓位 → 越来越轻', ha='center', fontsize=8.5, color='#78909c')
save(fig, 'mls-03-pyramid.png')

# 4. 耐心等待正确时机
fig, ax = plt.subplots(figsize=(6.2, 3.2))
base_ax(ax, '图4  钱是"坐"出来的，不是"做"出来的')
x = np.arange(25)
y = np.concatenate([np.linspace(5,5,15), np.linspace(5,8.8,10)])
ax.plot(x, y, color=INK, lw=1.8)
ax.axvspan(0,15, color='#fff3e0', alpha=0.6)
ax.text(7.5, 9.3, '大部分时间空仓等待\n（忍住手痒）', ha='center', fontsize=9, color='#e65100')
ax.scatter([15],[5], color=UP, s=50, zorder=5)
ax.annotate('正确的时刻出现\n重仓进场', xy=(15,5), xytext=(16.5,6.4),
            fontsize=9, color=UP, arrowprops=dict(arrowstyle='->', color=UP, lw=1.2))
ax.set_xlim(0,25); ax.set_ylim(3.5,10); ax.set_xticks([]); ax.set_yticks([])
save(fig, 'mls-04-waiting.png')

# 5. 听内幕消息
fig, ax = plt.subplots(figsize=(5.6, 3.2))
base_ax(ax, '图5  内幕消息：耳听为虚，听信即被套')
x = np.arange(18)
y = np.concatenate([np.linspace(5,6.2,8), np.linspace(6.2,3.2,10)])
ax.plot(x, y, color=DN, lw=2)
ax.scatter([8],[6.2], color=UP, s=55, zorder=5)
ax.annotate('"内幕消息"让你\n在山顶接盘', xy=(8,6.2), xytext=(1,7.6),
            fontsize=9, color=UP, arrowprops=dict(arrowstyle='->', color=UP, lw=1.2))
ax.text(11, 4.6, '买入即套\n越补越跌', fontsize=9, color=DN)
ax.set_xlim(0,18); ax.set_ylim(2,8.5); ax.set_xticks([]); ax.set_yticks([])
save(fig, 'mls-05-tip.png')

# 6. 止损纪律
fig, ax = plt.subplots(figsize=(6.2, 3.2))
base_ax(ax, '图6  第一笔交易就设好止损，错了立刻认赔')
x = np.arange(20)
y = np.concatenate([np.linspace(5,5.6,6), np.linspace(5.6,3.0,14)])
ax.plot(x, y, color=INK, lw=1.8)
ax.axhline(5.2, color=DN, ls='--', lw=1.3)
ax.text(0.2, 5.35, '止损线 -8%', fontsize=8.5, color=DN)
ax.scatter([6],[5.2], color=DN, s=55, zorder=5, marker='v')
ax.annotate('触发止损\n果断离场', xy=(6,5.2), xytext=(7.5,6.4),
            fontsize=9, color=DN, arrowprops=dict(arrowstyle='->', color=DN, lw=1.2))
ax.text(12, 3.6, '不肯割肉 →\n小亏拖成大亏', fontsize=9, color=UP)
ax.set_xlim(0,20); ax.set_ylim(2,7.5); ax.set_xticks([]); ax.set_yticks([])
save(fig, 'mls-06-stop.png')

# 7. 利弗莫尔操作流程
fig, ax = plt.subplots(figsize=(6.6, 2.6))
ax.axis('off')
steps = ['观察走势\n找规律', '等关键点\n不抢跑', '首笔试单\n对了再加', '金字塔加码\n让利润奔跑', '趋势反转\n落袋为安']
n = len(steps)
for i, s in enumerate(steps):
    x0 = i/n
    rect = plt.Rectangle((x0+0.005, 0.25), 1/n-0.02, 0.5,
                         facecolor=UP if i in (1,3) else '#90caf9',
                         edgecolor='white', transform=ax.transAxes)
    ax.add_patch(rect)
    ax.text(x0+1/(2*n), 0.5, s, ha='center', va='center',
            fontsize=8.6, color='white', transform=ax.transAxes, fontweight='bold')
ax.set_title('图7  利弗莫尔式操作闭环', fontsize=12, color=INK, pad=8, fontweight='bold')
save(fig, 'mls-07-system.png')

# 8. 不与大盘争论 / 市场永远是对的
fig, ax = plt.subplots(figsize=(6.2, 3.2))
base_ax(ax, '图8  不要和行情争论：市场从不错，错的是你的固执')
x = np.arange(20)
y = np.concatenate([np.linspace(6,6,6), np.linspace(6,3.6,14)])
ax.plot(x, y, color=DN, lw=2)
ax.annotate('"我只是顺市而行"', xy=(10,5), xytext=(3,7.2),
            fontsize=10, color=UP, fontweight='bold',
            arrowprops=dict(arrowstyle='->', color=UP, lw=1.3))
ax.text(11, 4.2, '下跌趋势中\n不猜底、不抄底', fontsize=9, color=DN)
ax.set_xlim(0,20); ax.set_ylim(2.5,8); ax.set_xticks([]); ax.set_yticks([])
save(fig, 'mls-08-no-argue.png')

print('ALL DONE')
