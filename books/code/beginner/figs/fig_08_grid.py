import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np
from matplotlib.ticker import FixedLocator, FixedFormatter

CH = "08"

T = 1000
beta = np.linspace(1e-4, 0.02, T)
abar = np.cumprod(1 - beta)
lam = np.log(abar / (1 - abar))          # 对数信噪比，t=1 时最大

N = 20
idx = np.round(np.linspace(T - 1, 0, N + 1)).astype(int)
gap_idx = np.abs(np.diff(lam[idx]))

lam_t = np.linspace(lam[-1], lam[0], N + 1)        # 在 log-SNR 上均匀取点
gap_lam = np.abs(np.diff(lam_t))

print("索引均匀：min %.2f  max %.2f  总跨度 %.2f" % (gap_idx.min(), gap_idx.max(), np.abs(lam[0] - lam[-1])))
print("间距/均匀值：max %.1f 倍，中位数 %.1f 倍" % (gap_idx.max() / gap_lam[0], np.median(gap_idx) / gap_lam[0]))

fig, ax = plt.subplots(figsize=(W_FULL * 0.8, 2.25))
k = np.arange(1, N + 1)
ax.semilogy(k, gap_idx, "o-", color=BLUE, ms=3.4, lw=1.3, label="按索引均匀取 20 步")
ax.semilogy(k, gap_lam, "--", color=GRAY, lw=1.1, label="按对数信噪比均匀取 20 步")
ax.set_xticks([1, 5, 10, 15, 20])
ax.get_xaxis().set_major_formatter(FixedFormatter(["1", "5", "10", "15", "20"]))
ax.set_yticks([0.3, 1, 3, 6])
ax.get_yaxis().set_major_formatter(FixedFormatter(["0.3", "1", "3", "6"]))
ax.get_yaxis().set_minor_formatter(matplotlib.ticker.NullFormatter())
ax.set_ylim(0.3, 8)
ax.set_xlim(0.3, 20.9)
ax.set_xlabel("采样步序号（从高噪声端数）")
ax.set_ylabel("单步跨越的 $\\Delta\\lambda$")
ax.legend(loc="upper left", fontsize=7.6, handlelength=1.8)
style(ax, grid=True)
save(fig, "fig08_grid", CH)
