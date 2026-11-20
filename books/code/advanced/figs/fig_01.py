import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np

CH = "01"

# 左：条件直线交叉；右：边际轨迹弯曲（二维）
fig, axes = plt.subplots(1, 2, figsize=(W_FULL, 2.25), gridspec_kw=dict(wspace=0.25))

ax = axes[0]
pairs = [((-1.0, -0.55), (0.75, 1.0)), ((-1.0, 0.55), (0.75, -1.0)),
         ((1.0, -0.55), (-0.75, 1.0)), ((1.0, 0.55), (-0.75, -1.0))]
for (a, b) in pairs:
    ax.plot([a[0], b[0]], [a[1], b[1]], color=BLUE_L, lw=1.0, alpha=0.95)
    ax.scatter(*a, s=18, c=BLUE, zorder=4)
    ax.scatter(*b, s=18, c="#b9b9b6", zorder=4)
ax.set_xlim(-1.6, 1.6)
ax.set_ylim(-1.45, 1.45)
ax.set_xticks([])
ax.set_yticks([])
ax.set_aspect("equal")
ax.text(-1.5, 1.22, "起点：数据", fontsize=8.2, color=BLUE)
ax.text(0.75, 1.22, "终点：噪声", fontsize=8.2, color=GRAY)

ax = axes[1]
t = np.linspace(0, 1, 200)
bx = 0.85 * np.cos(np.pi * t + 0.25) * (1 - 0.5 * t)
by = 1.0 * np.sin(np.pi * t + 0.25) * (1 - 0.5 * t)
ax.plot(bx, by, color=RED, lw=1.5)
for tt in np.linspace(0.08, 0.92, 8):
    i = int(tt * (len(t) - 1))
    ax.annotate("", xy=(bx[i] + 0.1, by[i] + 0.09), xytext=(bx[i], by[i]),
                arrowprops=dict(arrowstyle="-|>", color=RED, lw=0.8, mutation_scale=7))
ax.set_xlim(-1.6, 1.6)
ax.set_ylim(-1.45, 1.45)
ax.set_xticks([])
ax.set_yticks([])
ax.set_aspect("equal")
ax.text(-1.5, 1.22, "边际速度的方向", fontsize=8.2, color=RED)
save(fig, "fig01_paths", CH)
