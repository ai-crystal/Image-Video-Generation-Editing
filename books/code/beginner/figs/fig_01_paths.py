import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np

CH = "01"

rng = np.random.default_rng(5)

# 数据流形：右侧一段弧
tt = np.linspace(-0.62, 0.62, 120)
curve = np.stack([0.84 + 0.045 * np.sin(3.2 * tt), 0.50 + 0.27 * tt], 1)

# 噪声团：左侧一团点
blob = np.stack([0.13 + 0.050 * rng.normal(size=90), 0.50 + 0.095 * rng.normal(size=90)], 1)
blob[:, 1] = np.clip(blob[:, 1], 0.18, 0.82)

fig, axes = plt.subplots(1, 4, figsize=(W_FULL, 1.62))
fig.subplots_adjust(wspace=0.10)

titles = ["一次映射", "多步去噪", "连续流", "一步生成"]
subs = ["变分自编码器、对抗网络", "扩散模型", "流模型", "蒸馏、一致性模型"]

for ax in axes:
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_aspect("equal")
    style(ax, spines=("top", "right", "left", "bottom"))
    for s in ax.spines.values():
        s.set_color(LIGHT)
    ax.plot(curve[:, 0], curve[:, 1], color=BLUE, lw=2.2, solid_capstyle="round", zorder=2)
    ax.scatter(blob[:, 0], blob[:, 1], s=1.9, c=GRAY, alpha=0.40, lw=0, zorder=1)

start = np.array([0.15, 0.50])

# (a) 一步映射：一条粗箭头
ax = axes[0]
ax.annotate("", xy=(0.775, 0.615), xytext=start,
            arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.5,
                            connectionstyle="arc3,rad=-0.16"))

# (b) 多步去噪：折线，每段一个箭头
ax = axes[1]
path = np.array([[0.17, 0.50], [0.27, 0.56], [0.36, 0.45], [0.45, 0.51],
                 [0.55, 0.42], [0.64, 0.47], [0.72, 0.41], [0.775, 0.43]])
for i in range(len(path) - 1):
    ax.annotate("", xy=path[i + 1], xytext=path[i],
                arrowprops=dict(arrowstyle="-|>", color=RED, lw=0.9,
                                shrinkA=1.0, shrinkB=1.0))
ax.scatter(path[1:-1, 0], path[1:-1, 1], s=4, c=RED, lw=0, zorder=3)

# (c) 连续流：一族轨迹，各自指向流形上不同的点
ax = axes[2]
for target in [(0.79, 0.68), (0.79, 0.50), (0.79, 0.32)]:
    ax.annotate("", xy=target, xytext=start,
                arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.0,
                                connectionstyle="arc3,rad=0.22",
                                shrinkA=2.0, shrinkB=1.0))

# (d) 一步生成：原来那条折线退成虚线，剩下两段
ax = axes[3]
fine = np.array([[0.17, 0.50], [0.28, 0.57], [0.38, 0.45], [0.48, 0.52],
                 [0.58, 0.43], [0.68, 0.46], [0.775, 0.43]])
ax.plot(fine[:, 0], fine[:, 1] - 0.10, color=GRAY, lw=1.0, alpha=0.60, ls=(0, (2.2, 2.0)))
ax.annotate("", xy=(0.52, 0.50), xytext=(0.17, 0.50),
            arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.4))
ax.annotate("", xy=(0.785, 0.44), xytext=(0.52, 0.50),
            arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.4))

axes[0].text(0.12, 0.86, "噪声", color=GRAY, fontsize=7.4, ha="center")
axes[0].text(0.84, 0.14, "数据", color=BLUE, fontsize=7.4, ha="center")

for ax, t, s in zip(axes, titles, subs):
    ax.set_xlabel(t + "\n" + s, fontsize=7.8, color=INK, labelpad=3)
    ax.xaxis.label.set_linespacing(1.6)

save(fig, "fig01_paths", CH)
