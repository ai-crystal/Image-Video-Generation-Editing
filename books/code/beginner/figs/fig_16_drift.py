import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np

CH = "16"

# 偏差递推 d_{k+1} = rho*d_k + eps 的闭式解
k = np.arange(1, 21)


def dev(rho, eps=1.0):
    return eps * (1 - rho ** k) / (1 - rho)


loose = dev(0.98)
anchor = dev(0.70)
scale = loose[-1]
loose, anchor = loose / scale, anchor / scale

fig, ax = plt.subplots(figsize=(W_FULL * 0.9, 2.35))
ax.plot(k, loose, color=BLUE, lw=1.6, label="只给上一块末帧（$\\rho=0.98$）")
ax.plot(k, anchor, color=GREEN, lw=1.6, label="首帧常驻锚定（$\\rho=0.70$）")
ax.axhline(anchor[-1], color=GREEN, lw=0.8, ls=(0, (3, 3)), alpha=0.7)
ax.annotate("", xy=(13.5, anchor[-1] + 0.03), xytext=(13.5, anchor[-1] - 0.16),
            arrowprops=dict(arrowstyle="-", color=GREEN, lw=0.7, ls=(0, (2, 2))))
ax.text(13.8, anchor[-1] - 0.10, "收敛到 $\\epsilon/(1-\\rho)$", fontsize=7.2, color=GREEN)
ax.set_xlabel("块序号")
ax.set_ylabel("偏离首帧")
ax.set_xticks([1, 5, 10, 15, 20])
ax.set_xlim(0.5, 20.5)
ax.set_ylim(0, 1.12)
ax.legend(loc="upper left", handlelength=1.6, borderaxespad=0.3)
style(ax, grid=True, spines=("top", "right"))
save(fig, "fig16_drift", CH)
