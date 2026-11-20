import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np

CH = "08"


mu = np.array([-1.5, 1.5])
sd = 0.55


def score_exact(x, t):
    ab = np.exp(-3.0 * t)
    s2 = 1 - ab
    comp = []
    for m in mu:
        C = ab * sd ** 2 + s2
        comp.append((x - np.sqrt(ab) * m) / C)
    # 简化为两分量等权，用后验权重
    w = []
    for m in mu:
        C = ab * sd ** 2 + s2
        w.append(np.exp(-0.5 * (x - np.sqrt(ab) * m) ** 2 / C) / np.sqrt(C))
    w = np.array(w)
    w /= w.sum()
    return -sum(wk * c for wk, c in zip(w, comp))


rng = np.random.default_rng(0)
x_true = rng.choice(mu, 20000) + rng.normal(0, sd, 20000)
x0 = np.sort(x_true)

def run(nfe, order):
    x = rng.normal(0, 1, 4000)
    ts = np.linspace(1.0, 0.0, nfe + 1)
    for i in range(nfe):
        t0, t1 = ts[i], ts[i + 1]
        h = t1 - t0
        def f(tt, xx):
            return -0.5 * 3.0 * xx - 0.5 * 3.0 * score_exact(xx, tt)
        if order == 1:
            x = x + h * f(t0, x)
        else:
            k1 = f(t0, x)
            xp = x + h * k1
            k2 = f(t1, xp)
            x = x + 0.5 * h * (k1 + k2)
    xs = np.sort(x)
    # W1 距离，两样本等量
    n = min(len(xs), 4000)
    return np.mean(np.abs(xs[:n] - x0[::max(1, len(x0) // n)][:n]))

nfe_list = [2, 3, 5, 8, 12, 20, 30, 50]
e1 = [run(n, 1) for n in nfe_list]
e2 = [run(n, 2) for n in nfe_list]

fig, ax = plt.subplots(figsize=(W_FULL * 0.8, 2.2))
ax.loglog(nfe_list, e1, "o-", color=BLUE, ms=3.2, lw=1.2, label="Euler（1 阶）")
ax.loglog(nfe_list, e2, "s-", color=RED, ms=3.2, lw=1.2, label="Heun（2 阶）")
ax.set_xlabel("网络前向次数 NFE")
ax.set_ylabel("$W_1$ 距离")
ax.legend(loc="lower left", fontsize=7.6)
ax.grid(True, which="both", color=LIGHT, lw=0.5, alpha=0.7)
ax.set_axisbelow(True)
style(ax, spines=("top", "right"))
save(fig, "fig08_error", CH)
