# MusicGEN

在本节中，我们以 [MusicGEN](https://musicgen.com/) {cite}`copet2024simple` 为例，介绍通过 Transformer 架构 {cite}`Vaswani2017AttentionIA` 进行音乐生成的自回归建模方法。

## 神经音频编解码器

MusicGEN 是一个自回归的文本到音乐生成模型。MusicGEN 的输入利用 Encodec {cite}`DBLP:journals/tmlr/DefossezCSA23` 将音乐时域信号处理为离散 token，即神经音频编解码 token。

<center><img alt='generation_encodec' src='../_images/encodec.PNG' width='50%' ></center>

如上图所示，Encodec 架构在其编码器和解码器网络中分别使用一维卷积和一维反卷积模块。瓶颈模块采用多步残差向量量化（Residual Vector Quantization, RVQ）机制，将编码器输出的连续潜在音乐嵌入转换为离散音频 token。解码器的目标是从这些音频 token 重建输入的时域信号。重建过程通过多种不同的目标函数组合进行训练，包括时域信号的 L1 损失、梅尔频谱的 L1 损失、梅尔频谱的 L2 损失，以及使用多分辨率 STFT 判别器的对抗训练。

预训练的 Encodec 模型将音乐时域信号预处理为音频 token，作为 MusicGEN 模型输入的一部分。

## MusicGEN

MusicGEN 使用 Transformer 解码器架构，基于前面的音频 token 预测下一个音频 token，如以下概率函数所示：

<center><img alt='generation_musicgen_p1' src='../_images/musicgen_p1.PNG' width='50%' ></center>
训练目标为交叉熵损失：
<center><img alt='generation_musicgen_l1' src='../_images/musicgen_l1.PNG' width='50%' ></center>

<center><img alt='generation_musicgen_arch' src='../_images/musicgen_arch.PNG' width='50%' ></center>

在将文本融入音乐生成任务时，MusicGEN 采用两种方法将文本作为音乐生成目标的条件信息，如上图所示：

1. 时域拼接：利用 T5 模型生成的文本 token 作为前缀 token 置于音频 token 之前，作为条件机制。

2. Cross Attention（交叉注意力）：将文本 token 的 Keys 和 Values (K, V) 与音频 token 的 Queries (Q) 送入 MusicGEN 的交叉注意力模块。

新的概率函数表示为：
<center><img alt='generation_musicgen_p2' src='../_images/musicgen_p2.PNG' width='50%' ></center>



