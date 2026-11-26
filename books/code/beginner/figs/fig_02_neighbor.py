import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np

CH = "02"


def pair_stats(n, d, seed=0):
    rng = np.random.default_rng(seed)
    x = rng.normal(size=(n, d)).astype(np.float32)
    g = x @ x.T
    sq = np.diag(g).copy()
    d2 = sq[:, None] + sq[None, :] - 2.0 * g
    iu = np.triu_indices(n, 1)
    dist = np.sqrt(np.maximum(d2[iu], 0.0))
    return float(dist.min()), float(dist.mean()), float(dist.max())


dims = [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384]
n = 1000
pts = []
for d in dims:
    lo, mid, hi = pair_stats(n, d, seed=11 + d)
    pts.append((d, hi / lo - 1.0))
    print("d=%6d  min=%8.3f mean=%8.3f max=%8.3f  ratio-1=%.4f" % (d, lo, mid, hi, hi / lo - 1))

lo, mid, hi = pair_stats(n, 196608, seed=7)
big = (196608, hi / lo - 1.0)
print("d=196608  min=%.2f mean=%.2f max=%.2f  ratio-1=%.4f" % (lo, mid, hi, hi / lo - 1))

fig, ax = plt.subplots(figsize=(W_FULL * 0.9, 2.45))
xs = np.array([p[0] for p in pts])
ys = np.array([p[1] for p in pts])
ax.plot(xs, ys, "o-", color=BLUE, ms=3.2, lw=1.0, label="实测（$n=1000$ 个高斯样本）")

# 参考斜率 -1/2
ref = np.array([2.0, 200000.0])
ax.plot(ref, 1.60 * ref ** -0.5, ls=(0, (4, 3)), color=GRAY, lw=1.0, label="斜率 $-1/2$ 的参考线")

ax.plot([big[0]], [big[1]], "o", ms=5.0, mfc="white", mec=RED, mew=1.4, zorder=4)
ax.annotate("196608 维：差 1.4%\n距离 622.6 / 627.1 / 631.5",
            xy=big, xytext=(5.0e4, 2.6e-3), fontsize=7.6, color=RED, ha="right",
            va="center", linespacing=1.7,
            arrowprops=dict(arrowstyle="-", color=RED, lw=0.7,
                            connectionstyle="arc3,rad=-0.28"))

ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlabel("维度 $d$（对数坐标）")
ax.set_ylabel("$d_{\\max}/d_{\\min}-1$")
ax.set_xlim(1.6, 4.0e5)
ax.set_ylim(8e-4, 2.0)
style(ax, grid=True)
ax.legend(loc="upper right", handlelength=2.2, borderpad=0.6)
save(fig, "fig02_neighbor", CH)
