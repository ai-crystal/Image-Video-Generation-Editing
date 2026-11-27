import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np

CH = "11"

# 面积加权：整图 MSE = p * MSE_in + (1-p) * MSE_bg
E_BG = 1e-5                      # 背景几乎没动，约 50 dB
E_IN = [0.005, 0.01, 0.02]       # 编辑区内三种质量
COLORS = [GREEN, BLUE, RED]
p = np.linspace(0.005, 0.6, 400)


def psnr(mse):
    return 10.0 * np.log10(1.0 / mse)


fig, ax = plt.subplots(figsize=(W_FULL, 2.6))

for e, c in zip(E_IN, COLORS):
    mse_all = p * e + (1 - p) * E_BG
    ax.plot(p * 100, psnr(mse_all), color=c, lw=1.5,
            label=r"编辑区 MSE $=%.3f$" % e)
    ax.axhline(psnr(e), color=c, ls=(0, (4, 3)), lw=0.9, alpha=0.85)

# 6% 处的读数，与正文手算一致
p0, e0 = 0.06, 0.02
mse0 = p0 * e0 + (1 - p0) * E_BG
ax.plot([p0 * 100], [psnr(mse0)], "o", ms=3.6, color=RED, zorder=5)
ax.axvline(p0 * 100, color=LIGHT, lw=0.8, ls=(0, (2, 2)), zorder=0)
ax.text(p0 * 100 + 0.9, 47.6, r"$p=6\%$", fontsize=8.2, color=GRAY)
ax.annotate("%.1f dB" % psnr(mse0), xy=(p0 * 100, psnr(mse0)),
            xytext=(8.4, 25.6), fontsize=8.2, color=RED,
            arrowprops=dict(arrowstyle="-", color=RED, lw=0.6))
ax.annotate("编辑区自身 %.1f dB" % psnr(e0), xy=(22, psnr(e0)),
            xytext=(3.0, 13.4), fontsize=8.2, color=RED,
            arrowprops=dict(arrowstyle="-", color=RED, lw=0.6))

ax.set_xlabel("编辑区面积占比 (%)")
ax.set_ylabel("PSNR (dB)")
ax.set_xlim(0, 60)
ax.set_ylim(12, 54)
ax.set_xticks([0, 10, 20, 30, 40, 50, 60])
ax.legend(loc="upper right", ncol=1, handlelength=1.6, borderpad=0.2,
          labelspacing=0.35)
style(ax, grid=True)

save(fig, "fig11_maskpsnr", CH)
