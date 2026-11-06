# A.2.3 课程覆盖表

| 节 | 原文 | 课 |
|---|---|---|
| 1.1 | Perceptrons | `neuron` |
| 1.2 | Sigmoid neurons | `neuron` |
| 1.3 | The architecture of neural networks | `layers` |
| 1.4 | A simple network to classify handwritten digits | `layers` |
| 1.5 | Learning with gradient descent | `train` |
| 1.6 | Implementing our network to classify digits | `layers` |
| 1.7 | Toward deep learning | `layers` |
| 2.1 | Warm up: a fast matrix-based approach to computing the output from a neural network | `backward` |
| 2.2 | The two assumptions we need about the cost function | `backward` |
| 2.3 | The Hadamard product, s ⊙ t | `backward` |
| 2.4 | The four fundamental equations behind backpropagation | `backward` |
| 2.5 | Proof of the four fundamental equations (optional) | `backward` |
| 2.6 | The backpropagation algorithm | `torch-loop` |
| 2.7 | The code for backpropagation | `torch-loop` |
| 2.8 | In what sense is backpropagation a fast algorithm? | `torch-loop` |
| 2.9 | Backpropagation: the big picture | `backward` |
| 3.1 | The cross-entropy cost function | `train` |
| 3.2 | Overfitting and regularization | `regularize` |
| 3.3 | Weight initialization | `deep-train` |
| 3.4 | Handwriting recognition revisited: the code | `regularize` |
| 3.5 | How to choose a neural network's hyper-parameters? | `deep-train` |
| 3.6 | Other techniques | `regularize` |
| 4.1 | Two caveats | `deep-features` |
| 4.2 | Universality with one input and one output | `deep-features` |
| 4.3 | Many input variables | `deep-features` |
| 4.4 | Extension beyond sigmoid neurons | `deep-features` |
| 4.5 | Fixing up the step functions | `deep-features` |
| 4.6 | Conclusion | `deep-features` |
| 5.1 | The vanishing gradient problem | `deep-train` |
| 5.2 | What's causing the vanishing gradient problem? Unstable gradients in deep neural nets | `deep-train` |
| 5.3 | Unstable gradients in more complex networks | `deep-train` |
| 5.4 | Other obstacles to deep learning | `deep-train` |
| 6.1 | Introducing convolutional networks | `deep-features` |
| 6.2 | Convolutional neural networks in practice | `deep-features` |
| 6.3 | The code for our convolutional networks | `deep-features` |
| 6.4 | Recent progress in image recognition | `deep-features` |
| 6.5 | Other approaches to deep neural nets | `deep-features` |

## 核心主题、综合练习与后继技能

CS2023 的基本神经网络、训练和表示分别见 `neuron` / `layers`、`train` / `deep-train` / `backward`、`deep-features`。原综合练习的前后向、初始化、正则化、优化器和 PyTorch 循环分别见 `backward`、`deep-train`、`regularize`、`train`、`torch-loop`。依据 [Nielsen 教材](https://neuralnetworksanddeeplearning.com/) 和 [PyTorch 训练循环教程](https://docs.pytorch.org/tutorials/beginner/basics/optimization_tutorial.html)。
