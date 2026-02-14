<div align="center">

# intro2musictech

公众号 **「无痛入门音乐科技」** 开源代码和相关资料链接

欢迎微信扫码关注或直接搜索 **intro2musictech**

<img src="attachment/qrcode.jpg" width="180">

*♬ 公众号文章同步更新 ipynb 代码 · 一边阅读一边执行 · 快速入门无痛 skr ♫*

</div>

## Quick Start

```bash
git clone https://github.com/beiciliang/intro2musictech.git
cd intro2musictech
uv sync                    # 自动安装 Python 和所有依赖
uv run jupyter notebook    # 启动 Jupyter Notebook
uv run marimo edit MIR-CC.py  # 启动 marimo 交互式笔记本
```

> 编程零基础？展开下方 [从零设置编程环境](#从零设置编程环境) 查看详细指南。

## 文章目录

| 日期 | 文章 | 代码 |
|:----:|------|------|
| 2018.07.27 | [「README」无痛入门音乐科技门槛须知](https://mp.weixin.qq.com/s/S8Q5iSUMgKZQ5g-17dF8UA) | — |
| 2018.07.28 | [「SETUP」从零设置编程环境](https://mp.weixin.qq.com/s/ngvmPl5S7QI-PqUUBtbQ3w) | [下方指南](#从零设置编程环境) · [00-Hello.ipynb](00-Hello.ipynb) |
| 2018.08.03 | [「NIME-01」那些为身障人士设计的乐器](https://mp.weixin.qq.com/s/vUU30Ap5ot-Ygpy8eBeC4w) | — |
| 2018.08.05 | [「MIR-01」要把音乐画出来，总共分几步？](https://mp.weixin.qq.com/s/pvpFoKKa0Ki_uZ3Y6rqaJw) | [MIR-01.ipynb](MIR-01.ipynb) |
| 2018.08.11 | [「NIME-02」日常物件在没有成精的前提下如何发声儿？](https://mp.weixin.qq.com/s/X05DgjhXO7oMf8Gej5P3Mw) | [The Bela Blog](http://blog.bela.io/) |
| 2018.08.18 | [「MIR-02_1」音频特征小全之概览](https://mp.weixin.qq.com/s/oFrW7hmZgmAuZGIVHjZTAQ) | [MIR-02_1.ipynb](MIR-02_1.ipynb) |
| 2018.08.22 | [「INFO」音乐科技相关科研组列表](https://mp.weixin.qq.com/s/2nDWikda9fh2x5o093F6HA) | [INFO-ResearchGroups.md](INFO-ResearchGroups.md) |
| 2018.08.27 | [「NIME-03」为什么说钢琴是乐器之王？复杂！](https://mp.weixin.qq.com/s?__biz=MzU5MzY3NzI0OA==&mid=2247483718&idx=1&sn=fbf3f7c11e61096bafd72ea6ed0c0e8a&scene=19#wechat_redirect) | [知乎问题](https://www.zhihu.com/question/288614974) |
| 2018.09.13 | [「MIR-02_2」音频特征小全之时域特征](https://mp.weixin.qq.com/s/fwbxA0ZWJPuOKolouQea3Q) | [MIR-02_2.ipynb](MIR-02_2.ipynb) |
| 2018.10.14 | [「MIR-02_3」音频特征小全之频域特征](https://mp.weixin.qq.com/s/TOAXROVlOVYDmVlmFIyBxQ) | [MIR-02_3.ipynb](MIR-02_3.ipynb) |
| 2018.11.24 | [「MIR-02_4」音频特征小全之乐音特征](https://mp.weixin.qq.com/s/XqZvZ4-m3xd81udyUSg4wg) | [MIR-02_4.ipynb](MIR-02_4.ipynb) |
| 2018.11.30 | [「INFO」音乐科技相关会议期刊列表](https://mp.weixin.qq.com/s?__biz=MzU5MzY3NzI0OA==&mid=2247483761&idx=1&sn=52b81b9fca161df1afad2a8babad251a&scene=19#wechat_redirect) | — |
| 2018.12.17 | [「INFO」2018年度那些亮眼的音乐科技成就](https://mp.weixin.qq.com/s/5FBzxHm1PcgBpHy6645JmA) | — |
| 2019.02.18 | [「INFO」C4DM在ICASSP 2019的收录成果](https://mp.weixin.qq.com/s/RkcOyFf4eLIe512B37nmIw) | — |
| 2019.08.19 | [「INFO」在C4DM读博是怎样一番体验？](https://mp.weixin.qq.com/s/N4p_jmsuY6RVuz1IjrSMeg) | — |
| 2019.11.13 | [「MIR-02_4」音频特征小全之提取工具](http://mp.weixin.qq.com/s?__biz=MzU5MzY3NzI0OA==&mid=2247483792&idx=1&sn=38b07d6efff4523eecd78366f3e87962&chksm=fe0d9f3fc97a1629669c5875ea33a3b43878a2859e71a052c7c38b212127fea936e935e79c75#rd) | — |
| 2020.01.12 | [「INFO」2019年度那些亮眼的音乐科技成就](http://mp.weixin.qq.com/s?__biz=MzU5MzY3NzI0OA==&mid=2247483802&idx=1&sn=9790d92e685baa74f28f3053c4ff15ef&chksm=fe0d9f35c97a1623fc305ce8c79b19e7451f5500d95b08c4fd5c27e47c8a256094c3e2022066#rd) | — |
| 2020.03.07 | [「MIR-03」听歌识曲: 音乐宇宙里的占星师](http://mp.weixin.qq.com/s?__biz=MzU5MzY3NzI0OA==&mid=2247483818&idx=1&sn=db17b69603b98532f993f7f094248ce3&chksm=fe0d9f05c97a16139ee4114ed6890c8d99bd2c09210aa7ba0d085a2f44599e5cbd5a93375290#rd) | [知乎系列文章](https://zhuanlan.zhihu.com/p/75360272) |
| 2020.03.14 | [「MIR-04」音乐推荐: 努力懂你的预言家](http://mp.weixin.qq.com/s?__biz=MzU5MzY3NzI0OA==&mid=2247483885&idx=1&sn=f9e4c9f71451575d1111e566943f4aff&chksm=fe0d9f42c97a16544b35edd490294e754e9e3cf48a13ca6585bcb7f58c02d0c1bf0222822793#rd) | — |
| 2020.03.20 | [「MIR-05_0」震惊! AI发现这些歌竟然...](http://mp.weixin.qq.com/s?__biz=MzU5MzY3NzI0OA==&mid=2247483898&idx=1&sn=3a405119a32714442c8dcd9be830cdb9&chksm=fe0d9f55c97a1643a091acb7d6c25c14a8d19d107f9d430ffd9055a468f4d18c43666b2c260f#rd) | — |
| 2020.04.30 | [「INFO」《音频音乐技术》正式出版](http://mp.weixin.qq.com/s?__biz=MzU5MzY3NzI0OA==&mid=2247483904&idx=1&sn=959fd70b768b9416a5065748ba6f5818&chksm=fe0d9cafc97a15b9c1123a30af34497d5e79e5b636a15a70ad169434ed5b0cf937f13ca87a7b#rd) | — |
| 2020.05.16 | [「说得好听」EP7-音乐推荐算法的小秘密](http://mp.weixin.qq.com/s?__biz=MzU5MzY3NzI0OA==&mid=2247483914&idx=1&sn=1a474f9bdfb1c7981a461151737bb5e0&chksm=fe0d9ca5c97a15b36c77c5879d916cb7f2a56c62741c3490dd1c18c5f638231452e9929e398f#rd) | [小宇宙播客](https://www.xiaoyuzhoufm.com/episode/5ebeec95418a84a0468f2ed5) |
| 2020.10.08 | [「MIR-05_1」音乐流派自动识别的前世今生](http://mp.weixin.qq.com/s?__biz=MzU5MzY3NzI0OA==&mid=2247483923&idx=1&sn=2fe1ad96ba0b764888f28fdd88ce9e36&chksm=fe0d9cbcc97a15aa70632d73d3d7cafbc63d97027d8a9d1ecd7fee20212649d6b1fbde37c90f#rd) | — |
| 2021.03.06 | [「INFO」2020年度那些亮眼的音乐科技成就](http://mp.weixin.qq.com/s?__biz=MzU5MzY3NzI0OA==&mid=2247483940&idx=1&sn=c6470c7b689da2882ee4fb6c43e1577c&chksm=fe0d9c8bc97a159d2c7734ab466b38d2d524f4e8e2ce87a2d54cf5303ae5c436eadbdd103b09#rd) | — |
| 2021.06.04 | [「MIR-05_2」当音乐标签化身为音频Embedding时能解决什么？](http://mp.weixin.qq.com/s?__biz=MzU5MzY3NzI0OA==&mid=2247483954&idx=1&sn=7bdcc70838c0fc3d014cdedec91411b2&chksm=fe0d9c9dc97a158b31d11ec699d6e5ab53caf1897431cdf2f20f73ab67d885790b4a9361f055#rd) | [arXiv论文](https://arxiv.org/abs/2010.15389) |
| 2021.08.06 | [「INFO」三分钟认识音乐科技](http://mp.weixin.qq.com/s?__biz=MzU5MzY3NzI0OA==&mid=2247483960&idx=1&sn=80ce28a10186dab81af2af239df76c8a&chksm=fe0d9c97c97a158114decdbdbe6cc6916c6c81f6fce9f9c52617fc6d0ea8738b9720efe8975a#rd) | [YouTube视频](https://www.youtube.com/watch?v=YgYV-7-ohxQ) |
| 2021.09.04 | [「MIR-06」打破砂锅问到底，不同python库做音频预处理的区别在哪里？](http://mp.weixin.qq.com/s?__biz=MzU5MzY3NzI0OA==&mid=2247483966&idx=1&sn=f968b4f55595357afa8f6d483715262d&chksm=fe0d9c91c97a1587f42ce8e52d3cd4eec9ba49cad01680aead1b60d0918c134340ce75e3c469#rd) | TBC |
| 2022.10.17 | [「INFO」从数据角度聊聊音乐版权版税](https://mp.weixin.qq.com/s?__biz=MzU5MzY3NzI0OA==&mid=2247483988&idx=1&sn=d5b6dfa1ab0e460f9abad915838f6e59&chksm=fe0d9cfbc97a15edff8b2f5ac49ca678350bc3af18d6558c6508499703e384f82bca36253ca8&scene=178&cur_album_id=1342444458121576448#rd) | — |
| 2023.03.26 | [「INFO」分享我的MIR研发技术栈](https://mp.weixin.qq.com/s?__biz=MzU5MzY3NzI0OA==&mid=2247483994&idx=1&sn=3dfeefafc11c264106f448379052b42d&chksm=fe0d9cf5c97a15e30a5338b9031ae1741ea45856d234dc02d13ecc7723b5682a747f9c00de31&scene=178&cur_album_id=1342444458121576448#rd) | [B站视频](https://www.bilibili.com/video/BV1MX4y1R7cu/?share_source=copy_web&vd_source=9a7c2143e3aca83788929d6099a36f8f) |
| 2026.02.14 | 「MIR-CC」2026年，用Claude Code就可以无痛入门音乐科技 | [MIR-CC.py](MIR-CC.py) · [在线预览](https://beiciliang.github.io/intro2musictech/) |
| 2026.02.14 | 「ISMIR-2024」连接音乐音频与自然语言（[英文原版](https://github.com/mulab-mir/music-language-tutorial)，[中文版](music-language-tutorial/intro.md)由 Claude Code 翻译） | [music-language-tutorial/](music-language-tutorial/) |

---

## 从零设置编程环境

<details>
<summary><b>展开查看完整指南</b>（适用于编程零基础的读者）</summary>

> 如果你已经清楚如何 `git clone` 本项目，并能用 [uv](https://docs.astral.sh/uv/) 安装 [pyproject.toml](pyproject.toml) 中的依赖之后，不报错地加载 [00-Hello.ipynb](00-Hello.ipynb) 并运行其中代码，恭喜你，编程环境配置成功！

### 目录

1. [命令行基础操作](#1-命令行)
2. [Git 用法](#2-git-用法)
3. [用 uv 设置环境](#3-用-uv-设置环境)
4. [用 Jupyter Notebook 运行 Python](#4-用-jupyter-notebook-运行-python)
5. [如何退出](#5-如何退出)
6. [后续工作](#6-后续工作)

---

### 1. 命令行

在计算机还没有酷炫的交互界面甚至连鼠标都没有的年代，人们通过命令行来操作程序，如果你学会了在命令行下如何操作，表面上能看起来像个黑客，实际上能大大加快操作速度。

假如你是 MacOS 或 Linux 用户，博主希望你懂得如何使用终端（Terminal）；假如你是 Windows 用户，则希望你懂得如何使用命令窗口（Command Prompt）或 PowerShell。**以下内容以在 MacOS 上操作为例！**

打开命令行界面后，应该会看到一个白色或黑色的窗口，正等待着你的命令：

```
HOSTNAME:~ USER$
```

其中 `HOSTNAME` 的部分指主机名，冒号后的 `~` 表示当前路径在根目录下，`USER` 是用户名，最后 `$` 提示终端在等待你输入命令。本文将主要用到 `ls` `cd` `pwd` `git` `uv` 这些命令。

**`ls`** — 列出当前路径下的所有文件：

```
HOSTNAME:~ USER$ ls
```

输入后回车，窗口中会返回所有文件和文件夹的名字。

**`cd`** — 进入某个文件夹，假设一个叫 `Downloads` 的文件夹在上述返回的名字列表中：

```
HOSTNAME:~ USER$ cd Downloads
```

**`pwd`** — 回车后"当前路径"已经由 `~` 变成这个文件夹的位置，输入 `pwd` 可以再确认：

```
HOSTNAME:Downloads USER$ pwd
/Users/USER/Downloads
```

**`cd ..`** — 返回上一级目录：

```
HOSTNAME:Downloads USER$ cd ..
```

这些就是最最基本的命令行了！下面的部分会继续讲解其他命令行的用法，需要时刻注意路径是否正确，指令之间是否有空格分隔等等。

---

### 2. Git 用法

Git 即版本控制，是一种记录一个或若干文件内容变化，以便将来查阅特定版本修订情况的系统。程序员们用它才能最快发现到底是谁在什么时候删了一行不该删的代码。

公众号涉及的代码都是由博主先在自己的电脑上通过 git 进行本地版本控制，再托管到 GitHub 这个可以让读者们看到的地方。如果有错误的地方，其他人也可以发起 `pull request` 来纠正，博主再 `git merge` 把别人的修改意见融到自己的代码中。

1. 首先需要将 Git 安装在你的计算机上 — [安装指南](https://git-scm.com/book/zh/v2/%E8%B5%B7%E6%AD%A5-%E5%AE%89%E8%A3%85-Git)
2. 其次，你需要一个 [GitHub](https://github.com) 账号，这也能方便将来对自己代码的托管
3. 之后通过 Git 命令行，将公众号的代码克隆到你的计算机上：

```bash
git clone https://github.com/beiciliang/intro2musictech.git
```

克隆完成后若在当前路径下输入 `ls`，返回的名单中将包含 `intro2musictech`。

因为公众号的代码会随新文章的发布而增加更多内容，博主建议读者发现有新文章发布后通过 `git pull` 来同步更新。

> **Tips**
> - 如果实在觉得各种 git 指令太晦涩，可通过 [GitHub Desktop](https://desktop.github.com/) 软件进行版本控制
> - 如果想更深入了解 git 和 GitHub，英文好的读者可直接参考官方帮助文档，中文资料可参考[这里](https://github.com/xirong/my-git/blob/main/how-to-use-github.md)

---

### 3. 用 uv 设置环境

现在通过 `ls` 查看一下 `intro2musictech` 文件夹里都有哪些东东：

```
HOSTNAME:~ USER$ ls intro2musictech
```

其中 `attachment` 文件夹里包含一些音乐素材和图片，以 `.ipynb` 为后缀的文件都是 Jupyter Notebook，重点是 `pyproject.toml` 中声明的 Python 库，成功安装这些才能确保今后所有 `.ipynb` 中的 Python 代码能跑起来。

不过首先需要解决的大事儿是，如何安装 Python？

我们借助 [uv](https://docs.astral.sh/uv/)，它是一个非常快的 Python 包管理器，能帮你自动安装 Python 并管理依赖。

**安装 uv：**

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**安装 Python 和所有依赖：**

```bash
cd intro2musictech
uv sync
```

`uv sync` 会自动下载合适版本的 Python，创建虚拟环境，并安装 `pyproject.toml` 中声明的所有库。无需手动创建虚拟环境！

**安装 ffmpeg**（librosa 加载 mp3 格式的音频文件需要）：

```bash
# macOS (Homebrew)
brew install ffmpeg

# Ubuntu / Debian
sudo apt install ffmpeg
```

Windows 用户可从 [ffmpeg 官网](https://ffmpeg.org/download.html)下载并添加到系统路径。

---

### 4. 用 Jupyter Notebook 运行 Python

Jupyter Notebook 本身是一种网页端应用，能让用户将说明文本、数学方程、代码和可视化内容全部组合到一个易于共享的文档中。

在项目目录下启动：

```bash
uv run jupyter notebook
```

此时你的浏览器应该会直接弹出一个新页面，你也可以粘贴命令行返回的 URL 链接，拷贝到浏览器中打开应用。

- 点击页面右侧的 `New` 并选择 `Python 3` 可新建一个 Notebook
- 回到之前的页面，进入 `intro2musictech` 文件夹后打开 [00-Hello.ipynb](00-Hello.ipynb)
- 其中简要介绍了 Notebook 在跑 Python 代码时的妙用，你会用它加载一段音频后听到猫叫，并画出波形！

---

### 5. 如何退出

关闭 Notebook 不仅仅要关闭浏览器页面，在其运行的命令行界面，要通过两次 `Ctrl+C` 中止程序。

---

### 6. 后续工作

假设上述所有步骤都能成功执行，那么一旦有新文章时，读者可以在自己的电脑上获取更新后查看最新的 Notebook：

```bash
cd intro2musictech
git pull
uv sync
uv run jupyter notebook
```

</details>
