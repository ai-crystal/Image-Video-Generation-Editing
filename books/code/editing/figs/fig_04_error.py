import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np

# ---------- 图 4.3 反演漂移的两个可测量：重建误差与端点方差 ----------
CH = "04"

W = np.array([0.40, 0.35, 0.25])
MU = np.array([[1.2, 0.0], [-0.9, 0.9], [-0.6, -1.1]])
SIG = 0.16
T = 1000


def sample_x0(rng, n):
    k = rng.choice(3, size=n, p=W)
    return MU[k] + SIG * rng.normal(size=(n, 2))


def abar(t):
    s = (t / T + 0.008) / 1.008
    return np.cos(s * np.pi / 2.0) ** 2


def eps(x, ab):
    """三峰混合分布在噪声水平 ab 下的噪声预测（解析式）。"""
    s2 = ab * SIG ** 2 + (1 - ab)
    lp = []
    for k in range(3):
        lp.append(np.log(W[k]) - ((x - np.sqrt(ab) * MU[k]) ** 2).sum(1) / (2 * s2))
    lp = np.stack(lp, 1)
    lp -= lp.max(1, keepdims=True)
    r = np.exp(lp)
    r /= r.sum(1, keepdims=True)
    sc = np.zeros_like(x)
    for k in range(3):
        sc += r[:, [k]] * (x - np.sqrt(ab) * MU[k]) / s2
    return np.sqrt(1 - ab) * sc


def step(x, a, b):
    """DDIM 一步：查询在水平 a，走到水平 b。"""
    e = eps(x, a)
    return np.sqrt(b) * (x - np.sqrt(1 - a) * e) / np.sqrt(a) + np.sqrt(1 - b) * e


def back(y, a, b):
    """采样一步：查询在水平 b，回到水平 a。"""
    e = eps(y, b)
    return np.sqrt(a) * (y - np.sqrt(1 - b) * e) / np.sqrt(b) + np.sqrt(1 - a) * e


def invert_implicit(x, a, b, iters=3):
    y = step(x, a, b)
    for _ in range(iters):
        y = y + (x - back(y, a, b))
    return y


def run(rng, x0, N, mode):
    ts = np.unique(np.round(np.linspace(0, T, N + 1)).astype(int))
    ab = np.array([abar(t) for t in ts])
    ab[0] = 1.0
    ab[-1] = 1e-6
    x = x0.copy()
    for i in range(len(ts) - 1):
        a, b = ab[i], ab[i + 1]
        x = step(x, a, b) if mode == "naive" else invert_implicit(x, a, b)
    xt = x
    for i in range(len(ts) - 2, -1, -1):
        x = back(x, ab[i], ab[i + 1])
    return np.sqrt(((x - x0) ** 2).sum(1).mean()), (xt ** 2).sum(1).mean() / 2.0


rng = np.random.default_rng(21)
BATCH = [sample_x0(rng, 800) for _ in range(4)]
Ns = np.array([5, 10, 20, 30, 50, 100, 200, 400])
e_naive, e_impl, disp = [], [], []
for N in Ns:
    a_ = [run(rng, x, N, "naive") for x in BATCH]
    b_ = [run(rng, x, N, "impl") for x in BATCH]
    e_naive.append(np.mean([v[0] for v in a_]))
    e_impl.append(np.mean([v[0] for v in b_]))
    disp.append(np.mean([v[1] for v in a_]))
e_naive = np.array(e_naive)
e_impl = np.array(e_impl)
disp = np.array(disp)

fig, axes = plt.subplots(1, 2, figsize=(W_FULL, 2.3))
ax = axes[0]
ax.loglog(Ns, e_naive, "o-", color=BLUE, ms=3.4, lw=1.2, label="逐点查询（朴素反演）")
ax.loglog(Ns, e_impl, "s-", color=GREEN, ms=3.2, lw=1.2, label="每步解不动点")
ax.loglog(Ns, e_naive[4] * (50.0 / Ns), ls=(0, (4, 3)), color=RED, lw=1.0, label=r"$\propto 1/N$")
ax.set_xlabel("步数 $N$")
ax.set_ylabel("往返误差（数据标准差 0.89）")
ax.set_xticks([5, 10, 20, 50, 100, 200, 400])
ax.set_xticklabels(["5", "10", "20", "50", "100", "200", "400"])
ax.minorticks_off()
ax.set_ylim(3e-7, 0.6)
ax.legend(loc="lower left", fontsize=7.2, labelspacing=0.22, handlelength=1.5)
ax.set_title("(a)", fontsize=8.6, color=GRAY, loc="left", pad=3)
style(ax)

ax = axes[1]
ax.axhline(1.0, color=SAND, lw=0.9, ls=(0, (4, 3)))
ax.plot(Ns, disp, "o-", color=PURPLE, ms=3.4, lw=1.2)
ax.set_xscale("log")
ax.set_xlabel("步数 $N$")
ax.set_ylabel(r"端点 $\mathbb{E}\|x_T\|^2/d$")
ax.set_xticks([5, 10, 20, 50, 100, 200, 400])
ax.set_xticklabels(["5", "10", "20", "50", "100", "200", "400"])
ax.minorticks_off()
ax.set_ylim(0.25, 1.09)
ax.set_yticks([0.5, 0.75, 1.0])
ax.annotate("标准正态：1.0", xy=(8, 1.0), xytext=(6.2, 1.035), fontsize=7.0, color=GRAY)
ax.annotate("$N=20$：0.74", xy=(20, disp[2]), xytext=(26, 0.63), fontsize=7.0, color=GRAY,
            arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=0.6, mutation_scale=6))
ax.set_title("(b)", fontsize=8.6, color=GRAY, loc="left", pad=3)
style(ax)

fig.subplots_adjust(wspace=0.36)
save(fig, "fig04_error", CH)
print("naive", np.round(e_naive, 5), "impl", np.round(e_impl, 6), "disp", np.round(disp, 3))
