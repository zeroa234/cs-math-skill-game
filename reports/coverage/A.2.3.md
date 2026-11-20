# A.2.3 深度学习：课程覆盖表

**状态（2026-11-20）：已定稿并核验（v2，按零基础与知识覆盖面标准）。** 依据 `../cs-math-skill-tree/output/outlines.json` 的 A.2.3 大纲（Michael Nielsen《Neural Networks and Deep Learning》第 1–6 章），并按主中文来源《动手学深度学习》中文版第 3–6、11 章及 PyTorch 官方训练循环教程安排章序与算例。全包共 11 课，覆盖全部 37 个大纲小节；30 项核对断言（含有限差分梯度检验与 PyTorch AST 语法检查）及全部 17 道数值题已由 `tests/content/A.2.3.verify.py` 独立核对通过。

| 节 | 原文 | 课 |
|---|---|---|
| 1.1 | Perceptrons | `perceptron-and-sigmoid-neuron` |
| 1.2 | Sigmoid neurons | `perceptron-and-sigmoid-neuron` |
| 1.3 | The architecture of neural networks | `mlp-architecture-and-digits` |
| 1.4 | A simple network to classify handwritten digits | `mlp-architecture-and-digits` |
| 1.5 | Learning with gradient descent | `loss-sgd-and-minibatch` |
| 1.6 | Implementing our network to classify digits | `mlp-architecture-and-digits` |
| 1.7 | Toward deep learning | `mlp-architecture-and-digits` |
| 2.1 | Warm up: a fast matrix-based approach to computing the output from a neural network | `backprop-computation-graph` |
| 2.2 | The two assumptions we need about the cost function | `backprop-computation-graph` |
| 2.3 | The Hadamard product, s ⊙ t | `backprop-computation-graph` |
| 2.4 | The four fundamental equations behind backpropagation | `backprop-four-equations` |
| 2.5 | Proof of the four fundamental equations (optional) | `backprop-four-equations` |
| 2.6 | The backpropagation algorithm | `backprop-speed-and-pytorch-loop` |
| 2.7 | The code for backpropagation | `backprop-speed-and-pytorch-loop` |
| 2.8 | In what sense is backpropagation a fast algorithm? | `backprop-speed-and-pytorch-loop` |
| 2.9 | Backpropagation: the big picture | `backprop-computation-graph` |
| 3.1 | The cross-entropy cost function | `loss-sgd-and-minibatch` |
| 3.2 | Overfitting and regularization | `regularization-dropout-batchnorm` |
| 3.3 | Weight initialization | `initialization-hyperparams-vanishing` |
| 3.4 | Handwriting recognition revisited: the code | `regularization-dropout-batchnorm` |
| 3.5 | How to choose a neural network's hyper-parameters? | `initialization-hyperparams-vanishing` |
| 3.6 | Other techniques | `regularization-dropout-batchnorm` |
| 4.1 | Two caveats | `universal-approximation` |
| 4.2 | Universality with one input and one output | `universal-approximation` |
| 4.3 | Many input variables | `universal-approximation` |
| 4.4 | Extension beyond sigmoid neurons | `universal-approximation` |
| 4.5 | Fixing up the step functions | `universal-approximation` |
| 4.6 | Conclusion | `universal-approximation` |
| 5.1 | The vanishing gradient problem | `initialization-hyperparams-vanishing` |
| 5.2 | What's causing the vanishing gradient problem? Unstable gradients in deep neural nets | `initialization-hyperparams-vanishing` |
| 5.3 | Unstable gradients in more complex networks | `initialization-hyperparams-vanishing` |
| 5.4 | Other obstacles to deep learning | `initialization-hyperparams-vanishing` |
| 6.1 | Introducing convolutional networks | `cnn-deep-representations` |
| 6.2 | Convolutional neural networks in practice | `cnn-deep-representations` |
| 6.3 | The code for our convolutional networks | `cnn-deep-representations` |
| 6.4 | Recent progress in image recognition | `cnn-deep-representations` |
| 6.5 | Other approaches to deep neural nets | `cnn-deep-representations` |

## 写法上的取舍

- 按照技能树依据《动手学深度学习》调整后的四章顺序组织教学：第 1 章「神经网络」（`perceptron-and-sigmoid-neuron`、`mlp-architecture-and-digits`）、第 2 章「训练」（`loss-sgd-and-minibatch`、`optimizers-momentum-adam`、`initialization-hyperparams-vanishing`）、第 3 章「正则化和深层表示」（`regularization-dropout-batchnorm`、`universal-approximation`、`cnn-deep-representations`）、第 4 章「反向传播」（`backprop-computation-graph`、`backprop-four-equations`、`backprop-speed-and-pytorch-loop`）。
- 由于「训练」与「正则化和深层表示」排在「反向传播」之前，第 2–3 章从激活函数与链式直觉解释小批量 SGD、动量/Adam、梯度消失与 He 初始化、Dropout/批归一化以及深层特征层级；第 4 章再严密推通计算图、Hadamard 积、反向传播四大基本方程、O(W) 复杂度优势及 PyTorch `optimizer.zero_grad()` 标准循环。这样在满足零基础 B1 顺序的同时完整落实全部章序。
- 恢复游戏实验室内的两大深度学习互动组件：`perceptron-and-sigmoid-neuron` 提供单神经元 AND 线性分类实验与 XOR 不可分探究；`mlp-architecture-and-digits` 提供隐藏层神经元数量可调的小型神经网络圆形边界实验；`backprop-speed-and-pytorch-loop` 加入标量前/反向手写自动求导链的 Python `trace` 追迹。

## 核心主题（C2）

`../cs-math-skill-tree/data/curation/scope.json` 列入的 A.2.3 CS2023 主题：

| 知识点 | CS2023 原文 | 课 |
|---|---|---|
| 神经网络与前向结构 | Basic neural networks | `perceptron-and-sigmoid-neuron`、`mlp-architecture-and-digits` |
| 训练与反向传播 | Training process | `loss-sgd-and-minibatch`、`optimizers-momentum-adam`、`initialization-hyperparams-vanishing`、`backprop-computation-graph`、`backprop-four-equations`、`backprop-speed-and-pytorch-loop` |
| 深层表示与正则化 | Visualization of learned feature representations from deep nets | `regularization-dropout-batchnorm`、`universal-approximation`、`cnn-deep-representations` |

## 学习资源的章节（C3）

- Michael Nielsen [Neural Networks and Deep Learning](https://neuralnetworksanddeeplearning.com/) 第 1–6 章：全 37 个小节均已一对一归课（见上表）。
- 《动手学深度学习》中文版 第 3–6 章（线性/多层感知机、前向/反向传播计算图、权重衰减与暂退法、卷积基础）及第 11 章（动量 SGD、Adam 优化器）：融入各章对应课目。
- [PyTorch 训练循环官方教程](https://docs.pytorch.org/tutorials/beginner/basics/optimization_tutorial.html)：`backprop-speed-and-pytorch-loop`。

## 综合练习（C4）

| 小题 | 内容 | 课 |
|---|---|---|
| (1) | 两层 ReLU 网络 `x=(1,2), y=1` 的手算前向传播（$\hat{y}=-4.5, L=15.125$）与反向传播各参数梯度 | `backprop-four-equations` |
| (2) | 深层网络普遍采用 ReLU 而非 Sigmoid 的原因，以及 He 初始化方差取 $2/n_{\text{in}}$ 的方差推导 | `initialization-hyperparams-vanishing` |
| (3) | Dropout、权重衰减、早停、批归一化各自解决的问题 | `regularization-dropout-batchnorm` |
| (4) | 带动量 SGD 与 Adam 更新公式及学习率过大/过小症状 | `optimizers-momentum-adam` |
| (5) | PyTorch MLP 分类器训练循环五步骨架及每次迭代前调用 `optimizer.zero_grad()` 的原因 | `backprop-speed-and-pytorch-loop` |

## 后继技能（C5）

- **A.2.3.1 网络架构与表示学习**：在 `mlp-architecture-and-digits`、`regularization-dropout-batchnorm`（批归一化）与 `cnn-deep-representations`（局部连接/卷积/池化/残差层级特征）建立坚实的前向、归一化与深层表示基础。
- **A.2.3.2 深度模型训练与推理系统** 与 **A.3.5 生成式 AI**：依赖小批量 SGD、动量/Adam 优化器、反向传播梯度图与 PyTorch 标准训练步（`zero_grad` / `backward` / `step`），均已在第 2、4 章完整展开。
