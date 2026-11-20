import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np

CH = "11"

rng = np.random.default_rng(3)
fig, ax = plt.subplots(figsize=(W_FULL, 2.45))
ax.set_xlim(-0.4, 9.6)
ax.set_ylim(0.0, 4.35)
ax.axis("off")


def frame_row(y0, eps_list, shared=False):
    for k in range(4):
        shade = 0.60 + 0.05 * np.tanh(eps_list[k])
        ax.add_patch(plt.Rectangle((k * 2.2, y0), 1.7, 1.0,
                                   fc=(shade, shade * 0.96, shade * 0.92), ec=LIGHT, lw=0.6))
        ax.add_patch(plt.Circle((k * 2.2 + 0.6 + 0.15 * k, y0 + 0.5), 0.12,
                                color=BLUE, alpha=0.85))
        ax.text(k * 2.2 + 0.85, y0 - 0.16, "帧 %d" % (k + 1), ha="center", fontsize=6.8, color=GRAY)


# 上：每帧独立
eps = [rng.normal(0, 1) for _ in range(4)]
frame_row(2.75, eps)
for k in range(4):
    ax.text(k * 2.2 + 0.85, 3.90, "$\\epsilon_%d$" % (k + 1), ha="center", fontsize=7.4, color=GRAY)

# 下：共享
e = rng.normal(0, 1)
frame_row(0.65, [e] * 4)
ax.plot([0.85, 7.45], [2.00, 2.00], color=GRAY, lw=0.8)
for k in range(4):
    ax.plot([k * 2.2 + 0.85, k * 2.2 + 0.85], [2.00, 1.68], color=GRAY, lw=0.8)
ax.text(3.65, 2.14, "$\\epsilon$（共享）", ha="center", fontsize=7.4, color=GRAY)

save(fig, "fig11_video_step", CH)
