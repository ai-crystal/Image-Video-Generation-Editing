import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np

# 蒙特卡洛：每步方向 = 均值 + 噪声，取 K 个实现后平均，看平均后剩余误差的范数
CH = "07"

rng = np.random.default_rng(11)
Ks = np.array([1, 2, 3, 4, 6, 8, 12, 16, 24, 32])
TRIALS = 6000
err = []
for K in Ks:
    v = rng.normal(0.0, 1.0, size=(TRIALS, K, 2))
    m = v.mean(axis=1)
    err.append(np.sqrt((m ** 2).sum(-1)).mean())
err = np.array(err)

fig, ax = plt.subplots(figsize=(W_FULL * 0.72, 2.25))
ax.loglog(Ks, err, "o-", color=BLUE, ms=3.6, lw=1.2, label="平均后的方向误差")
ax.loglog(Ks, err[0] / np.sqrt(Ks), ls=(0, (4, 3)), color=RED, lw=1.0, label="$c/\\sqrt{K}$")
ax.set_xlabel("每个时间步的噪声采样数 $K$")
ax.set_ylabel("误差范数")
ax.set_xticks([1, 2, 4, 8, 16, 32])
ax.set_xticklabels(["1", "2", "4", "8", "16", "32"])
ax.minorticks_off()
ax.set_ylim(0.15, 2.2)
ax.set_yticks([0.2, 0.3, 0.5, 0.9, 1.6])
ax.set_yticklabels(["0.2", "0.3", "0.5", "0.9", "1.6"])
ax.legend(loc="lower left", fontsize=7.6)
ax.annotate("$K=4$：误差约减半", xy=(4, err[3]), xytext=(6.0, 1.05),
            fontsize=7.2, color=GRAY,
            arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=0.6, mutation_scale=6))
style(ax, spines=("top", "right"))

save(fig, "fig07_variance", CH)
