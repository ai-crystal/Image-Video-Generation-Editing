import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np

CH = "02"
rng = np.random.default_rng(7)
d = 256
trials = 400


def diag_same():
    lam = 0.5 + 0.02 * rng.normal(size=d)
    return np.diag(lam)


def dense_random():
    a = rng.normal(size=(d, d)) / np.sqrt(d)
    return (a + a.T) / 2


def cancel():
    lam = np.empty(d)
    lam[0::2] = 1.0
    lam[1::2] = -0.98
    return np.diag(lam)


cases = (("对角、同号", diag_same, BLUE),
         ("随机稠密", dense_random, GREEN),
         ("正负抵消", cancel, RED))

ks = np.array([1, 2, 4, 8, 16, 32, 64, 128])
fig, ax = plt.subplots(figsize=(W_FULL * 0.68, 2.45))

for name, build, col in cases:
    J = build()
    tr = np.trace(J)
    rel = []
    for k in ks:
        E = rng.normal(size=(trials, k, d))
        est = np.einsum("tki,ij,tkj->t", E, J, E) / k
        rel.append(est.std() / abs(tr))
    rel = np.array(rel)
    ax.loglog(ks, rel, color=col, lw=1.3, marker="o", ms=2.8, label=name)
    print(name, "trace %.2f" % tr, "rel@1 %.3f" % rel[0], "rel@128 %.4f" % rel[-1])

ref = 1.0 / np.sqrt(ks)
ax.loglog(ks, ref * 0.9, color=GRAY, lw=0.8, ls="--")
ax.text(9, 0.14, "斜率 $-1/2$", fontsize=8.0, color=GRAY)
ax.set_xlabel("每次估计用的探针数 $k$")
ax.set_ylabel("相对标准差")
ax.set_xlim(0.85, 170)
ax.legend(loc="lower left", fontsize=8.0, handlelength=1.6, labelspacing=0.28)
style(ax, grid=True, spines=("top", "right"))

save(fig, "fig02_hutch", CH)
