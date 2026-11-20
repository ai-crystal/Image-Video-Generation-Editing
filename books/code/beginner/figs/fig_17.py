import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np

CH = "17"

# 左：弯曲路径；右：直线路径。两条都从噪声（上）到数据（下），端点相同。
fig, axes = plt.subplots(1, 2, figsize=(W_FULL, 2.3), gridspec_kw=dict(wspace=0.25))

ax = axes[0]
t = np.linspace(0, 1, 300)
x = 0.55 * np.sin(2.2 * t) + 0.25 * np.sin(5.0 * t)
y = 1.0 - 1.8 * t
ax.plot(x + 0.9, y + 0.1, color=BLUE, lw=1.5)
for tt, dx in [(0.15, 0.05), (0.35, 0.02), (0.55, -0.02), (0.8, -0.05)]:
    i = int(tt * (len(t) - 1))
    ax.annotate("", xy=(x[i] + 0.9 + dx, y[i] + 0.1 - 0.09), xytext=(x[i] + 0.9, y[i] + 0.1),
                arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=0.9, mutation_scale=7))
ax.scatter([x[0] + 0.9], [y[0] + 0.1], s=30, c="#9a9a9a", zorder=4)
ax.scatter([x[-1] + 0.9], [y[-1] + 0.1], s=30, c=BLUE, zorder=4)
ax.text(x[0] + 1.0, y[0] + 0.05, "噪声", fontsize=8.4, color=GRAY)
ax.text(x[-1] + 1.0, y[-1] + 0.02, "数据", fontsize=8.4, color=BLUE)
ax.set_xlim(-1.3, 2.3)
ax.set_ylim(-1.1, 1.4)
ax.set_xticks([])
ax.set_yticks([])
ax.set_aspect("equal")
style(ax, spines=("top", "right", "left", "bottom"))
for s in ax.spines.values():
    s.set_color(LIGHT)

ax = axes[1]
ax.plot([0.0, 0.0], [1.0, -0.8], color=RED, lw=1.5)
ax.annotate("", xy=(0.0, 0.0), xytext=(0.0, 0.35),
            arrowprops=dict(arrowstyle="-|>", color=RED, lw=0.9, mutation_scale=7))
ax.scatter([0.0], [1.0], s=30, c="#9a9a9a", zorder=4)
ax.scatter([0.0], [-0.8], s=30, c=BLUE, zorder=4)
ax.text(0.12, 0.95, "噪声", fontsize=8.4, color=GRAY)
ax.text(0.12, -0.82, "数据", fontsize=8.4, color=BLUE)
ax.set_xlim(-1.3, 2.3)
ax.set_ylim(-1.1, 1.4)
ax.set_xticks([])
ax.set_yticks([])
ax.set_aspect("equal")
style(ax, spines=("top", "right", "left", "bottom"))
for s in ax.spines.values():
    s.set_color(LIGHT)

save(fig, "fig17_paths", CH)
