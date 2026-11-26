import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np

CH = "02"


def f(x):
    return -x + 0.5 * np.sin(x)


def df(x):
    return -1.0 + 0.5 * np.cos(x)


def p0(x):
    g = lambda m: np.exp(-0.5 * ((x - m) / 0.30) ** 2) / (0.30 * np.sqrt(2 * np.pi))
    return 0.5 * g(-1.25) + 0.5 * g(1.25)


# 在网格上解流：映射 x0 -> x_t，同时累积散度
x0 = np.linspace(-3.2, 3.2, 1400)
n = 1000
dt = 1.0 / n
targets = (0.0, 0.35, 0.7, 1.0)
store = {}
x = x0.copy()
acc = np.zeros_like(x0)
store[0.0] = (x.copy(), acc.copy())
for i in range(n):
    k1 = f(x);      d1 = df(x)
    k2 = f(x + 0.5 * dt * k1); d2 = df(x + 0.5 * dt * k1)
    k3 = f(x + 0.5 * dt * k2); d3 = df(x + 0.5 * dt * k2)
    k4 = f(x + dt * k3);       d4 = df(x + dt * k3)
    acc = acc + dt / 6 * (d1 + 2 * d2 + 2 * d3 + d4)
    x = x + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
    tt = (i + 1) * dt
    for T in targets:
        if T > 0 and abs(tt - T) < dt / 2:
            store[T] = (x.copy(), acc.copy())


def density(xg):
    jac = np.gradient(xg, x0)
    return p0(x0) / jac


fig, axes = plt.subplots(1, 2, figsize=(W_FULL, 2.45), gridspec_kw=dict(wspace=0.34))

# ---------------- 左：流的方向与三个时刻的密度 ----------------
ax = axes[0]
for xx in np.linspace(-2.9, 2.9, 15):
    vv = f(np.array([xx]))[0]
    ax.annotate("", xy=(xx + 0.34 * vv, -0.09), xytext=(xx, -0.09),
                arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=0.7, mutation_scale=6))
xs = np.linspace(-3.0, 3.0, 600)
ax.plot(xs, p0(xs), color=BLUE, lw=1.4, label="$p_0$")
for T, col, lab in ((0.35, SAND, "$p_{0.35}$"), (1.0, RED, "$p_1$")):
    xg, _ = store[T]
    ax.plot(xg, density(xg), color=col, lw=1.4, label=lab)
ax.set_xlim(-3.0, 3.0)
ax.set_ylim(-0.15, 2.2)
ax.set_xlabel("$x$")
ax.set_ylabel("密度")
ax.set_yticks([])
ax.legend(loc="upper center", fontsize=8.0, ncol=3, columnspacing=1.0, handlelength=1.3)
style(ax, spines=("top", "right"))

# ---------------- 右：沿轨迹验证两条式子 ----------------
ax = axes[1]
lab_pt = [np.argmin(abs(x0 - s)) for s in (-2.0, -1.25, -0.6, 0.6, 1.25)]
lp0 = np.log(p0(x0[lab_pt]))
ax.plot([], [], color=RED, lw=1.2, label="$-\\int_0^t \\nabla\\!\\cdot\\! f\\,ds$")
ax.plot([], [], "o", color=INK, ms=3.0, label="实测 $\\log(p_t/p_0)$")
for T in targets:
    xg, ac = store[T]
    gain = np.log(density(xg)[lab_pt]) - lp0
    ax.plot([T] * len(lab_pt), -ac[lab_pt], "o", ms=4.4, mfc="none", mec=RED, mew=0.9, zorder=4)
    ax.plot([T] * len(lab_pt), gain, "o", ms=2.2, c=INK, zorder=5)
ax.set_xlabel("$t$")
ax.set_ylabel("$\\log p_t(x_t)-\\log p_0(x_0)$")
ax.set_xticks([0, 0.35, 0.7, 1.0])
ax.set_xlim(-0.1, 1.14)
ax.legend(loc="upper left", fontsize=7.8, handlelength=1.4)
style(ax, grid=True, spines=("top", "right"))

save(fig, "fig02_div", CH)
