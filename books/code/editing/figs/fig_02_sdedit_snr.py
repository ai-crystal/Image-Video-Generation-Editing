import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np
from matplotlib.lines import Line2D

# ---------- 图 2.4  不同频带的信号幅度与噪声幅度 ----------
# DDPM 线性日程：T=1000，beta 从 1e-4 线性升到 0.02
CH = "02"
T = 1000
beta = np.linspace(1e-4, 0.02, T)
abar = np.cumprod(1.0 - beta)
t = np.arange(1, T + 1)

sig = np.sqrt(abar)            # 原图幅度保留系数
noi = np.sqrt(1.0 - abar)      # 噪声幅度

A_L, A_H = 4.0, 1.0            # 低频、高频系数的幅度（噪声标准差取 1）

# 信号与噪声幅度持平的时刻：abar = 1/(1+A^2)
t_hi = int(np.argmin(np.abs(abar - 0.5))) + 1
t_lo = int(np.argmin(np.abs(abar - 1.0 / (1 + A_L ** 2)))) + 1

fig, ax = plt.subplots(figsize=(W_FULL, 2.35))

ax.axvspan(t_hi, t_lo, color=LIGHT, alpha=0.55, lw=0, zorder=0)

ax.plot(t, A_L * sig, color=BLUE, lw=1.5)
ax.plot(t, A_H * sig, color=RED, lw=1.5)
ax.plot(t, noi, color=GRAY, lw=1.0, ls=(0, (4, 3)))

y_hi = A_H * sig[t_hi - 1]
y_lo = A_L * sig[t_lo - 1]
ax.scatter([t_hi, t_lo], [y_hi, y_lo], s=20, color=INK, zorder=5)

ax.annotate("高频与噪声持平\n$t_0\\approx %d$" % t_hi, xy=(t_hi, y_hi), xytext=(t_hi - 26, 1.75),
            fontsize=7.0, color=RED, ha="right", va="center",
            arrowprops=dict(arrowstyle="-|>", color=RED, lw=0.55, mutation_scale=6,
                            connectionstyle="arc3,rad=0.12"))
ax.annotate("低频与噪声持平\n$t_0\\approx %d$" % t_lo, xy=(t_lo, y_lo), xytext=(t_lo + 26, 1.75),
            fontsize=7.0, color=BLUE, ha="left", va="center",
            arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=0.55, mutation_scale=6,
                            connectionstyle="arc3,rad=-0.12"))

ax.text((t_hi + t_lo) / 2, 3.55, "结构还在、细节已重采样", fontsize=7.0, ha="center", color=GRAY)
ax.set_xlabel("加噪时刻 $t_0$")
ax.set_ylabel("幅度（噪声 $\\sigma=1$）")
ax.set_xlim(0, T)
ax.set_ylim(0, 4.7)
ax.set_xticks([0, 200, 400, 600, 800, 1000])

handles = [
    Line2D([], [], color=BLUE, lw=1.5, label="低频分量 $4\\sqrt{\\bar\\alpha}$"),
    Line2D([], [], color=RED, lw=1.5, label="高频分量 $\\sqrt{\\bar\\alpha}$"),
    Line2D([], [], color=GRAY, lw=1.0, ls=(0, (4, 3)), label="噪声 $\\sqrt{1-\\bar\\alpha}$"),
]
ax.legend(handles=handles, loc="upper right", handlelength=1.7, labelspacing=0.25)
style(ax, grid=False)

save(fig, "fig02_sdedit_snr", CH)
