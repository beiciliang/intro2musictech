# intro2musictech

公众号“无痛入门音乐科技”开源代码，欢迎微信扫码关注或直接搜索intro2musictech！

<img src="https://github.com/beiciliang/intro2musictech/blob/master/attachment/qrcode.jpg" width="200">

**♬ 以后有新的公众号文章发布，其ipynb格式会在GitHub这里同步更新 ♬**

**♫ 方便读者在自己的电脑上一边阅读一边执行代码，快速入门，无痛skr ♫**

更新日期 | 公众号文章链接 | GitHub代码链接               
-------- | ---------------------------------------- | ---------------------------------------------------------
20180727 | [「README」无痛入门音乐科技门槛须知](https://mp.weixin.qq.com/s/S8Q5iSUMgKZQ5g-17dF8UA) | N/A
20180728 | [「SETUP」从零设置编程环境](https://mp.weixin.qq.com/s/ngvmPl5S7QI-PqUUBtbQ3w) | 可直接浏览[下方内容](#从零设置编程环境)，附测试代码[00-Hello.ipynb](https://github.com/beiciliang/intro2musictech/blob/master/00-Hello.ipynb)
20180803 | [「NIME-01」那些为身障人士设计的乐器](https://mp.weixin.qq.com/s/vUU30Ap5ot-Ygpy8eBeC4w) | N/A
20180805 | [「MIR-01」要把音乐画出来，总共分几步？](https://mp.weixin.qq.com/s/pvpFoKKa0Ki_uZ3Y6rqaJw) | [MIR-01.ipynb](https://github.com/beiciliang/intro2musictech/blob/master/MIR-01.ipynb)
20180811 | [「NIME-02」日常物件在没有成精的前提下如何发声儿？](https://mp.weixin.qq.com/s/X05DgjhXO7oMf8Gej5P3Mw) | N/A，可参考[The Bela Blog](http://blog.bela.io/)
20180818 | [「MIR-02_1」音频特征小全之概览](https://mp.weixin.qq.com/s/oFrW7hmZgmAuZGIVHjZTAQ) | [MIR-02_1.ipynb](https://github.com/beiciliang/intro2musictech/blob/master/MIR-02_1.ipynb)
20180822 | [「INFO」音乐科技相关科研组列表](https://mp.weixin.qq.com/s/2nDWikda9fh2x5o093F6HA) | 列表会在[这里](https://github.com/beiciliang/intro2musictech/blob/master/INFO-ResearchGroups.md)更新
20180827 | [「NIME-03」为什么说钢琴是乐器之王？复杂！](https://mp.weixin.qq.com/s?__biz=MzU5MzY3NzI0OA==&mid=2247483718&idx=1&sn=fbf3f7c11e61096bafd72ea6ed0c0e8a&scene=19#wechat_redirect) | N/A，原知乎问题在[这里](
https://www.zhihu.com/question/288614974)

---

### 从零设置编程环境:

以下内容适用于编程零基础的读者，如果你已经清楚如何`git clone`本项目，并能在一个基于Python 3的虚拟环境内安装Jupyter Notebook以及[requirements.txt](https://github.com/beiciliang/intro2musictech/blob/master/requirements.txt)中的第三方库之后，不报错地加载[00-Hello.ipynb](https://github.com/beiciliang/intro2musictech/blob/master/00-Hello.ipynb)并运行其中代码，恭喜你，编程环境配置成功！

1. [命令行基础操作](#命令行)

2. [Git用法](#git用法)

3. [Anaconda设置环境](#anaconda设置环境)

4. [用Jupyter Notebook运行Python代码](#用jupyter-notebook运行python)

5. [如何退出](#如何退出)

6. [后续工作](#后续工作)

---

### 『命令行』

在计算机还没有酷炫的交互界面甚至连鼠标都没有的年代，人们通过命令行来操作程序，如果你学会了在命令行下如何操作，表面上能看起来像个黑客，实际上能大大加快操作速度。

假如你是MacOS或Linux用户，博主希望你懂得如何使用终端(Terminal)；假如你是Windows用户，则希望你懂得如何使用命令窗口(Command Prompt)或PowerShell。**以下内容以在MacOS上操作为例！**

✎ 打开命令行界面后，应该会看到一个白色或黑色的窗口，正等待着你的命令：
```
HOSTNAME:~ USER$ 
```

其中`HOSTNAME`的部分指主机名，冒号后的`~`表示当前路径在根目录下，`USER`是用户名，最后`$`提示终端在等待你输入命令。本文将主要用到`ls` `cd` `pwd` `git` `conda` `pip` 这些命令。

✎ 首先`ls`表示列出当前路径下的所有文件：
```
HOSTNAME:~ USER$ ls
```

输入后回车，窗口中会返回所有文件和文件夹的名字。

✎ 假设一个叫`Downloads`的文件夹在上述返回的名字列表中，进入这个文件夹需要`cd`：
```
HOSTNAME:~ USER$ cd Downloads
```

✎ 回车后“当前路径”已经由`~`变成这个文件夹的位置，输入`pwd`可以再确认：
```
HOSTNAME:Downloads USER$ pwd
```

回车后会显示当前路径为
```
/Users/USER/Downloads
```

✎ 如果需要返回上一级目录，依然可以使用`cd`：
```
HOSTNAME:Downloads USER$ cd ..
```

这些就是最最基本的命令行了！下面的部分会继续讲解其他命令行的用法，需要时刻注意路径是否正确，指令之间是否有空格分隔等等。

---

### 『Git用法』

Git即版本控制，是一种记录一个或若干文件内容变化，以便将来查阅特定版本修订情况的系统。程序员们用它才能最快发现到底是谁在什么时候删了一行不该删的代码。

公众号涉及的代码都是由博主先在自己的电脑上通过git进行本地版本控制，再托管到Github这个可以让读者们看到的地方。如果有错误的地方，其他人也可以发起`pull request`来纠正，博主再`git merge`把别人的修改意见融到自己的代码中。


✎ 首先需要将Git安装在你的计算机上，安装指南[点击链接](https://git-scm.com/book/zh/v2/%E8%B5%B7%E6%AD%A5-%E5%AE%89%E8%A3%85-Git)

✎ 其次，你需要一个GitHub账号，这也能方便将来对自己代码的托管。

✎ 之后你可以通过Git命令行，将公众号的代码克隆到你的计算机上：
```
HOSTNAME:~ USER$ git clone https://github.com/beiciliang/intro2musictech.git
```

克隆完成后若在当前路径下输入`ls`，返回的名单中将包含`intro2musictech`。

因为公众号的代码会随新文章的发布而增加更多内容，博主建议读者发现有新文章发布后通过`git pull`来同步更新。

☞ 如果实在觉得各种git指令太晦涩，可通过GitHub Desktop软件进行版本控制。

☞ 如果想更深入了解git和GitHub，英文好的读者可直接参考官方帮助文档，中文资料可参考[这里](https://github.com/xirong/my-git/blob/master/how-to-use-github.md)

---

### 『Anaconda设置环境』

现在通过`ls`查看一下`intro2musictech`文件夹里都有哪些东东:

```
HOSTNAME:~ USER$ ls intro2musictech
```

其中`attachment`文件夹里包含一些音乐素材和图片，以`.ipynb`为后缀的文件都是Jupyter Notebook，重点是`requirements.txt`中所有的Python库，成功安装这些才能确保今后所有`.ipynb`中的Python代码能跑起来。

不过首先需要解决的大事儿是，如何安装Python？

我们可借助Anaconda，即一个预装了很多我们用的到或用不到的第三方库的Python。

✎ 首先去官网根据自己系统的型号，下载**Anaconda3**并安装，但是国内的同学也许会发现官网下载太慢，这种情况可从国内清华大学开源软件镜像站进行下载并配置镜像:

☞ [官方下载链接](https://www.anaconda.com/download/)

☞ [清华大学镜像站](https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/)

✎ 安装过程中，建议勾选把Anaconda加入环境变量，并设置Anaconda所带的Python 3.6为系统默认的Python版本，不过这些步骤不做问题也不大，反正之后我们要建立一个新的Python 3.7虚拟环境！

**另**，建议国内读者通过镜像成功安装Anaconda之后，修改其包管理镜像为国内源，即运行下方两个命令行：

```
$ conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
$ conda config --set show_channel_urls yes
```

✎ 安装Anaconda后，用它建立虚拟环境可以指定要安装在环境中的Python版本和第三方库，避免在自己的电脑上瞎安装/起冲突/费时间，这对需要同时用Python版本2和3的程序员非常有必要！

✎ 下面的命令行将一步步带领读者走向成功的一半！

1. 先用`conda`在全局下安装些notebook的拓展包：
```
$ conda install nb_conda
$ conda install -c conda-forge jupyter_nbextensions_configurator
```

2. 建立一个名字为`py37`的环境，该环境下Python版本为3.7，并安装`ipykernel`这个库也就顺便将Jupyther Notebook安装到`py37`环境中：
```
$ conda create -n py37 python=3.7 ipykernel
```

3. 激活`py37`环境：
```
$ source activate py37
```

激活后可见命令行开头有括号提示你已经在括号内显示的虚拟环境中。

4. 在该虚拟环境下用`pip`安装其他第三方库（先升级下`pip`）：
```
(py37)$ pip install --upgrade pip
(py37)$ pip install numpy scipy matplotlib librosa scikit-learn
```

**另**，这些库也可通过指令`pip install -r requirements.txt`来安装，注意除非当前路径与该txt文件相同，否则要在指令中声明txt所在的具体路径！

对于第三方库的安装，用`pip`或`conda`其实没有大区别，但博主一般会参考这个库本身建议哪种方式最简单。

5. 此时你可通过`conda list`指令来查看`py37`环境下具体成功安装上了哪些库。

6. 若想退出虚拟环境，可直接输入`source deactivate`后回车，不过为了最后关于Notebook的环节，暂且先不要退出！

**对于完全不想安装anaconda，只想用`pip`掌控大权的读者**：

创建虚拟环境的时候就需要用其他如[virtualenv](https://virtualenv.pypa.io/en/stable/)的辅助，在创建并激活进入到虚拟环境后：
```
(py37)$ pip install --upgrade pip
(py37)$ pip install ipykernel
(py37)$ ipython kernel install --user --name=py37
(py37)$ pip install -r requirements.txt
```

在以上设置完成后才能确保`py37`中的Python 3内核将被Notebook正确调用。

---

### 『用Jupyter Notebook运行Python』

Jupyter Notebook本身是一种网页端应用，能让用户将说明文本、数学方程、代码和可视化内容全部组合到一个易于共享的文档中。

✎ 现在我们在`py37`虚拟环境下直接用命令行打开该应用：
```
(py37)$ jupyter notebook
```

此时你的浏览器应该会直接弹出一个新页面，你也可以粘贴命令行返回的URL链接，拷贝到浏览器中打开应用。

✎ 点击页面右侧的`New`并选择`Python [conda env:py37]`可新建一个基于该虚拟环境的Notebook。

✎ 现在我们回到之前的页面，进入`intro2musictech`文件夹后打开`00-Hello.ipynb`。

✎ 读者也可直接浏览[00-Hello.ipynb](https://github.com/beiciliang/intro2musictech/blob/master/00-Hello.ipynb)的内容。

✎ 其中简要介绍了Notebook在跑Python代码时的妙用，你会用它加载一段音频后听到猫叫，并画出波形！

---

### 『如何退出』

✎ 关闭Notebook不仅仅要关闭浏览器页面，在其运行的命令行界面，要通过两次`CTRL+C`中止程序。

✎ 通过`source deactivate`命令行退出当前虚拟环境。

✎ 以后若需要再次激活某个虚拟环境但不巧忘了其名字，可通过`conda env list`指令来查询。

✎ 慎重！如果对这个`py37`虚拟环境不爽，可以用`conda env remove -n py37`彻底删除。

---

### 『后续工作』

假设上述所有步骤都能成功执行，那么一旦有新文章时，读者可以在自己的电脑上获取更新后查看最新的Notebook，大致流程如下：
```
$ cd intro2musictech
$ git pull
$ source activate py37
(py37)$ jupyter notebook
```

