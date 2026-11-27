import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np

CH = "11"


def tri_pos(tau, D, vp):
    """线性加速到 vp 再线性减速回零的位置；tau 与 D 同单位。"""
    tau = np.asarray(tau, dtype=float)
    half = D / 2.0
    acc = vp * tau ** 2 / D
    dec = vp * D / 2.0 - vp * (D - tau) ** 2 / D
    return np.where(tau <= half, acc, dec)


fig, axes = plt.subplots(1, 2, figsize=(W_FULL, 2.75), gridspec_kw={"width_ratios": [1.25, 1.0]})

# 左：真实轨迹与一步给出的直线
ax = axes[0]
D, vp = 1.0, 1.0
tau = np.linspace(0, D, 400)
S = vp * D / 2.0
ax.plot(tau / D, tri_pos(tau, D, vp) / S, color=BLUE, lw=1.7, label="真实轨迹")
ax.plot(tau / D, tau / D, color=RED, lw=1.5, ls="--", label="一步：平均速度的直线")

# 在 tau = D/4 处标出偏差
tq = D / 4.0
xq = float(tri_pos(tq, D, vp)) / S
ax.plot([tq / D, tq / D], [xq, 0.25], color=GRAY, lw=0.7, ls=":")
tq4, lq = D / 4.0, 0.25
ax.annotate("", xy=(tq / D, xq), xytext=(tq / D, lq),
            arrowprops=dict(arrowstyle="<->", color=GRAY, lw=0.8))
ax.text(0.31, 0.045, "$\\tau=\\Delta/4$ 处偏差 $S/8$", fontsize=7.8, color=GRAY,
        ha="left", va="center")
ax.plot([tq / D], [xq], "o", color=BLUE, ms=3.5)
ax.set_xlabel("片段内时间 $\\tau/\\Delta$")
ax.set_ylabel("位移（以总位移 $S$ 为单位）")
ax.set_xlim(0, 1)
ax.set_ylim(0, 1.06)
ax.set_xticks([0, 0.25, 0.5, 0.75, 1])
ax.set_yticks([0, 0.5, 1])
style(ax, grid=True)
ax.legend(loc="upper left", handlelength=1.6)

# 右：最大偏差随区间长度线性下降
ax = axes[1]
Dv = np.linspace(0.05, 1.0, 200)
ax.plot(Dv, Dv / 16.0, color=BLUE, lw=1.7)
for k, col in [(1, GRAY), (2, PURPLE), (4, RED)]:
    d = 1.0 / k
    ax.plot([d], [d / 16.0], "o", color=col, ms=4.2)
    ax.text(d, d / 16.0 + 0.0075, "%d 步" % k, fontsize=7.6, color=col,
            ha="center", va="bottom")
ax.set_xlabel("一步覆盖的区间 $\\Delta$（秒）")
ax.set_ylabel("最大偏差（位移单位，$v_p$ 取 1）")
ax.set_xlim(0, 1.05)
ax.set_ylim(0, 0.086)
style(ax, grid=True)

fig.subplots_adjust(wspace=0.34)
save(fig, "fig11_rhythm", CH)
