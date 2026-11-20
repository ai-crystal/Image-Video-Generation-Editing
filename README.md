# 图像生成与编辑技术

**三册：从图像与视频的生成，到流模型与一步生成，再到图像与视频编辑**

作者：Dr. Dezeming ｜ 2026

这套书讲同一件事的不同层面：怎样让机器凭空造出图像与视频，怎样把采样压到一步，以及怎样在已有的图像或视频上按要求改。

## 分册

| 册 | 内容 | 页数 | 阅读 | 下载 |
| --- | --- | --- | --- | --- |
| 入门篇 | 图像、视频与编辑的全景（25 章） | 115 | [在线阅读](books/beginner/README.md) | [PDF](output/generative-models-01-beginner.pdf) |
| 进阶篇 | 流模型与一步生成（含视频） | 53 | [在线阅读](books/advanced/README.md) | [PDF](output/generative-models-02-advanced.pdf) |
| 深入篇 | 图像与视频编辑的原理 | 52 | [在线阅读](books/editing/README.md) | [PDF](output/generative-models-03-editing.pdf) |

三册各自独立，可以按顺序读，也可以挑着读。

入门篇是一张全景图：从变分自编码器、对抗网络、扩散模型讲到流模型与一步生成，再讲到视频生成（时空 U-Net、时间层、3D VAE、长视频）与图像/视频编辑（注意力编辑、ControlNet、EDICT、FlowEdit、ChordEdit、TokenFlow）。目标是让外行能纵览全貌。

进阶篇换一套语言：把生成写成一条从噪声到数据的路径，用速度场描述它。从连续归一化流、流匹配讲到整流流与随机插值，后半部分处理一步生成：一致性模型、分布匹配蒸馏、MeanFlow，以及视频上的一步生成。

深入篇讲编辑。从保真与对齐的权衡开始，经过潜空间、噪声注入、注意力操作、结构条件、精确反演，落到 RF-Inversion、FlowEdit 与 ChordEdit；后半部分讲视频编辑：对应关系、传播、形变场与整体生成。

## 怎么读

入门篇：第 1 章是全景，先读它建立地图；第 3 章补数学。关心生成的读第 4 到 11 章，关心视频的读第 12 到 16 章，关心编辑的读第 19 到 24 章。

进阶篇：第 1 到第 3 章是地基，讲路径与速度场；第 4 到第 6 章是对照与统一；第 7 到第 12 章讲一步生成与视频。

深入篇：第 1 章建立语言，第 2 到第 5 章按"改哪里"分类，第 6 到第 8 章讲流模型上的编辑，第 9、10 章讲视频编辑，第 11、12 章讲边界与工程。

## 仓库说明

- `books/<册名>/chapters/` 是正文，Markdown 写成，图片用相对路径，GitHub 网页端可以直接读。
- `books/code/<册名>/figs/` 是绘图脚本，所有插图由代码生成，可以自己运行、修改。
- `output/` 放各册 PDF，每册都控制在 20 MB 以内。
- 在线阅读站点用 docsify 搭建，根目录的 `index.html` 是入口，每章有独立链接。
- 写作规范、草稿与参考资料不在仓库里。

## 编译

```text
build.bat                 构建全部册
build.bat beginner        只构建某一册（beginner / advanced / editing）
build-beginner.bat        只构建入门篇
build.bat figures         重画全部插图后再构建
```
