import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np

CH = "12"

# 全自注意力的配对数：token 数 N = T * (R/8)^2，每个 token 与所有 token 配对，共 N^2 次
res = np.array([512, 640, 768, 1024, 1280, 1536], dtype=float)
Ts = [1, 16, 49]
colors = [BLUE_L, BLUE, RED]
labels = ["单帧", "$T=16$", "$T=49$"]

fig, ax = plt.subplots(figsize=(W_HALF, 2.15))
last = []
for T, col, lab in zip(Ts, colors, labels):
    tok = T * (res / 8.0) ** 2
    pairs = tok ** 2 / 1e9
    ax.plot(res, pairs, "-o", ms=3.2, lw=1.4, color=col)
    ax.text(1500, pairs[-1]*1.55, lab, fontsize=7.2, color=col, va="bottom", ha="right")

ax.axhspan(1e3, 3e4, color=LIGHT, alpha=0.5, lw=0)
ax.text(520, 5.5e3, "整段全注意力\n不现实（量级估计）", fontsize=6.6, color=GRAY,
        va="center", linespacing=1.5)

ax.set_xscale("log", base=2)
ax.set_yscale("log")
ax.set_xlabel("边长 $R$（像素）")
ax.set_ylabel(r"配对数（$\times 10^9$）")
ax.set_xticks([512, 768, 1024, 1536])
ax.set_xticklabels(["512", "768", "1024", "1536"])
ax.set_xlim(480, 2300)
ax.set_ylim(1e-2, 3e4)
style(ax, grid=True)
save(fig, "fig12_scale", CH)
