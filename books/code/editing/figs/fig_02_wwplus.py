import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np
from matplotlib.patches import Rectangle

# ---------- 图 2.3  W 与 W+ 的逐层注入 ----------
CH = "02"

# 18 个风格层：4^2 .. 1024^2，每个分辨率两层
res = [4, 4, 8, 8, 16, 16, 32, 32, 64, 64, 128, 128, 256, 256, 512, 512, 1024, 1024]
L = len(res)

fig, ax = plt.subplots(figsize=(W_FULL, 2.35))
ax.set_xlim(-0.15, L + 0.15)
ax.set_ylim(-1.95, 2.30)
ax.axis("off")

bw, bh = 0.78, 0.28
y_w = 1.30
y_wp = -0.62


def row(y0, colors):
    for i, c in enumerate(colors):
        ax.add_patch(Rectangle((i + 0.11, y0), bw, bh, facecolor=c, edgecolor="#4a4a4a", lw=0.5))


# W：一个 w 广播到全部层，颜色全同
row(y_w, [BLUE_L] * L)
ax.text(-0.10, y_w + bh + 0.14, "$W$：同一个 $w$ 送进全部 18 层", fontsize=8.0, color=INK, va="bottom")

# W+：每层一个 w_i，深浅示意取值不同
rng = np.random.default_rng(7)
vals = []
for _ in range(L):
    c = 0.30 + 0.55 * rng.random()
    rgb = np.array([0.18, 0.36, 0.54]) * c + (1 - c) * np.array([0.97, 0.97, 0.96])
    vals.append(tuple(rgb))
row(y_wp, vals)
ax.text(-0.10, y_wp + bh + 0.14, "$W^+$：每层各有自己的 $w_i$", fontsize=8.0, color=INK, va="bottom")

for i in (0, 8, 17):
    ax.text(i + 0.11 + bw / 2, y_wp - 0.09, "$w_{%d}$" % (i + 1), fontsize=6.9,
            ha="center", va="top", color=GRAY)

# 中间的分辨率刻度
ymid = 0.36
ax.plot([0.30, L - 0.09], [ymid, ymid], color=LIGHT, lw=0.8, zorder=0)
for i, r in enumerate(res):
    if res.index(r) == i:
        x = i + 0.11
        ax.plot([x, x], [ymid - 0.07, ymid + 0.07], color=GRAY, lw=0.6)
        ax.text(x + 0.89, ymid, "$%d^2$" % r, fontsize=6.8, ha="center", va="center",
                color=GRAY, bbox=dict(boxstyle="round,pad=0.10", fc="white", ec="none"))

# 底部两条尺度说明
ax.annotate("", xy=(6.4, -1.22), xytext=(0.30, -1.22),
            arrowprops=dict(arrowstyle="-|>", color=SAND, lw=0.9, mutation_scale=7))
ax.text(0.30, -1.34, "粗尺度层：姿态、脸型、整体布局", fontsize=7.2, ha="left", va="top", color=SAND)

ax.annotate("", xy=(17.7, -1.22), xytext=(11.4, -1.22),
            arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=0.9, mutation_scale=7))
ax.text(17.7, -1.34, "细尺度层：纹理、光照、局部颜色", fontsize=7.2, ha="right", va="top", color=GREEN)

save(fig, "fig02_wwplus", CH)
