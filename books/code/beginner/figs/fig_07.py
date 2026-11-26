import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np

CH = "07"

T = 1000
beta = np.linspace(1e-4, 0.02, T)
alpha = 1 - beta
abar = np.cumprod(alpha)
abar_prev = np.concatenate([[1.0], abar[:-1]])
# 变分下界给出的每步权重，t = 2..T（t = 1 处 1 - abar_0 = 0，单独处理）
w = beta / (2 * alpha * (1 - abar_prev))
t = np.arange(2, T + 1)
w = w[1:]

i = np.argmin(w)
print("w 范围 %.4f (t=%d) ~ %.4f (t=%d)，比值 %.0f" % (w.min(), t[i], w.max(), t[-1], w.max() / w.min()))

fig, axes = plt.subplots(1, 2, figsize=(W_FULL, 2.25), gridspec_kw=dict(wspace=0.3))
ax = axes[0]
ax.semilogy(t, w, color=BLUE, lw=1.4)
ax.set_xlabel("$t$")
ax.set_ylabel("权重 $w_t$")
ax.set_yticks([0.005, 0.01, 0.05, 0.1, 0.5])
ax.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
ax.get_yaxis().set_minor_formatter(matplotlib.ticker.NullFormatter())
ax.set_ylim(0.004, 0.8)
style(ax, spines=("top", "right"))

ax = axes[1]
ax.semilogy(t, w / w.mean(), color=BLUE, lw=1.4, label="下界权重")
ax.axhline(1.0, color=RED, lw=1.1, ls=(0, (4, 3)), label="等权重")
ax.set_xlabel("$t$")
ax.set_ylabel("相对权重")
ax.set_yticks([0.5, 1, 5, 10, 50, 100])
ax.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
ax.get_yaxis().set_minor_formatter(matplotlib.ticker.NullFormatter())
ax.set_ylim(0.4, 150)
ax.legend(loc="upper right", fontsize=7.8)
style(ax, spines=("top", "right"))
save(fig, "fig07_weight", CH)
