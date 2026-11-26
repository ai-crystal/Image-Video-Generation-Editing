import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np

CH = "23"

# 一维线性速度场 v = J x，状态转移矩阵 Phi(t) = exp(J t)
# G(t) = Phi(1) Phi^-1(t) = exp(J(1-t))
# u(t) = G(t) * delta / int_0^1 G(s)^2 ds
t = np.linspace(0.0, 1.0, 400)

fig, ax = plt.subplots(figsize=(W_FULL, 2.6))
for J, c, ls, lab in [
    (3.0, RED, "-", r"$J=3$（拉伸）"),
    (0.0, GRAY, "-", r"$J=0$（常数控制）"),
    (-3.0, BLUE, "-", r"$J=-3$（收缩）"),
]:
    G = np.exp(J * (1.0 - t))
    u = G / np.trapezoid(G ** 2, t)
    ax.plot(t, u / u.max(), color=c, ls=ls, label=lab)

ax.set_xlabel("时间 $t$（0 为数据端，1 为噪声端）")
ax.set_ylabel("归一化控制强度 $|u(t)|$")
ax.set_xlim(0, 1)
ax.set_ylim(0, 1.35)
ax.legend(loc="upper center", ncol=3, handlelength=1.6)
style(ax, grid=True)
save(fig, "fig23_lqr", CH)
