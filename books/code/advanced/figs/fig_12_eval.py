import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np

CH = "12"

D = 32
RNG = np.random.default_rng(7)


def frechet_to_standard(x):
    """样本到标准正态的 Fréchet 距离（真值解析）。"""
    mu = x.mean(axis=0)
    xc = x - mu
    cov = xc.T @ xc / len(x)
    w = np.linalg.eigvalsh(cov)
    w = np.clip(w, 0, None)
    d2 = mu @ mu + D + w.sum() - 2.0 * np.sqrt(w).sum()
    return np.sqrt(max(d2, 0.0))


ns = np.array([100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000])
reps = 60
means, stds = [], []
for n in ns:
    vals = []
    for _ in range(reps):
        x = RNG.standard_normal((n, D))
        vals.append(frechet_to_standard(x))
    vals = np.array(vals)
    means.append(vals.mean())
    stds.append(vals.std())
    print("%6d  mean %.3f  std %.3f" % (n, vals.mean(), vals.std()))

means = np.array(means)
stds = np.array(stds)

fig, ax = plt.subplots(figsize=(W_HALF * 1.5, 2.5))
ax.fill_between(ns, means - stds, means + stds, color=BLUE_L, alpha=0.45, lw=0)
ax.plot(ns, means, color=BLUE, lw=1.6, marker="o", ms=3.4)
ax.text(1100, 0.115, "偏差与 $n^{-1/2}$ 成正比", fontsize=8, color=GRAY)
ax.annotate("%.2f" % means[3], xy=(ns[3], means[3]), xytext=(ns[3] * 1.5, means[3] * 1.5),
            fontsize=7.6, color=GRAY,
            arrowprops=dict(arrowstyle="-", lw=0.6, color=GRAY))
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlabel("评测样本数 $n$")
ax.set_ylabel("与真实分布的 Fréchet 距离")
ax.set_xlim(80, 70000)
style(ax, grid=True)
save(fig, "fig12_eval_noise", CH)
