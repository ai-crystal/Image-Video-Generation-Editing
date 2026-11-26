import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np

CH = "07"

T = 1000
beta = np.linspace(1e-4, 0.02, T)
abar = np.cumprod(1 - beta)
t = np.arange(1, T + 1)

# 预测误差 delta 传回 x0 时的放大系数
amp_eps = np.sqrt((1 - abar) / abar)
amp_x0 = np.ones_like(abar)
amp_v = np.sqrt(1 - abar)

for tt in [100, 500, 900, 1000]:
    print("t=%4d  eps %.2f  x0 %.2f  v %.3f" % (tt, amp_eps[tt - 1], 1.0, amp_v[tt - 1]))

fig, ax = plt.subplots(figsize=(W_FULL * 0.8, 2.25))
ax.semilogy(t, amp_eps, color=BLUE, lw=1.5, label=r"$\epsilon$ 参数化")
ax.semilogy(t, amp_x0, color=GRAY, lw=1.2, ls=(0, (5, 3)), label="$x_0$ 参数化")
ax.semilogy(t, amp_v, color=RED, lw=1.5, label="$v$ 参数化")
ax.set_xlabel("$t$")
ax.set_ylabel("误差放大系数")
ax.set_yticks([0.1, 1, 10, 100])
ax.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
ax.get_yaxis().set_minor_formatter(matplotlib.ticker.NullFormatter())
ax.set_ylim(0.05, 250)
ax.legend(loc="upper left", fontsize=7.8)
style(ax, spines=("top", "right"))
save(fig, "fig07_param", CH)
