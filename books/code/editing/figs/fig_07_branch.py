import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np

# 一维模型：v_c(z, t) = a(t)(z - mu_c) + gamma * f(z)，a(t) = 1 + t，mu_src = 0，mu_tar = 0.9
# 记 Y = Z_FE - x_src，则 V^Delta = a(Y - mu_tar + mu_src) + gamma * (f(z+Y) - f(z))
# gamma = 0 时 V^Delta 与噪声实现无关：噪声在一阶上抵消。
CH = "07"

x_src = 0.2
delta = 0.9
NSTEP = 600
tau = np.linspace(0.0, 1.0, NSTEP + 1)      # tau = 1 - t


def a_of(t):
    return 1.0 + t


def fc(z, gamma):
    return gamma * np.sin(1.7 * z)


def run(noise, gamma):
    """从 t = 1（tau = 0）积到 t = 0（tau = 1），返回 Y 与两条支路。"""
    dtau = 1.0 / NSTEP
    y = 0.0
    ys, srcs, tars = [], [], []
    for k in range(NSTEP + 1):
        tu = tau[k]
        t = 1.0 - tu
        z_src = (1 - t) * x_src + t * noise
        a = a_of(t)
        ys.append(y)
        srcs.append(z_src)
        tars.append(z_src + y)
        if k == NSTEP:
            break
        a2 = a_of(1.0 - (tu + dtau))
        v_delta = a * (y - delta) + fc(z_src + y, gamma) - fc(z_src, gamma)
        y = y + dtau * (-v_delta)
    return np.array(ys), np.array(srcs), np.array(tars)


noise1, noise2 = 1.85, -1.6
y1, s1, t1 = run(noise1, 0.0)
y2, s2, t2 = run(noise2, 0.0)

fig, axes = plt.subplots(1, 2, figsize=(W_FULL, 2.3), gridspec_kw=dict(wspace=0.34))

# ------------------ 左：三条曲线 ------------------
ax = axes[0]
ax.plot(tau, s1, color=BLUE_L, lw=1.5, label="源支路 $Z_t^{\\mathrm{src}}$")
ax.plot(tau, t1, color=SAND, lw=1.5, label="目标支路 $Z_t^{\\mathrm{tar}}$")
ax.plot(tau, x_src + y1, color=RED, lw=1.8, label="编辑路径 $Z_t^{\\mathrm{FE}}$")
ax.scatter([0], [noise1], s=24, color=INK, zorder=6)
ax.text(0.05, 1.52, "在 $t=1$ 重合", fontsize=7.0, color=INK)
ax.annotate("", xy=(0.93, x_src), xytext=(0.93, x_src + y1[-1]),
            arrowprops=dict(arrowstyle="<|-|>", color=GRAY, lw=0.7, mutation_scale=6))
ax.text(0.965, 0.62, "$\\Delta Y$", fontsize=7.4, color=GRAY, ha="right")
ax.axvline(1.0, color=LIGHT, lw=0.8, zorder=0)
ax.set_xlabel("进程 $\\tau = 1-t$")
ax.set_ylabel("状态值")
ax.set_xlim(-0.02, 1.12)
ax.set_ylim(0.0, 2.15)
ax.legend(loc="upper right", fontsize=6.9, handletextpad=0.4, borderpad=0.15,
          labelspacing=0.25)
style(ax, spines=("top", "right"))

# ------------------ 右：残差随非线性增强 ------------------
ax = axes[1]
for gamma, c in [(0.0, GRAY), (0.06, BLUE), (0.20, RED)]:
    ya, _, _ = run(noise1, gamma)
    yb, _, _ = run(noise2, gamma)
    ax.plot(tau, np.abs(ya - yb), color=c, lw=1.3, label="$\\gamma=%g$" % gamma)
ax.set_xlabel("进程 $\\tau = 1-t$")
ax.set_ylabel("两次噪声的编辑路径之差")
ax.set_xlim(0, 1)
ax.set_ylim(-0.01, 0.20)
ax.legend(loc="upper left", fontsize=7.4)
style(ax, spines=("top", "right"))

save(fig, "fig07_branch", CH)
