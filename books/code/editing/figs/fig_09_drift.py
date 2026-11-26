import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np
from matplotlib.lines import Line2D

# ---------- 图 9.3 传播误差的三种走势 ----------
CH = "09"
rng = np.random.default_rng(3)
K = 64
TRIALS = 4000
B = 0.18            # 每步的系统偏差，以单步随机误差的标准差为单位


def walk(anchor=None, bias=0.0):
    """累积误差的均方根；anchor 不为空时每 anchor 帧清零（关键帧重新对齐）。"""
    e = np.zeros(TRIALS)
    out = np.empty(K)
    for k in range(K):
        if anchor is not None and k > 0 and k % anchor == 0:
            e = np.zeros(TRIALS)
        e = e + rng.normal(size=TRIALS) + bias
        out[k] = np.sqrt(np.mean(e ** 2))
    return out


k = np.arange(1, K + 1)
fig, ax = plt.subplots(figsize=(W_HALF + 0.6, 2.4))

ax.axhline(2, color=SAND, lw=0.9, ls=(0, (4, 3)), zorder=0)
ax.plot(k, walk(), color=BLUE, lw=1.3)
ax.plot(k, walk(bias=B), color=RED, lw=1.3)
ax.plot(k, walk(anchor=8), color=GREEN, lw=1.3)

ax.set_xlabel("传播帧数 $k$")
ax.set_ylabel("累积误差（单步 $\\sigma$ 为单位）")
ax.set_xlim(1, K)
ax.set_ylim(0, 15.5)
ax.set_yticks([0, 5, 10, 15])

handles = [
    Line2D([], [], color=BLUE, lw=1.3, label=r"独立误差 $\sqrt{k}$"),
    Line2D([], [], color=RED, lw=1.3, label=r"每步带偏差 $b=0.18$"),
    Line2D([], [], color=GREEN, lw=1.3, label="每 8 帧锚定"),
    Line2D([], [], color=SAND, lw=0.9, ls=(0, (4, 3)), label="可见阈"),
]
ax.legend(handles=handles, loc="upper left", handlelength=1.6, labelspacing=0.28)
style(ax, grid=True)

save(fig, "fig09_drift", CH)
