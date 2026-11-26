import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np

CH = "11"

# 一条带弯曲的路径：x(t) = a + (b-a) t + kappa sin(pi t) n
# 速度 u(t) = (b-a) + kappa pi cos(pi t)
# 精确位移 = b - a（正弦项积分为零），单步 Euler 的位移 = u(1) = (b-a) - kappa pi
# 所以单步误差随曲率 kappa 线性增长，随步数按 1/N 衰减。
a, b = 0.0, 1.0
Ns = np.array([1, 2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 64])
kappas = [0.5, 2.0, 8.0]
colors = [BLUE_L, BLUE, RED]

fig, ax = plt.subplots(figsize=(W_HALF, 2.05))
for kap, col in zip(kappas, colors):
    errs = []
    for N in Ns:
        h = 1.0 / N
        x = 1.0  # 从 t=1 出发
        for k in range(N):
            t = 1.0 - k * h
            u = (b - a) + kap * np.pi * np.cos(np.pi * t)
            x -= h * u  # 往回走
        errs.append(abs(x - a))
    ax.plot(Ns, errs, "-o", ms=3.2, lw=1.3, color=col, label=r"$\kappa=%.1f$" % kap)

ref = np.array([1.0, 64.0])
ax.plot(ref, 0.9 * 3.0 / ref, "--", lw=0.9, color=GRAY, alpha=0.8)
ax.text(6.0, 0.28, r"斜率 $-1$", fontsize=7.4, color=GRAY)

ax.set_xscale("log", base=2)
ax.set_yscale("log")
ax.set_xlabel("采样步数 $N$")
ax.set_ylabel(r"终点误差 $|x_{\mathrm{out}}-x_{\mathrm{tar}}|$")
ax.set_xticks([1, 2, 4, 8, 16, 32, 64])
ax.set_xticklabels(["1", "2", "4", "8", "16", "32", "64"])
ax.legend(loc="upper right", handlelength=1.4, borderaxespad=0.2)
style(ax, grid=True)
save(fig, "fig11_steps", CH)
