import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np

CH = "04"
rng = np.random.default_rng(11)

# 一维两峰数据：两个等权、窄方差的高斯
MU, SG, NDATA = 1.0, 0.13, 1400
label = rng.integers(0, 2, NDATA)
xs = np.where(label == 0, -MU, MU) + rng.normal(0, SG, NDATA)

fig, axes = plt.subplots(1, 2, figsize=(W_FULL, 2.35), gridspec_kw=dict(wspace=0.28))

# ---------- 左：数据密度与单峰生成分布 ----------
ax = axes[0]
grid = np.linspace(-2.0, 2.0, 700)
p_data = 0.5 * np.exp(-(grid + MU) ** 2 / (2 * SG**2)) + 0.5 * np.exp(-(grid - MU) ** 2 / (2 * SG**2))
p_data /= np.sqrt(2 * np.pi) * SG
m, v = xs.mean(), xs.var()
p_fit = np.exp(-(grid - m) ** 2 / (2 * v)) / np.sqrt(2 * np.pi * v)

ax.fill_between(grid, p_data, color=BLUE, alpha=0.16, lw=0)
ax.plot(grid, p_data, color=BLUE, lw=1.4, label="数据密度")
ax.plot(grid, p_fit, color=RED, lw=1.3, ls=(0, (5, 2)), label="单峰模型的最优拟合")
ax.axvline(0.0, color=GRAY, lw=0.6, ls=":")
ax.set_xlabel("$x$")
ax.set_ylabel("密度")
ax.set_xlim(-2, 2)
ax.set_ylim(0, 3.9)
ax.set_yticks([])
ax.set_xticks([-2, -1, 0, 1, 2])
ax.legend(loc="upper right", fontsize=7.4, handlelength=1.6, borderaxespad=0.2)
ax.annotate("模型把质量堆在这里，\n数据在这里是谷", (0.0, 0.30), xytext=(-1.92, 2.72),
            fontsize=7.5, color=RED, linespacing=1.7, va="top",
            arrowprops=dict(arrowstyle="-", color=RED, lw=0.6))
style(ax, spines=("top", "right"))

# ---------- 右：编码重叠与解码函数 ----------
ax = axes[1]
zs = 0.45 * np.where(label == 0, -1.0, 1.0) + rng.normal(0, 0.40, NDATA)
for lab, c in [(0, BLUE), (1, SAND)]:
    sel = label == lab
    ax.scatter(zs[sel], xs[sel], s=2.6, color=c, alpha=0.55, lw=0)

# 用分箱均值近似最小二乘回归得到的解码函数
bins = np.linspace(-1.5, 1.5, 19)
idx = np.digitize(zs, bins) - 1
cz, cx = [], []
for i in range(len(bins) - 1):
    sel = idx == i
    if sel.sum() > 8:
        cz.append(zs[sel].mean())
        cx.append(xs[sel].mean())
ax.plot(cz, cx, color=INK, lw=1.6, zorder=5)
ax.axhline(0.0, color=RED, lw=0.8, ls=(0, (4, 3)))
ax.axvspan(-0.28, 0.28, color=LIGHT, alpha=0.55, lw=0, zorder=0)
ax.text(0.0, -1.68, "两类共用的 $z$ 区间", fontsize=7.3, color=GRAY, ha="center",
        va="bottom")
ax.plot([0.0], [0.0], "o", ms=5, color=RED, zorder=6)
ax.text(0.16, -0.44, "$g$ 取两簇中间的值", fontsize=7.5, color=RED, va="center", ha="left")
ax.annotate("$g(z)$", (1.02, 1.02), xytext=(1.12, 1.42), fontsize=8.0, color=INK,
            arrowprops=dict(arrowstyle="-", color=GRAY, lw=0.6))
ax.set_xlabel("$z$")
ax.set_ylabel("$x$")
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.85, 1.75)
ax.set_xticks([-1, 0, 1])
ax.set_yticks([-1, 0, 1])
style(ax, spines=("top", "right"))

save(fig, "fig04_gap", CH)
