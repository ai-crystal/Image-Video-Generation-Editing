import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np
from matplotlib.ticker import FixedLocator, FixedFormatter

CH = "08"

# 一维两峰高斯混合，VP 日程 abar(t) = exp(-3t)，t in [0, 1]
MU = np.array([-1.5, 1.5])
SD = 0.55


def comp(t):
    ab = np.exp(-3.0 * t)
    return np.sqrt(ab), ab * SD ** 2 + (1 - ab)


def score(x, t):
    a, C = comp(t)
    m = a * MU
    lw = -0.5 * (x[..., None] - m) ** 2 / C
    lw = lw - lw.max(axis=-1, keepdims=True)
    w = np.exp(lw)
    w /= w.sum(axis=-1, keepdims=True)
    return -(w * (x[..., None] - m) / C).sum(axis=-1)


def drift(x, t):
    # dx/dt = -beta/2 * x - beta/2 * score, beta = 3
    return -1.5 * x - 1.5 * score(x, t)


def sample_start(n, rng):
    """p_1 的精确样本，避开初值分布不匹配带来的额外误差"""
    a, C = comp(1.0)
    k = rng.integers(0, 2, n)
    return a * MU[k] + rng.normal(0, np.sqrt(C), n)


rng = np.random.default_rng(3)
ref = np.sort(rng.choice(MU, 200000) + rng.normal(0, SD, 200000))
PROB = (np.arange(20000) + 0.5) / 20000
REFQ = np.quantile(ref, PROB)


def w1(xs):
    return np.mean(np.abs(np.quantile(xs, PROB) - REFQ))


def run(nfe, order, seed):
    x = sample_start(20000, np.random.default_rng(seed))
    ts = np.linspace(1.0, 0.0, nfe + 1)
    for i in range(nfe):
        t0, t1 = ts[i], ts[i + 1]
        h = t1 - t0
        if order == 1:
            x = x + h * drift(x, t0)
        else:
            k1 = drift(x, t0)
            xp = x + h * k1
            k2 = drift(xp, t1)
            x = x + 0.5 * h * (k1 + k2)
    return w1(x)


nfe_list = [2, 3, 5, 8, 12, 20, 32, 50, 80, 128, 256]
e1 = [np.mean([run(n, 1, s) for s in range(3)]) for n in nfe_list]
e2 = [np.mean([run(n, 2, s) for s in range(3)]) for n in nfe_list]

def data_sample(n, rng):
    return rng.choice(MU, n) + rng.normal(0, SD, n)


floor = np.mean([w1(data_sample(20000, np.random.default_rng(100 + s))) for s in range(10)])

# 读数：在抽样下限之上取窗口拟合斜率
def slope(ns, es, lo, hi):
    ns, es = np.array(ns, float), np.array(es, float)
    m = (es > 1.4 * floor) & (np.array(ns) >= lo) & (np.array(ns) <= hi)
    return np.polyfit(np.log(ns[m]), np.log(es[m]), 1)[0]


s1 = slope(nfe_list, e1, 3, 64)
s2 = slope(nfe_list, e2, 3, 12)
print("slope Euler %.2f  Heun %.2f  floor %.4f" % (s1, s2, floor))
print("Euler", np.round(e1, 4))
print("Heun ", np.round(e2, 4))

fig, ax = plt.subplots(figsize=(W_FULL * 0.82, 2.35))
ax.loglog(nfe_list, e1, "o-", color=BLUE, ms=3.4, lw=1.3, label="Euler（1 阶，斜率 %.1f）" % s1)
ax.loglog(nfe_list, e2, "s-", color=RED, ms=3.2, lw=1.3, label="Heun（2 阶，斜率 %.1f）" % s2)
ax.axhline(floor, color=GRAY, lw=0.9, ls=(0, (5, 3)))
ax.text(4.4, floor * 1.5, "抽样下限", fontsize=8.2, color=GRAY)
ax.set_xticks([2, 3, 5, 10, 20, 50, 100, 250])
ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
ax.get_xaxis().set_minor_formatter(matplotlib.ticker.NullFormatter())
ax.set_yticks([0.006, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5])
ax.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
ax.get_yaxis().set_minor_formatter(matplotlib.ticker.NullFormatter())
ax.set_ylim(0.005, 0.75)
ax.set_xlim(1.8, 320)
ax.set_xlabel("网络前向次数 NFE")
ax.set_ylabel("$W_1$ 距离")
ax.legend(loc="upper right", fontsize=7.6, handlelength=1.6)
style(ax, grid=True)
save(fig, "fig08_error", CH)
