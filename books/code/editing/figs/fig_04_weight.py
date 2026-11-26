import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np

# ---------- 图 4.2 单步反演误差沿日程的分布 ----------
CH = "04"

W = np.array([0.40, 0.35, 0.25])
MU = np.array([[1.2, 0.0], [-0.9, 0.9], [-0.6, -1.1]])
SIG = 0.16
T = 1000
N = 100


def sample_x0(rng, n):
    k = rng.choice(3, size=n, p=W)
    return MU[k] + SIG * rng.normal(size=(n, 2))


def abar(t):
    s = (t / T + 0.008) / 1.008
    return np.cos(s * np.pi / 2.0) ** 2


def eps(x, ab):
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
    e = eps(x, a)
    return np.sqrt(b) * (x - np.sqrt(1 - a) * e) / np.sqrt(a) + np.sqrt(1 - b) * e, e


def back(y, a, b):
    e = eps(y, b)
    return np.sqrt(a) * (y - np.sqrt(1 - b) * e) / np.sqrt(b) + np.sqrt(1 - a) * e


rng = np.random.default_rng(51)
x0 = sample_x0(rng, 3000)
ts = np.unique(np.round(np.linspace(0, T, N + 1)).astype(int))
ab = np.array([abar(t) for t in ts])
ab[-1] = 1e-6

meas, pred = [], []
for i in range(len(ts) - 1):
    a, b = ab[i], ab[i + 1]
    xt = np.sqrt(a) * x0 + np.sqrt(1 - a) * rng.normal(size=x0.shape)
    y, e1 = step(xt, a, b)
    z = back(y, a, b)
    e2 = eps(y, b)
    meas.append(np.sqrt(((z - xt) ** 2).sum(1).mean()))
    c = np.sqrt(a * (1 - b) / b) - np.sqrt(1 - a)
    pred.append(np.sqrt(((c * (e1 - e2)) ** 2).sum(1).mean()))
meas = np.array(meas)
pred = np.array(pred)
share = meas[:10].sum() / meas.sum()

fig, ax = plt.subplots(figsize=(W_FULL * 0.80, 2.45))
x = ts[:-1] / T
ax.semilogy(x, meas, "o", color=BLUE, ms=3.0, label="实测单步误差")
ax.semilogy(x, pred, "-", color=RED, lw=1.1, label=r"$c_t\,\|\varepsilon_t-\varepsilon_{t+1}\|$")
ax.set_xlabel(r"反演进度 $t/T$（左端为原图，右端为纯噪声）")
ax.set_ylabel("单步往返误差")
ax.set_xlim(-0.02, 1.02)
ax.set_xticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
ax.set_ylim(1.8e-4, 1.0e-2)
ax.legend(loc="upper right", fontsize=7.6, handlelength=1.4, labelspacing=0.25)
ax.annotate("前 10 步占总量 %.0f%%" % (100 * share), xy=(0.02, meas[0]),
            xytext=(0.14, meas[0] * 1.55), fontsize=7.4, color=GRAY,
            arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=0.6, mutation_scale=6))
style(ax, grid=True)

save(fig, "fig04_weight", CH)
print("share first 10 = %.3f, first 5 = %.3f, median pred/meas = %.2f"
      % (share, meas[:5].sum() / meas.sum(), np.median(pred / meas)))
