import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np

CH = "15"

# 时间感受野：每层核长 3，感受野按 1+2d 扩张
T = 36
target = 18  # 被解码的帧
depths = 9  # 输入 + 8 层

fig, axes = plt.subplots(1, 2, figsize=(W_FULL, 2.85), gridspec_kw=dict(wspace=0.12))


def draw(ax, causal, ylabels):
    for d in range(depths):
        lo = max(1, target - 2 * d)
        hi = target + 2 * d if not causal else target
        hi = min(T, hi)
        ax.add_patch(plt.Rectangle((lo - 0.34, d - 0.15), (hi - lo) + 0.68, 0.3,
                                   fc=BLUE, alpha=0.16, ec="none"))
        ax.plot([lo - 0.34, hi + 0.34], [d, d], color=BLUE, lw=0.8, alpha=0.6)
    ax.plot([target, target], [-0.55, depths - 0.55], color=RED, lw=0.9, ls=(0, (4, 2)), zorder=0)
    ax.set_xlim(0.4, T + 0.6)
    ax.set_ylim(-1.35, depths + 0.45)
    ax.set_yticks(range(depths))
    ax.set_yticklabels(ylabels, fontsize=6.6)
    ax.set_xticks([2, 10, 18, 26, 34])
    ax.set_xlabel("帧序号")
    style(ax, spines=("top", "right"))


draw(axes[0], causal=False, ylabels=["输入"] + ["第 %d 层" % i for i in range(1, depths)])
axes[0].text(target + 0.4, depths - 0.15, "被解码帧", fontsize=7.0, color=RED)
axes[0].text((1 + T) / 2, -1.05, "非因果：前后各看 8 帧", fontsize=7.6, color=GRAY, ha="center")

draw(axes[1], causal=True, ylabels=[""] * depths)
axes[1].text(target + 0.4, depths - 0.15, "被解码帧", fontsize=7.0, color=RED)
axes[1].text((1 + T) / 2, -1.05, "因果：只看过去 16 帧", fontsize=7.6, color=GRAY, ha="center")
save(fig, "fig15_causal", CH)
