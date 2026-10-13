# -*- coding: utf-8 -*-
"""补充：小阳线、小阴线、高档五阴线"""
import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'FangSong', 'SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

OUT = r"E:\生活\股票操练大全全套\stock-blog\source\images\kxian"
UP = '#FF4444'
DN = '#00AA00'

def draw_kline(ax, x, o, c, h, l, width=0.35):
    color = UP if c >= o else DN
    ax.plot([x, x], [l, h], color=color, linewidth=1.5)
    bottom = min(o, c)
    height = max(abs(c - o), 0.05)
    rect = patches.Rectangle((x - width/2, bottom), width, height,
                            facecolor=color, edgecolor=color, linewidth=1)
    ax.add_patch(rect)

# v1o-51 小阳线
fig, ax = plt.subplots(figsize=(3, 3))
draw_kline(ax, 1, 10, 10.3, 10.5, 9.8)
ax.set_xlim(0, 2); ax.set_ylim(9.5, 11); ax.axis('off')
fig.savefig(os.path.join(OUT, 'v1o-51.png'), dpi=150, bbox_inches='tight', facecolor='white')
plt.close(); print("saved v1o-51")

# v1o-52 小阴线
fig, ax = plt.subplots(figsize=(3, 3))
draw_kline(ax, 1, 10, 9.7, 10.2, 9.5)
ax.set_xlim(0, 2); ax.set_ylim(9, 10.5); ax.axis('off')
fig.savefig(os.path.join(OUT, 'v1o-52.png'), dpi=150, bbox_inches='tight', facecolor='white')
plt.close(); print("saved v1o-52")

# v1o-53 高档五阴线
fig, ax = plt.subplots(figsize=(4, 3))
draw_kline(ax, 1, 8, 11, 11.5, 7.8)  # 前期大阳线
for i in range(5):
    draw_kline(ax, i+2, 11-i*0.1, 10.5-i*0.15, 11.2-i*0.1, 10.3-i*0.12)
ax.set_xlim(0, 8); ax.set_ylim(7, 12); ax.axis('off')
fig.savefig(os.path.join(OUT, 'v1o-53.png'), dpi=150, bbox_inches='tight', facecolor='white')
plt.close(); print("saved v1o-53")
