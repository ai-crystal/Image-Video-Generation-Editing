import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np

CH = "17"

# 双峰数据（均值 ±1，标准差 0.1）在直线路径上的边缘速度场，从 z=1.5 出发积分到 t=0。
S = 0.1


def post_mean(x, t):
    v = (1 - t) ** 2 * S * S + t * t
    mp, mm = 1 - t, -(1 - t)
    cov = (1 - t) * S * S
    lp = -(x - mp) ** 2 / (2 * v)
    lm = -(x - mm) ** 2 / (2 * v)
    top = max(lp, lm)
    a, b = np.exp(lp - top), np.exp(lm - top)
    ep = 1 + cov * (x - mp) / v
    em = -1 + cov * (x - mm) / v
    return (a * ep + b * em) / (a + b)


def vel(x, t):
    if t < 1e-9:
        return 0.0
    return (x - post_mean(x, t)) / t


def euler(x0, n, t_end=1e-6):
    ts = np.linspace(1.0, t_end, n + 1)
    x = x0
    xs = [x]
    for i in range(n):
        x = x + (ts[i + 1] - ts[i]) * vel(x, ts[i])
        xs.append(x)
    return np.array(xs), ts


def rk4(x0, n, t_end=1e-6):
    ts = np.linspace(1.0, t_end, n + 1)
    x = x0
    xs = [x]
    for i in range(n):
        t, h = ts[i], ts[i + 1] - ts[i]
        k1 = vel(x, t)
        k2 = vel(x + h / 2 * k1, t + h / 2)
        k3 = vel(x + h / 2 * k2, t + h / 2)
        k4 = vel(x + h * k3, t + h)
        x = x + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        xs.append(x)
    return np.array(xs), ts


Z = 1.5
ref, ref_t = rk4(Z, 4000)

fig, axes = plt.subplots(1, 2, figsize=(W_FULL, 2.35), gridspec_kw=dict(wspace=0.34))

ax = axes[0]
ax.plot(ref_t, ref, color=INK, lw=1.2, label="参考解")
for n, c, ls in [(1, RED, (0, (4, 2))), (2, SAND, (0, (4, 2))), (4, BLUE, (0, (4, 2))), (8, GREEN, (0, (4, 2)))]:
    xs, ts = euler(Z, n)
    ax.plot(ts, xs, color=c, lw=1.1, ls=ls, label="$N=%d$" % n)
ax.set_xlim(1.02, -0.02)
ax.set_ylim(-0.05, 1.65)
ax.set_xlabel("$t$（采样从左向右）")
ax.set_ylabel("$x_t$")
ax.legend(loc="lower left", bbox_to_anchor=(0.0, 1.0), ncol=5, handlelength=1.5, columnspacing=0.8, borderpad=0.1)
style(ax, grid=True)

ax = axes[1]
Ns = np.array([1, 2, 4, 8, 16, 32, 64, 128, 256])
errs = []
for n in Ns:
    xs, _ = euler(Z, n)
    errs.append(abs(xs[-1] - ref[-1]))
errs = np.array(errs)
print(np.round(errs, 4))
ax.loglog(Ns, errs, "o-", color=BLUE, ms=3, lw=1.3)
ax.loglog(Ns, errs[0] / Ns, "--", color=LIGHT, lw=1.2)
ax.text(60, 0.02, "$1/N$", fontsize=8.4, color=GRAY)
ax.set_xlabel("Euler 步数 $N$")
ax.set_ylabel("端点误差")
ax.set_yticks([1e-3, 1e-2, 1e-1, 1])
ax.set_ylim(1e-3, 2)
style(ax, grid=True)

save(fig, "fig17_steps", CH)
