import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np

CH = "11"


def sinc(x):
    x = np.asarray(x, dtype=float)
    out = np.ones_like(x)
    nz = np.abs(x) > 1e-9
    out[nz] = np.sin(x[nz]) / x[nz]
    return out


fig, axes = plt.subplots(1, 2, figsize=(W_FULL, 2.85), gridspec_kw={"width_ratios": [1.35, 1.0]})

# 左：相位在宽度 W 内均匀分布时，平均后的波形
ax = axes[0]
t = np.linspace(0, 2, 600)
cases = [(0.0, GRAY, "$W=0$，幅度 1.00"),
         (np.pi / 2, BLUE, "$W=\\pi/2$，幅度 0.90"),
         (2 * np.pi, RED, "$W=2\\pi$，幅度 0")]
for Wd, c, lab in cases:
    a = float(sinc(Wd / 2))
    ax.plot(t, a * np.sin(2 * np.pi * t), color=c, lw=1.6, label=lab)
ax.set_xlabel("时间（周期）")
ax.set_ylabel("平均后的信号")
ax.set_xlim(0, 2)
ax.set_ylim(-1.18, 1.18)
ax.set_yticks([-1, 0, 1])
style(ax, grid=True)
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.30), ncol=3, fontsize=7.4,
          handlelength=1.3, columnspacing=1.0, handletextpad=0.4)

# 右：幅度衰减因子
ax = axes[1]
Wv = np.linspace(0, 2 * np.pi, 400)
ax.plot(Wv, np.abs(sinc(Wv / 2)), color=BLUE, lw=1.7)
for Wd in [np.pi / 2, np.pi, 2 * np.pi]:
    a = abs(float(sinc(Wd / 2)))
    ax.plot([Wd], [a], "o", color=GRAY, ms=4)
    ax.plot([Wd, Wd], [0, a], color=GRAY, lw=0.7, ls=":")
ax.text(np.pi / 2 + 0.10, 0.91, "0.90", fontsize=7.6, color=GRAY)
ax.text(np.pi + 0.10, 0.61, "0.64", fontsize=7.6, color=GRAY)
ax.text(2 * np.pi - 0.30, 0.06, "0", fontsize=7.6, color=GRAY)
ax.set_xlabel("平均窗口宽度（弧度）")
ax.set_ylabel("保留下来的幅度")
ax.set_xticks([0, np.pi / 2, np.pi, 3 * np.pi / 2, 2 * np.pi])
ax.set_xticklabels(["0", "$\\pi/2$", "$\\pi$", "$3\\pi/2$", "$2\\pi$"])
ax.set_xlim(0, 2 * np.pi)
ax.set_ylim(0, 1.14)
style(ax, grid=True)

fig.subplots_adjust(wspace=0.32, bottom=0.34)
save(fig, "fig11_phase", CH)
