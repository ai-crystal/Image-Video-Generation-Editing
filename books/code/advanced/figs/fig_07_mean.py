import os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np

CH = "07"
a = 1.0
fig, axes = plt.subplots(1, 2, figsize=(W_FULL, 2.2),
                         gridspec_kw=dict(width_ratios=[1.0, 1.05], wspace=0.38))

ax = axes[0]
ax.vlines([-a, a], 0, 0.5, color=GRAY, lw=2.4)
ax.scatter([0], [0], marker="x", s=44, c=RED, lw=1.8, zorder=5)
ax.annotate("条件均值\n（此处概率为 0）", (0, 0.02), xytext=(0, 0.30), ha="center",
            va="bottom", fontsize=8.0, color=RED,
            arrowprops=dict(arrowstyle="-", color=RED, lw=0.6))
ax.text(-a, 0.55, "真实样本", fontsize=8.2, color=GRAY, ha="center")
ax.set_xlim(-1.75, 1.75)
ax.set_ylim(0, 0.72)
ax.set_xticks([-a, 0, a])
ax.set_xticklabels(["$-a$", "0", "$a$"])
ax.set_yticks([])
ax.set_xlabel("$x_0$")
ax.set_ylabel(r"条件概率 $p(x_0\mid x_1)$")
style(ax)

ax = axes[1]
f = np.linspace(-2, 2, 400)
ax.plot(f, f ** 2 + a ** 2, color=BLUE, lw=1.6)
ax.axhline(a ** 2, color=RED, ls=(0, (4, 3)), lw=0.9)
ax.scatter([0], [a ** 2], s=26, c=RED, zorder=5)
ax.annotate("不可约损失 $a^2$", (0, a ** 2), xytext=(0.42, 0.34),
            fontsize=8.2, color=RED,
            arrowprops=dict(arrowstyle="-", color=RED, lw=0.6))
ax.scatter([-a, a], [2 * a ** 2, 2 * a ** 2], s=20, c=GRAY, zorder=4)
ax.text(a - 0.05, 2 * a ** 2 + 0.12, "预测真实值反而更差", fontsize=8.0, color=GRAY, ha="right")
ax.set_xlim(-2, 2)
ax.set_ylim(0, 4.6)
ax.set_xticks([-2, -1, 0, 1, 2])
ax.set_xlabel("预测值 $f(x_1)$")
ax.set_ylabel("平均平方损失")
style(ax, grid=True)

save(fig, "fig07_mean", CH)
