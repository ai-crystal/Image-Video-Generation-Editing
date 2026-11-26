import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np
from scipy.ndimage import uniform_filter

CH = "20"

# 线性噪声日程
T = 1000
beta = np.linspace(1e-4, 0.02, T)
abar = np.cumprod(1 - beta)

# 合成场景：天空、太阳、两道山脊、山上的细纹理
n = 256
yy, xx = np.mgrid[0:n, 0:n] / n
img = 0.45 - 0.55 * (yy - 0.5)
img += 0.55 * (((xx - 0.70) ** 2 + (yy - 0.26) ** 2) < 0.085 ** 2)
ridge1 = 0.60 + 0.05 * np.sin(2 * np.pi * 1.2 * xx + 0.4)
ridge2 = 0.76 + 0.04 * np.sin(2 * np.pi * 0.9 * xx + 2.1)
img -= 0.35 * (yy > ridge1)
img -= 0.25 * (yy > ridge2)
img += 0.06 * np.sin(2 * np.pi * 22 * xx) * (yy > ridge1 + 0.02)
img += 0.05 * np.sin(2 * np.pi * 17 * yy) * (yy > ridge2 + 0.02)
img = np.clip(img, -1, 1)

rng = np.random.default_rng(11)
t0s = [0, 150, 350, 550]

fig, axes = plt.subplots(2, 4, figsize=(W_FULL, 2.62),
                         gridspec_kw=dict(wspace=0.05, hspace=0.10))
for j, t0 in enumerate(t0s):
    a = abar[t0]
    eps = np.zeros((n, n)) if t0 == 0 else rng.normal(size=(n, n))
    xt = np.sqrt(a) * img + np.sqrt(1 - a) * eps
    low = uniform_filter(xt, size=20, mode="reflect")
    for i, im in enumerate([xt, low]):
        ax = axes[i, j]
        ax.imshow(im, cmap="gray", vmin=-1.15, vmax=1.15, interpolation="nearest")
        ax.set_xticks([])
        ax.set_yticks([])
        for s in ax.spines.values():
            s.set_color(LIGHT)
        if j == 0:
            ax.set_ylabel(["加噪", "低通"][i], fontsize=7.6, color=GRAY, rotation=90, labelpad=4)
    axes[1, j].set_xlabel("源图" if t0 == 0 else "$t_0=%d$" % t0, fontsize=7.6, color=INK)

save(fig, "fig20_snr", CH)
