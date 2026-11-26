import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np

# ---------- 图 9.2 共享噪声与帧间抖动 ----------
CH = "09"
rng = np.random.default_rng(7)
L = 24
A = 1.5          # 单帧输出扰动的标准差，单位：灰度级
z0 = rng.normal(size=1)          # 共享部分（同一像素在所有帧里共用）


def trace(rho, n=L):
    d = rng.normal(size=n)
    eps = np.sqrt(rho) * z0 + np.sqrt(1.0 - rho) * d
    return A * eps


fig, axes = plt.subplots(1, 2, figsize=(W_FULL, 2.0), gridspec_kw=dict(wspace=0.34))

ax = axes[0]
frames = np.arange(1, L + 1)
ax.axhline(0, color=LIGHT, lw=0.8, zorder=0)
for rho, col, lab in ((0.0, RED, r"$\rho=0$（独立）"),
                      (0.9, BLUE, r"$\rho=0.9$（共享九成）")):
    v = trace(rho)
    ax.plot(frames, v, "-o", color=col, ms=2.6, lw=1.0, label=lab)
ax.set_xlabel("帧序号")
ax.set_ylabel("该像素的灰度偏移（灰度级）")
ax.set_xlim(0, L + 1)
ax.set_ylim(-6.5, 9.5)
ax.set_yticks([-4, -2, 0, 2, 4])
ax.legend(loc="upper left", bbox_to_anchor=(0.0, 1.03), handlelength=1.4, labelspacing=0.3)

ax = axes[1]
rhos = np.linspace(0, 1, 201)
ax.plot(rhos, np.sqrt(2 * (1 - rhos)), color=INK, lw=1.1,
        label=r"理论值 $(2(1-\rho))^{1/2}$")
for rho, col, lab in ((0.0, RED, "独立采样实测"), (0.9, BLUE, "共享九成实测")):
    sd = np.std(np.diff(trace(rho, 4000)))
    ax.scatter([rho], [sd / A], s=26, color=col, zorder=5, edgecolor="white", lw=0.6,
               label=lab)
ax.set_xlabel(r"共享比例 $\rho$")
ax.set_ylabel(r"帧间差标准差 $/\sigma$")
ax.set_xlim(-0.04, 1.04)
ax.set_ylim(0, 1.72)
ax.legend(loc="lower left", handlelength=1.4, labelspacing=0.3, fontsize=7.6)
style(ax, grid=True)
style(axes[0])

save(fig, "fig09_flicker", CH)
