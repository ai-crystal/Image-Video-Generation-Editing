import os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np

CH = "08"
fig, ax = plt.subplots(figsize=(W_FULL * 0.86, 1.95))
ax.set_xlim(-0.26, 1.06)
ax.set_ylim(-0.35, 2.85)
ax.axis("off")

# 教师：20 段
ts = np.linspace(1, 0, 21)
y1 = 2.15
ax.plot([0, 1], [y1, y1], color=LIGHT, lw=1.2, zorder=1)
ax.scatter(ts, np.full_like(ts, y1), s=14, c=GRAY, zorder=3)
ax.text(-0.03, y1, "教师", fontsize=8.4, color=GRAY, ha="right", va="center")
ax.text(1.06, y1, "20 次前向", fontsize=8.0, color=GRAY, ha="left", va="center")

# 学生：跳 5 步，4 段
k = 5
pts = np.linspace(1, 0, 21 // k + 1)
y2 = 0.55
ax.plot([0, 1], [y2, y2], color=LIGHT, lw=1.2, zorder=1)
ax.scatter(pts, np.full_like(pts, y2), s=30, c=BLUE, zorder=4)
ax.text(-0.03, y2, "学生", fontsize=8.4, color=BLUE, ha="right", va="center")
ax.text(1.06, y2, "4 次前向", fontsize=8.0, color=BLUE, ha="left", va="center")

for i in range(len(pts) - 1):
    p, q = pts[i], pts[i + 1]
    ax.annotate("", xy=(q, y2), xytext=(p, y2),
                arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=1.0,
                                connectionstyle="arc3,rad=-0.55",
                                shrinkA=3, shrinkB=4))
    ax.text(0.5 * (p + q), y2 + 0.52, "跳 5 步", fontsize=7.6, color=BLUE, ha="center")

ax.text(1.0, 2.55, "噪声端 $t=1$", fontsize=8.0, color=INK, ha="center")
ax.text(0.0, 2.55, "数据端 $t=0$", fontsize=8.0, color=INK, ha="center")
ax.annotate("", xy=(0.10, 1.52), xytext=(0.90, 1.52),
            arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=0.7, ls=(0, (3, 2))))
ax.text(0.5, 1.60, "采样方向", fontsize=7.8, color=GRAY, ha="center")

save(fig, "fig08_skip", CH)
