import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np

# ---------- 图 14.2 时间层的参数量 ----------
CH = "14"
chans = [320, 640, 1280]
attn = [4 * c * c / 1e6 for c in chans]
full = [12 * c * c / 1e6 for c in chans]

fig, ax = plt.subplots(figsize=(W_FULL * 0.62, 2.3))
x = np.arange(len(chans))
ax.bar(x - 0.19, attn, width=0.34, color=BLUE_L, label="仅注意力（$4C^2$）")
ax.bar(x + 0.19, full, width=0.34, color=BLUE, label="含前馈（$12C^2$）")
for i, (a, b) in enumerate(zip(attn, full)):
    ax.text(i - 0.19, a + 0.8, "%.1f" % a, ha="center", fontsize=7.2, color=INK)
    ax.text(i + 0.19, b + 0.8, "%.1f" % b, ha="center", fontsize=7.2, color=INK)
ax.set_xticks(x)
ax.set_xticklabels(["$C=320$", "$C=640$", "$C=1280$"])
ax.set_ylabel("单个时间层参数量（百万）")
ax.set_ylim(0, 24)
ax.legend(loc="upper left")
style(ax, grid=True)
ax.grid(axis="x", visible=False)
save(fig, "fig14_params", CH)

# ---------- 图 14.3 共享噪声的强度 ----------
CH = "14"
lam = np.linspace(0, 1, 201)
corr = 1 - lam
diff = lam

fig, ax = plt.subplots(figsize=(W_FULL * 0.78, 2.45))
ax.plot(lam, corr, color=BLUE, label="$1-\\lambda$：两帧噪声的相关系数")
ax.plot(lam, diff, color=RED, label="$\\lambda$：帧差方差（独立时为 1）")
ax.axvline(0.1, color=GRAY, lw=0.7, ls=(0, (4, 3)))
ax.text(0.125, 0.30, "$\\lambda=0.1$", fontsize=7.6, color=GRAY)
ax.set_xlabel("$\\lambda$")
ax.set_ylabel("归一化数值")
ax.set_xlim(0, 1)
ax.set_ylim(0, 1.05)
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.30), ncol=2, handlelength=1.6)
style(ax, grid=True)
save(fig, "fig14_lambda", CH)
