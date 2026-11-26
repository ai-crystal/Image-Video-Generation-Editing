import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np
from scipy.stats import norm

CH = "06"

T = 1000
beta = np.linspace(1e-4, 0.02, T)
abar = np.cumprod(1 - beta)

x0 = 0.6
fig, axes = plt.subplots(1, 2, figsize=(W_FULL, 2.05), gridspec_kw=dict(wspace=0.28))

for ax, t in zip(axes, [20, 700]):
    i = t - 1
    a_t, b_t = 1 - beta[i], beta[i]
    at, ap = abar[i], abar[i - 1]
    xt = np.sqrt(at) * x0 + np.sqrt(1 - at) * 1.0      # 取一份具体噪声 eps = 1
    # 先验 q(x_{t-1}|x0)
    m_p, s_p = np.sqrt(ap) * x0, np.sqrt(1 - ap)
    # 似然（看作 x_{t-1} 的函数）q(x_t|x_{t-1})
    m_l, s_l = xt / np.sqrt(a_t), np.sqrt(b_t / a_t)
    # 后验
    c1 = np.sqrt(ap) * b_t / (1 - at)
    c2 = np.sqrt(a_t) * (1 - ap) / (1 - at)
    m_q, s_q = c1 * x0 + c2 * xt, np.sqrt(b_t * (1 - ap) / (1 - at))

    lo = min(m_p - 3.2 * s_p, m_l - 3.2 * s_l)
    hi = max(m_p + 3.2 * s_p, m_l + 3.2 * s_l)
    g = np.linspace(lo, hi, 700)
    ax.plot(g, norm.pdf(g, m_p, s_p), color=GRAY, lw=1.2, ls=(0, (4, 3)),
            label="$q(x_{t-1}\\mid x_0)$")
    ax.plot(g, norm.pdf(g, m_l, s_l), color=RED, lw=1.2, label="$q(x_t\\mid x_{t-1})$")
    ax.fill_between(g, norm.pdf(g, m_q, s_q), color=BLUE, alpha=0.22, lw=0)
    ax.plot(g, norm.pdf(g, m_q, s_q), color=BLUE, lw=1.5, label="后验")
    ax.axvline(x0, color=GREEN, lw=0.8, ls=(0, (1, 2)))
    ax.text(x0 - 0.02 * (hi - lo), ax.get_ylim()[1] * 0.50, "$x_0$", color=GREEN,
            fontsize=8.0, ha="right", va="center")
    ax.text(0.97, 0.92, "$t=%d$" % t, transform=ax.transAxes, ha="right",
            fontsize=8.4, color=INK)
    ax.set_xlabel("$x_{t-1}$")
    ax.set_yticks([])
    style(ax)
axes[0].set_ylabel("密度")
axes[0].legend(loc="upper left", fontsize=7.4)
save(fig, "fig06_posterior", CH)
