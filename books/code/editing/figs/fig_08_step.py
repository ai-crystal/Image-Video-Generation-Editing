import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np

# 一维 ODE: dx/dt = -[1 + A sin(3x)], x(1) = 0.6，积到 t = 0
# 精确解用极细的 RK4；Euler 从 t = 1 走到 0，步数 N，看终点误差。
CH = "08"


def f(x):
    return -(1.0 + AA * np.sin(3.0 * x))


def exact(x0, n=40001):
    dt = -1.0 / (n - 1)
    x = x0
    for _ in range(n - 1):
        k1 = f(x)
        k2 = f(x + 0.5 * dt * k1)
        k3 = f(x + 0.5 * dt * k2)
        k4 = f(x + dt * k3)
        x = x + dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6.0
    return x


def euler(x0, N):
    dt = -1.0 / N
    x = x0
    for _ in range(N):
        x = x + dt * f(x)
    return x


x0 = 0.6
Ns = np.array([1, 2, 4, 8, 16, 32, 64, 128])
fig, ax = plt.subplots(figsize=(W_FULL * 0.74, 2.25))

for AA, c in [(0.2, BLUE), (0.5, SAND), (1.0, RED)]:
    xe = exact(x0)
    err = np.array([abs(euler(x0, int(n)) - xe) for n in Ns])
    ax.loglog(Ns, err, "o-", color=c, ms=3.4, lw=1.1, label="$A=%g$" % AA)

ax.set_xlabel("步数 $N$")
ax.set_ylabel("终点误差")
ax.set_xticks([1, 2, 4, 8, 16, 32, 64, 128])
ax.set_xticklabels(["1", "2", "4", "8", "16", "32", "64", "128"])
ax.minorticks_off()
ax.legend(loc="upper right", fontsize=7.6)
ax.axvspan(0.9, 1.32, color=LIGHT, alpha=0.6, lw=0)
ax.set_ylim(4e-4, 3.0)
ax.text(1.05, 6.5e-4, "一步模型只能取这里", fontsize=7.0, color=GRAY, va="bottom", ha="left")
style(ax, spines=("top", "right"))

save(fig, "fig08_step", CH)
