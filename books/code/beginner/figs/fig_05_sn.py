import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np

CH = "05"

rng = np.random.default_rng(0)


def make_matrix(ratio, n=48):
    """构造最大奇异值为 1、第二奇异值为 ratio 的矩阵。"""
    A = rng.normal(size=(n, n))
    U, _, Vt = np.linalg.svd(A)
    sv = np.concatenate([[1.0, ratio], ratio * np.geomspace(0.9, 0.15, n - 2)])
    return U @ np.diag(sv) @ Vt


fig, ax = plt.subplots(figsize=(W_HALF * 1.9, 2.35))
K = 12
ks = np.arange(1, K + 1)
for ratio, c in [(0.4, BLUE), (0.8, SAND), (0.95, RED)]:
    W = make_matrix(ratio)
    v = rng.normal(size=W.shape[0])
    v /= np.linalg.norm(v)
    err = []
    for _ in range(K):
        u = W @ v
        u /= np.linalg.norm(u)
        v = W.T @ u
        v /= np.linalg.norm(v)
        err.append(abs(np.linalg.norm(W @ v) - 1.0))
    ax.semilogy(ks, err, marker="o", ms=2.6, lw=1.2, color=c,
                label="$\\sigma_2/\\sigma_1=%.2f$" % ratio)
    # 理论衰减 (sigma2/sigma1)^{2k}
    kk = np.linspace(1, K, 100)
    ax.semilogy(kk, 0.7 * ratio ** (2 * kk), color=c, lw=0.7, ls=(0, (3, 3)))

ax.axhline(1e-2, color=GRAY, lw=0.7, ls=(0, (5, 3)))
ax.text(4.2, 1.28e-2, "1% 误差线", fontsize=7.8, color=GRAY)
ax.set_xlabel("幂迭代次数")
ax.set_ylabel("$\\sigma_1$ 的相对误差")
ax.set_xticks([1, 3, 5, 7, 9, 11])
ax.set_ylim(1e-7, 5.0)
ax.legend(loc="lower left", fontsize=7.6)
style(ax)
save(fig, "fig05_sn", CH)
