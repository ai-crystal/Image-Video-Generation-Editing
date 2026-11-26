import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.figstyle import *
import numpy as np

CH = "03"

# ---------- 图 3.2 按掩码混合注意力 ----------
g = 16  # 注意力图分辨率（对应 512 图像的 32 倍下采样）
rng = np.random.default_rng(7)
yy, xx = np.mgrid[0:g, 0:g] / (g - 1.0)

# 图像特征：一个物体分量 + 一个天空分量 + 噪声
obj = np.exp(-((yy - 0.55) ** 2 / (2 * 0.15 ** 2) + (xx - 0.45) ** 2 / (2 * 0.12 ** 2)))
sky = np.exp(-((yy - 0.10) ** 2 / (2 * 0.10 ** 2)))

d = 8
q = np.zeros((g * g, d))
q[:, 0] = obj.ravel()
q[:, 1] = sky.ravel()
q[:, 2] = yy.ravel() - 0.5      # 粗位置通道
q[:, 3] = xx.ravel() - 0.5
q[:, 4:] = 0.25 * rng.standard_normal((g * g, d - 4))


def keys(w_obj, w_pos):
    k = np.zeros((5, d))
    k[0, 4] = 1.0               # 冠词，几乎均匀
    k[1, 0] = w_obj             # 物体词
    k[1, 2] = w_pos             # 物体词对垂直位置的偏好
    k[3, 0] = 0.45
    k[4, 1] = 2.2               # 天空词
    return k


def softmax(z):
    e = np.exp(z - z.max(axis=1, keepdims=True))
    return e / e.sum(axis=1, keepdims=True)


TMP = 6.0
A_s = softmax(q @ keys(1.7, 0.0).T / np.sqrt(d) * TMP)[:, 1].reshape(g, g)
A_t = softmax(q @ keys(0.95, 1.4).T / np.sqrt(d) * TMP)[:, 1].reshape(g, g)

# 像素级椭圆掩码，8 倍平均池化到注意力分辨率
P = 128
py, px = np.mgrid[0:P, 0:P] / (P - 1.0)
m_px = (((px - 0.45) / 0.24) ** 2 + ((py - 0.62) / 0.26) ** 2 < 1).astype(float)
M = m_px.reshape(g, 8, g, 8).mean(axis=(1, 3))
A_mix = M * A_t + (1 - M) * A_s
frac = int(((M > 0) & (M < 1)).sum())
print("覆盖率 %.3f  边界格 %d / %d  A_s 峰 %.3f  A_t 峰 %.3f  混合峰 %.3f"
      % (M.mean(), frac, g * g, A_s.max(), A_t.max(), A_mix.max()))

fig, axes = plt.subplots(1, 3, figsize=(W_FULL, 1.72), gridspec_kw=dict(wspace=0.06))
for ax, im in zip(axes, [A_s, A_t, A_mix]):
    ax.imshow(im, cmap="Blues", vmin=0, vmax=A_s.max(), interpolation="nearest")
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_color(LIGHT)
axes[0].set_xlabel("源 prompt 中“猫”", fontsize=8.2)
axes[1].set_xlabel("目标 prompt 中“狗”", fontsize=8.2)
axes[2].set_xlabel("按掩码混合", fontsize=8.2)
axes[2].contour(M, levels=[0.5], colors=[RED], linewidths=0.9)
axes[2].contour(M, levels=[0.02, 0.98], colors=[SAND], linewidths=0.7, linestyles="dashed")
save(fig, "fig03_mask", CH)

# ---------- 图 3.2 反演误差的单步传递系数 ----------
T = 1000
abar = np.cumprod(1 - np.linspace(1e-4, 0.02, T))
N = 50
ts = np.linspace(T - 2, 0, N).astype(int)

tt, c, tay = [], [], []
for i in range(len(ts) - 1):
    a0, a1 = abar[ts[i]], abar[ts[i + 1]]
    rr = np.sqrt(a1 / a0)
    c.append(np.sqrt(1 - a1) - rr * np.sqrt(1 - a0))
    tay.append(-(a1 - a0) / (2 * a0 * np.sqrt(1 - a0)))
    tt.append(ts[i])
tt, c, tay = np.array(tt), np.array(c), np.array(tay)
c, tay, tt = -c, -tay, tt
print("|c|: max %.3f at t=%d, min %.3f at t=%d, sum %.2f, sqrt(sum c2) %.2f"
      % (c.max(), tt[c.argmax()], c.min(), tt[c.argmin()], c.sum(), np.sqrt((c ** 2).sum())))

fig, ax = plt.subplots(figsize=(W_FULL * 0.86, 2.15))
ax.plot(tt, c, "o-", color=BLUE, ms=2.6, lw=1.1, label="直接按定义算")
ax.plot(tt, tay, lw=1.0, color=SAND, ls="dashed", label="一阶近似")
ax.text(330, 0.248, r"$t$ 越大、$\bar\alpha_t$ 越小，偏差被 $1/\sqrt{\bar\alpha_t}$ 放大",
        fontsize=7.4, color=RED)
ax.set_xlabel("反演所在的步（$t$）")
ax.set_ylabel("单步传递系数 $|c_t|$")
ax.set_xlim(-30, T + 30)
ax.set_ylim(0, 0.285)
ax.set_xticks([0, 250, 500, 750, 1000])
ax.legend(loc="upper left", fontsize=7.6)
style(ax, spines=("top", "right"))
save(fig, "fig03_inv", CH)
