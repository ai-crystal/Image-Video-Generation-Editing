import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np

CH = "16"

# 注意力开销：全注意力 ~ L^2，窗口 w 的滑动注意力 ~ L*w
L = np.logspace(3, 5, 200)
w = 1024
full = L ** 2
win = L * w

fig, ax = plt.subplots(figsize=(W_FULL * 0.9, 2.3))
ax.plot(L, full, color=BLUE, lw=1.6, label="全注意力 $\\propto L^2$")
ax.plot(L, win, color=SAND, lw=1.6, label="窗口 $w=1024$ 的滑动注意力 $\\propto Lw$")
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlabel("序列长度 $L$（token）")
ax.set_ylabel("位置对个数（对数）")
ax.set_xlim(1e3, 1e5)
ax.set_ylim(1e5, 2e10)
ax.annotate("", xy=(1e5, full[-1]), xytext=(1e5, win[-1]),
            arrowprops=dict(arrowstyle="<|-|>", color=GRAY, lw=0.8))
ax.text(7.2e4, 3e8, "约 100 倍", fontsize=7.4, color=GRAY, ha="center")
ax.legend(loc="upper left", handlelength=1.8, borderaxespad=0.3)
style(ax, spines=("top", "right"))
save(fig, "fig16_window", CH)
