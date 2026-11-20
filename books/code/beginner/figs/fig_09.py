import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np
from matplotlib.patches import FancyBboxPatch

CH = "09"

# ---------- 图 8.1 U-Net 结构 ----------
fig, ax = plt.subplots(figsize=(W_FULL, 2.15))
ax.set_xlim(0, 11.2)
ax.set_ylim(1.2, 5.6)
ax.axis("off")

boxes = [(1.3, 3.0, "64×64"), (3.3, 2.55, "32×32"), (5.2, 2.1, "16×16"),
         (7.1, 2.55, "32×32"), (8.9, 3.0, "64×64")]
w, h = 1.35, 0.62
for x, y, lab in boxes:
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.06",
                                fc="#e8eff6", ec=BLUE, lw=0.9))
    ax.text(x + w / 2, y + h / 2, lab, ha="center", va="center", fontsize=7.4, color=INK)

ax.annotate("", xy=(3.25, 2.86), xytext=(2.68, 3.28),
            arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=0.9))
ax.annotate("", xy=(5.15, 2.41), xytext=(4.68, 2.83),
            arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=0.9))
ax.annotate("", xy=(7.05, 2.83), xytext=(6.58, 2.41),
            arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=0.9))
ax.annotate("", xy=(8.85, 3.28), xytext=(8.48, 2.86),
            arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=0.9))

for i in range(3):
    x1 = boxes[i][0] + w / 2
    x2 = boxes[4 - i][0] + w / 2
    y1 = boxes[i][1] + h + 0.05
    y2 = boxes[4 - i][1] + h + 0.05
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color=SAND, lw=0.8,
                                connectionstyle="arc3,rad=-0.18", ls=(0, (3, 2))))

ax.text(5.55, 5.32, "虚线为跳跃连接", color=SAND, fontsize=7.4, ha="center")
ax.text(1.95, 3.78, "输入 $x_t$", fontsize=7.4, ha="center", color=INK)
ax.text(9.55, 3.78, "输出 $\\hat\\epsilon$", fontsize=7.4, ha="center", color=INK)
ax.text(5.88, 1.72, "自注意力", fontsize=7.4, color=GRAY, ha="center")
save(fig, "fig09_unet", CH)

# ---------- 图 8.2 EDM 预条件系数 ----------
sg = np.logspace(-2, 2.3, 400)
sd = 0.5
cs = sd ** 2 / (sg ** 2 + sd ** 2)
co = sg * sd / np.sqrt(sg ** 2 + sd ** 2)
ci = 1 / np.sqrt(sg ** 2 + sd ** 2)

fig, ax = plt.subplots(figsize=(W_FULL * 0.8, 2.2))
ax.loglog(sg, cs, color=BLUE, lw=1.4, label="$c_{\\mathrm{skip}}$")
ax.loglog(sg, co, color=RED, lw=1.4, label="$c_{\\mathrm{out}}$")
ax.loglog(sg, ci, color=GREEN, lw=1.4, label="$c_{\\mathrm{in}}$")
ax.set_xlabel("$\\sigma$")
ax.set_ylabel("系数")
ax.legend(loc="lower left", fontsize=8.0)
ax.grid(True, which="both", color=LIGHT, lw=0.5, alpha=0.7)
ax.set_axisbelow(True)
style(ax, spines=("top", "right"))
save(fig, "fig09_edm", CH)
