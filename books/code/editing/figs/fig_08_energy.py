import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np

# 端点固定的一维位移: x(t) = D t + A (1 - cos 2 pi t) / (2 pi)
# 速度 = D + A sin(2 pi t)，动能为 D^2 + A^2/2（交叉项积分为零）
CH = "08"

D = 1.0
fig, axes = plt.subplots(1, 2, figsize=(W_FULL, 2.25), gridspec_kw=dict(wspace=0.32))

# ---------------- 左：直线与摆动 ----------------
ax = axes[0]
t = np.linspace(0, 1, 400)
ax.plot(t, D * t, color=BLUE, lw=1.6, label="$A=0$：直线")
for A, c in [(1.2, SAND), (2.0, RED)]:
    x = D * t + A * (1 - np.cos(2 * np.pi * t)) / (2 * np.pi)
    ax.plot(t, x, color=c, lw=1.4, label="$A=%g$" % A)
    for tt in (0.125, 0.375, 0.625, 0.875):
        xx = D * tt + A * (1 - np.cos(2 * np.pi * tt)) / (2 * np.pi)
        vv = D + A * np.sin(2 * np.pi * tt)
        ax.annotate("", xy=(tt + 0.075, xx + 0.075 * vv), xytext=(tt, xx),
                    arrowprops=dict(arrowstyle="-|>", color=c, lw=0.7, mutation_scale=6))
ax.scatter([0, 1], [0, D], s=22, color=INK, zorder=6)
ax.set_xlabel("$t$")
ax.set_ylabel("这条维度上的位移")
ax.set_xlim(-0.03, 1.05)
ax.set_ylim(-0.05, 1.75)
ax.legend(loc="upper left", fontsize=7.4, handletextpad=0.4)
style(ax, spines=("top", "right"))

# ---------------- 右：动能随摆动幅值 ----------------
ax = axes[1]
A = np.linspace(0, 2.2, 400)
E = D ** 2 + A ** 2 / 2.0
ax.plot(A, E, color=BLUE, lw=1.6)
ax.axhline(D ** 2, color=GRAY, lw=0.8, ls=(0, (4, 3)))
ax.text(0.30, D ** 2 - 0.20, "直线：$D^2$", fontsize=7.2, color=GRAY)
for a0 in (1.2, 2.0):
    ax.scatter([a0], [D ** 2 + a0 ** 2 / 2], s=20, color=RED, zorder=5)
ax.annotate("$A=1$ 时多出 50%", xy=(1.02, 1.52), xytext=(0.12, 2.55), fontsize=7.2, color=RED,
            arrowprops=dict(arrowstyle="-|>", color=RED, lw=0.6, mutation_scale=6))
ax.set_xlabel("摆动幅值 $A$")
ax.set_ylabel("动能 $E(u)$")
ax.set_xlim(0, 2.2)
ax.set_ylim(0.6, 3.7)
style(ax, spines=("top", "right"))

save(fig, "fig08_energy", CH)
