import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np

# ---------- 图 7.1 一个噪声点对应两个结果 ----------
CH = "07"
fig, ax = plt.subplots(figsize=(W_FULL * 0.8, 2.15))
z = np.array([-2.2, 0.0])
ends = [np.array([1.1, 0.75]), np.array([1.1, -0.75])]
for e, c in zip(ends, [BLUE, GREEN]):
    ax.annotate("", xy=e, xytext=z, arrowprops=dict(arrowstyle="-|>", color=c, lw=1.1,
                                                    connectionstyle="arc3,rad=0.25"))
    ax.scatter(*e, s=24, c=c, zorder=4)
ax.scatter(*z, s=28, c="#9a9a9a", zorder=4)
ax.text(z[0] - 0.1, z[1] - 0.3, "一个噪声点", fontsize=8.2, color=GRAY)
mid = 0.5 * (ends[0] + ends[1])
ax.scatter(*mid, s=32, c=RED, marker="x", lw=1.6, zorder=5)
ax.annotate("一步回归落在均值", mid, xytext=(mid[0] - 0.2, mid[1] - 0.55), fontsize=8.2,
            color=RED, ha="center", arrowprops=dict(arrowstyle="-", color=RED, lw=0.6))
ax.text(0.35, 1.25, "两条都合理的轨迹", fontsize=8.2, color=GRAY)
ax.set_xlim(-2.8, 2.2)
ax.set_ylim(-1.7, 1.7)
ax.set_aspect("equal")
ax.set_xticks([])
ax.set_yticks([])
style(ax, spines=("top", "right", "left", "bottom"))
for s in ax.spines.values():
    s.set_color(LIGHT)
save(fig, "fig07_blur", CH)

# ---------- 图 8.1 一致性约束 ----------
CH = "08"
fig, ax = plt.subplots(figsize=(W_FULL * 0.86, 2.25))
ax.set_xlim(0, 10)
ax.set_ylim(0, 5.2)
ax.axis("off")

t = np.linspace(0, 1, 200)
x = 1.0 + 3.2 * t
y = 1.2 + 2.2 * t + 0.5 * np.sin(3.2 * t)
ax.plot(x, y, color=BLUE, lw=1.6)
for tt in [0.15, 0.4, 0.65, 0.9]:
    i = int(tt * (len(t) - 1))
    ax.scatter(x[i], y[i], s=26, c=BLUE, zorder=4)
    ax.annotate("", xy=(8.6, 1.3), xytext=(x[i] + 0.1, y[i]),
                arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=0.8,
                                connectionstyle="arc3,rad=-0.15", ls=(0, (3, 2))))
ax.scatter(8.75, 1.3, s=60, c=RED, marker="*", zorder=5)
ax.text(8.55, 0.9, "同一个终点", fontsize=8.2, color=RED, ha="center")
ax.text(1.0, 0.45, "轨迹上的不同时刻", fontsize=8.2, color=BLUE)
ax.text(4.9, 4.55, "网络对它们的预测必须相同", fontsize=8.2, color=GRAY)
save(fig, "fig08_cm", CH)
