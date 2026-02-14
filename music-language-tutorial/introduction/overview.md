# 教程概览

本教程将介绍随着语言模型的发展，音乐理解、检索和生成技术所发生的变化。

```{figure} ./img/flow.png
---
name: scope
---
音乐与语言模型发展的示意图。
```

## 语言模型

第2章介绍了语言模型（Language Models, LMs），它们对于使机器理解自然语言及其广泛应用至关重要。本章追溯了从简单的 one-hot 编码和词嵌入（word embedding）到更高级语言模型的发展历程，包括掩码语言模型（masked language model）{cite}`devlin2018bert`、自回归语言模型（auto-regressive language model）{cite}`radford2019language` 以及编码器-解码器语言模型（encoder-decoder language model）{cite}`raffel2020exploring`，进而发展到前沿的指令跟随（instruction-following）{cite}`wei2021finetuned` {cite}`ouyang2022training` {cite}`chung2024scaling` 和大语言模型（large language models）{cite}`achiam2023gpt`。此外，我们还回顾了语言模型的组成部分和条件方法，并探讨了将语言模型作为框架使用时面临的挑战和潜在的解决方案。


## 音乐描述

```{figure} ./img/annotation.png
---
name: annotation
---
```

第3章深入探讨了音乐标注作为增强音乐理解的工具。本章首先定义了任务和问题形式化，从基础的分类 {cite}`turnbull2008semantic` {cite}`nam2018deep` 过渡到更复杂的语言解码任务。接着，本章进一步探索了编码器-解码器模型 {cite}`manco2021muscaps` {cite}`doh2023lp` 以及多模态大语言模型（LLMs）在音乐理解中的作用 {cite}`gardner2023llark`。本章探讨了从"针对特定任务的分类模型"到"使用多样化自然语言监督训练的更通用的多任务模型"的演变过程。


## 音乐检索

```{figure} ./img/retrieval.png
---
name: retrieval
---
```

第4章聚焦于文本到音乐的检索（text-to-music retrieval），这是音乐搜索的关键组成部分，详细介绍了该任务的定义和各种搜索方法。内容涵盖从基本的布尔搜索和向量搜索到通过联合嵌入方法（joint embedding）{cite}`choi2019zero` 将词语与音乐连接起来的高级技术，解决了词汇表外（out-of-vocabulary）等问题。本章进一步发展到句子到音乐的检索 {cite}`huang2022mulan` {cite}`manco2022contrastive` {cite}`doh2023toward`，探索如何整合复杂的音乐语义，以及基于多轮对话的会话式音乐检索 {cite}`chaganty2023beyond`。本章介绍了评估指标，并包含开发基本联合嵌入模型用于音乐搜索的实践编程练习。本章的核心是模型如何以各种方式响应"用户的音乐查询"。


## 音乐生成

```{figure} ./img/generation.png
---
name: generation
---
```

第5章深入探讨了通过文本到音乐生成（text-to-music generation）技术创作新音乐的方法，重点介绍了在文本提示影响下产生新声音的过程 {cite}`dhariwal2020jukebox`。本章介绍了无条件音乐生成的概念，并详细说明了在训练阶段融入文本线索的方法。讨论内容包括相关数据集的概述以及基于听觉质量和文本相关性的音乐评估。本章比较了不同的音乐生成方法，包括扩散模型（diffusion models）{cite}`chen2023musicldm` 和离散编解码器语言模型（discrete codec language models）{cite}`agostinelli2023musiclm` {cite}`copet2024simple`。此外，本章还探讨了纯文本驱动生成面临的挑战，并研究了超越文本的替代条件生成方法，例如将文本描述转换为音乐属性 {cite}`wu2023music` {cite}`novack2024ditto`。


## 参考文献

```{bibliography}
:filter: docname in docnames
```
