import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np

CH = "09"

T = 1000
t = np.arange(T)
beta = (np.sqrt(0.00085) + (np.sqrt(0.012) - np.sqrt(0.00085)) * t / (T - 1)) ** 2
abar = np.cumprod(1 - beta)
sa = np.sqrt(abar)

# 平移再缩放：终点归零，起点保持不变
sa_fix = (sa - sa[-1]) * sa[0] / (sa[0] - sa[-1])

fig, ax = plt.subplots(figsize=(W_FULL * 0.78, 2.3))
ax.fill_between(t, sa_fix, sa, where=sa > sa_fix, color=RED, alpha=0.10, lw=0)
ax.plot(t, sa, color=BLUE, lw=1.5, label="修正前")
ax.plot(t, sa_fix, color=RED, lw=1.5, ls=(0, (5, 2)), label="修正后")

ax.text(690, 0.055, "末端 %.3f → 0" % sa[-1], fontsize=8.0, color=RED)
ax.text(120, 0.30, "阴影为被压缩的部分", fontsize=7.8, color=GRAY)

ax.set_xlabel("训练步 $t$")
ax.set_ylabel("$\\sqrt{\\bar\\alpha_t}$")
ax.set_xlim(0, T)
ax.set_ylim(0, 1.05)
ax.legend(loc="upper right", fontsize=8.0)
style(ax, grid=True)

save(fig, "fig09_terminal", CH)
