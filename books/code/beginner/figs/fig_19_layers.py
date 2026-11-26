import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np

CH = "19"

rows = [
    ("输入层", "硬替换像素或潜变量", "接缝、光照不一致"),
    ("时间步", "从某个 $t_0$ 重新去噪", "没有定位，全图都变"),
    ("注意力", "替换键值投影", "依赖注意力图的精度"),
    ("结构条件", "注入边缘、深度、姿态", "要额外的条件图或训练"),
    ("采样路径", "共享噪声、控制项、平滑", "要精确反演或额外求解"),
]

fig, ax = plt.subplots(figsize=(W_FULL, 2.55))
ax.set_xlim(0, 10.4)
ax.set_ylim(0, 6.1)
ax.axis("off")

ax.text(0.10, 5.72, "介入的层", fontsize=7.6, color=GRAY)
ax.text(2.75, 5.72, "保住结构靠什么", fontsize=7.6, color=GRAY)
ax.text(7.75, 5.72, "代价", fontsize=7.6, color=GRAY)
ax.plot([0.10, 10.2], [5.52, 5.52], color=GRAY, lw=0.7)

centers = [4.85, 3.95, 3.05, 2.15, 1.25]
for i, (lay, how, cost) in enumerate(rows):
    y = centers[i]
    ax.add_patch(plt.Rectangle((0.10, y - 0.30), 1.85, 0.60, fc="#eef2f6", ec="none"))
    ax.text(0.22, y, lay, fontsize=7.8, color=BLUE, va="center", ha="left")
    ax.text(2.75, y, how, fontsize=7.6, color=INK, va="center", ha="left")
    ax.text(7.75, y, cost, fontsize=7.4, color=GRAY, va="center", ha="left")
    if i < len(rows) - 1:
        ax.plot([0.10, 10.2], [y - 0.45, y - 0.45], color=LIGHT, lw=0.7)

ax.text(0.10, 0.55, "自上而下，介入点越来越深", fontsize=7.2, color=BLUE_L)

save(fig, "fig19_layers", CH)
