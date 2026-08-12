import marimo

__generated_with = "0.19.11"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 拼起来，再拆回去：用音乐讲明白傅里叶变换

    我们先用最简单的材料“正弦波”搭出乐音、旋律和一小段芯片音乐；然后反过来问：拿到一段声音，能不能把它是由哪些正弦波、多大振幅拼出来的算回去？把这个“反推”的问题想清楚，就等于把离散傅里叶变换（DFT）想清楚了。

    全文只需要高中三角函数的底子。图和声音都是现场算出来的，拖动滑块就能听见变化。

    > 本文的思路与例子改编自 George Tzanetakis 的
    > [A music and sound exposition of the Discrete Fourier Transform](https://medium.com/@georgetzanetakis/a-music-and-sound-exposition-of-the-discrete-fourier-transform-part-1-79b641ed1078)
    > 及其配套 Jupyter 笔记本，中文内容由博主重写整理。
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 目录

    **上半场：拼起来**（用正弦波造出声音）

    - [一、声音在计算机里就是一串数字](#sec1)
    - [二、一条正弦波，三个数就说完了](#sec2)
    - [三、把正弦波排成旋律](#sec3)
    - [四、让音符像乐器：振幅包络](#sec4)
    - [五、叠起来：加法合成](#sec5)

    **下半场：拆回去**（把声音还原成正弦波）

    - [六、把问题倒过来问](#sec6)
    - [七、还剩两道坎：相位和时间](#sec7)
    - [八、相位这道坎](#sec8)
    - [九、时间这道坎：把声音切成小段](#sec9)
    - [十、探针的频率对不准会怎样](#sec10)
    - [十一、DFT 就是一整排探针](#sec11)
    - [十二、声谱图：把两道坎一起跨过去](#sec12)

    [收个尾](#sec-end)　·　[其他参考资料](#sec-ref)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec1"></a>

    ## 一、声音在计算机里就是一串数字

    声音是空气压强的起伏。要让计算机处理它，得做两件事：

    - **采样**：每隔固定的一小段时间量一次压强。每秒量多少次叫**采样率**，本文的例子一律用 22050 次/秒。
    - **量化**：把量到的值存成一个数。本文一律用 -1.0 到 1.0 之间的浮点数，算起来省事。

    所以后面所有的“声音”，本质上都是一个很长的浮点数组，一秒钟的声音就是 22050 个介于 -1.0 和 1.0 之间的数。（采样率为什么不能随便取小，第十一节讲到奈奎斯特频率时会有交代。）

    下面两张图画的是同一段信号：左边是我们后面惯用的连线画法，右边把每一个采样点都标了出来，这才是数组的真面目。为了看得清，这里的采样率故意压到了每秒 20 点。
    """)
    return


@app.cell(hide_code=True)
def _():
    import io
    import logging
    import wave

    import librosa
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib import font_manager

    logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)

    plt.xkcd()  # 手绘风格，图看起来轻松一点

    # 手绘风格自带的字体没有汉字。把系统里可用的中文字体按优先级排成一个列表交给
    # matplotlib，它会逐字回退：前面的字体缺哪个字，就用后面的补上（有些字体只覆盖
    # 繁体，简体字形会画成方框）。
    _installed = {f.name for f in font_manager.fontManager.ttflist}
    _cjk = [
        _font
        for _font in [
            "PingFang SC",
            "Heiti SC",
            "Songti SC",
            "STHeiti",
            "Hiragino Sans GB",
            "Noto Sans CJK SC",
            "Source Han Sans SC",
            "Microsoft YaHei",
            "SimHei",
            "PingFang HK",
            "Heiti TC",
            "Arial Unicode MS",
        ]
        if _font in _installed
    ]
    if _cjk:
        plt.rcParams["font.family"] = _cjk
    plt.rcParams["axes.unicode_minus"] = False
    return io, librosa, np, plt, wave


@app.cell
def _(io, mo, np, plt, wave):
    SR = 22050  # 全文默认采样率

    def sine(freq, dur=1.0, amp=1.0, phase=0.0, sr=SR):
        """生成一段正弦波，返回（时间轴，采样数组）。"""
        t = np.arange(int(sr * dur)) / sr  # 相邻采样点正好隔 1/sr 秒
        return t, amp * np.sin(2 * np.pi * freq * t + phase)

    def play(x, rate=SR, normalize=False):
        """把采样数组变成 16 位单声道 WAV，交给播放器。"""
        x = np.asarray(x, dtype=float)
        peak = np.max(np.abs(x))
        if normalize and peak > 0:
            x = x / peak * 0.95  # 音量太大时整体缩放
        pcm = (np.clip(x, -1.0, 1.0) * 32767).astype("<h").tobytes()

        buffer = io.BytesIO()
        with wave.open(buffer, "wb") as f:
            f.setnchannels(1)
            f.setsampwidth(2)
            f.setframerate(int(rate))
            f.writeframes(pcm)
        buffer.seek(0)
        return mo.audio(buffer)

    def fig_ax(title="", xlabel="时间（秒）", ylabel="振幅", figsize=(9, 3.6), ylim=None):
        """开一张图，顺手把标题和坐标轴标签设好。"""
        fig, ax = plt.subplots(figsize=figsize)
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        if ylim:
            ax.set_ylim(*ylim)
        return fig, ax

    return SR, fig_ax, play, sine


@app.cell
def _(np, plt):
    _sr, _dur, _freq = 20, 1.5, 2  # 每秒 20 个采样点，1.5 秒，2 Hz
    _t = np.linspace(0, _dur, int(_sr * _dur), endpoint=False)
    _x = np.sin(2 * np.pi * _freq * _t)

    _fig, (_a1, _a2) = plt.subplots(1, 2, figsize=(11, 4))
    _a1.plot(_t, _x, lw=2, color="tab:blue")
    _a1.set_title("连线画出来的样子")
    _a1.set_xlabel("时间（秒）")
    _a1.set_ylabel("振幅")

    _markers, _stems, _ = _a2.stem(_t, _x, linefmt="r-", markerfmt="ro", basefmt=" ")
    plt.setp(_stems, lw=1.2)
    plt.setp(_markers, ms=4)
    _a2.plot(_t, _x, color="tab:blue", alpha=0.35)
    _a2.set_title(f"其实只有 {len(_x)} 个采样点")
    _a2.set_xlabel("时间（秒）")

    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec2"></a>

    ## 二、一条正弦波，三个数就说完了

    正弦波是一条形状固定、不断重复的曲线，写成公式是：

    $$
    f(t) = \alpha \sin(\omega t + \phi)
    $$

    它只由三个数决定：**振幅** $\alpha$（多响）、**频率** $\omega$（多高）、**相位** $\phi$（从波形的哪个位置起步）。这三个数是全文的主角：后面所有的分析工作，说到底就是把它们从一堆采样值里挖出来。

    顺带一提：数学上的正弦波无始无终，真实的声音却总有起点和终点。所以正弦波只是个好用的理想模型，这一点值得先记在心里。

    拖动下面的滑块，看波形也听声音。振幅只影响响度，频率决定音高，而相位改的只是波形的起点，单独听的时候，耳朵几乎察觉不到它。
    """)
    return


@app.cell
def _(mo):
    amp_ui = mo.ui.slider(0.1, 1.0, 0.05, value=0.6, label="振幅 α", show_value=True)
    freq_ui = mo.ui.slider(110, 880, 10, value=220, label="频率 ω（Hz）", show_value=True)
    phase_ui = mo.ui.slider(0.0, 6.2, 0.2, value=0.0, label="相位 φ（弧度）", show_value=True)
    return amp_ui, freq_ui, phase_ui


@app.cell
def _(SR, amp_ui, fig_ax, freq_ui, mo, phase_ui, play, sine):
    _t, _x = sine(freq_ui.value, dur=1.5, amp=amp_ui.value, phase=phase_ui.value)

    _n = SR // 40  # 只画很短的一段，才看得出波形
    _fig, _ax = fig_ax(
        title=f"α = {amp_ui.value:.2f}　ω = {freq_ui.value} Hz　φ = {phase_ui.value:.1f}",
        ylim=(-1.05, 1.05),
    )
    _ax.plot(_t[:_n], _x[:_n], lw=2, color="tab:blue")

    mo.vstack([
        mo.hstack([amp_ui, freq_ui, phase_ui], justify="start", gap=1.5, wrap=True),
        _fig,
        play(_x),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec3"></a>

    ## 三、把正弦波排成旋律

    给定几个频率，按顺序播放，就有了旋律。C5、D5、E5 大致对应 523、587、659 Hz。频率和音名之间怎么对应，背后是一整套调律系统的故事，这里先直接用现成的数。

    下面这段是「1 2 3 1」重复两遍。你会听到一个毛病：每个音都是硬生生地开始、硬生生地断掉，像有人在拿开关按乐器。
    """)
    return


@app.cell
def _(np, play, sine):
    NOTES = {"1": 523.0, "2": 587.0, "3": 659.0}  # do re mi（C5 D5 E5）
    SCORE = ["1", "2", "3", "1", "1", "2", "3", "1"]

    _melody = np.hstack([sine(NOTES[n], dur=0.5, amp=0.5)[1] for n in SCORE])
    play(_melody)
    return NOTES, SCORE


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec4"></a>

    ## 四、让音符像乐器：振幅包络

    真实乐器的音量一直在变：拨一下弦是“啪”地冲上去再慢慢消失，拉一把小提琴是缓缓涨起来。合成器里描述这条音量曲线的经典模型叫 **ADSR**，也就是起音（Attack）、衰减（Decay）、保持（Sustain）、释放（Release）。

    做法很朴素：先算出一条 0 到 1 的曲线，再让它逐点乘到正弦波上。
    """)
    return


@app.cell
def _(SR, np):
    def adsr(dur, attack=0.05, decay=0.10, sustain=0.8, release=0.10, sr=SR):
        """ADSR 包络。attack/decay/release 是各段占总时长的比例，sustain 是保持段的高度。"""
        n = int(dur * sr)
        na, nd, nr = int(attack * n), int(decay * n), int(release * n)
        ns = n - na - nd - nr
        if ns < 0:
            raise ValueError("起音、衰减、释放三段的比例加起来不能超过 1。")
        return np.concatenate([
            np.linspace(0.0, 1.0, na, endpoint=False),      # 冲上去
            np.linspace(1.0, sustain, nd, endpoint=False),  # 掉到保持电平
            np.full(ns, sustain),                           # 稳住
            np.linspace(sustain, 0.0, nr),                  # 收尾
        ])

    PRESETS = {
        "拨弦": dict(attack=0.01, decay=0.30, sustain=0.15, release=0.69),
        "弦乐": dict(attack=0.25, decay=0.15, sustain=0.70, release=0.35),
        "打击": dict(attack=0.00, decay=0.30, sustain=0.00, release=0.70),
    }
    return PRESETS, adsr


@app.cell
def _(PRESETS, SR, adsr, fig_ax, np):
    _fig, _ax = fig_ax(title="三条包络的形状（时长都是 1 秒）", ylabel="音量倍数")
    for _name, _cfg in PRESETS.items():
        _env = adsr(1.0, **_cfg, sr=SR)
        _ax.plot(np.arange(len(_env)) / SR, _env, lw=2, label=_name)
    _ax.legend(loc="upper right")
    _fig
    return


@app.cell
def _(NOTES, PRESETS, SCORE, adsr, mo, np, play, sine):
    melody_dry = np.hstack([sine(NOTES[n], dur=0.5, amp=0.5)[1] for n in SCORE])
    melody_wet = np.hstack([
        sine(NOTES[n], dur=0.5, amp=0.5)[1] * adsr(0.5, **PRESETS["拨弦"])
        for n in SCORE
    ])

    mo.vstack([
        mo.md("**光秃秃的正弦波**"),
        play(melody_dry),
        mo.md("**乘上“拨弦”包络之后**"),
        play(melody_wet),
    ])
    return (melody_wet,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec5"></a>

    ## 五、叠起来：加法合成

    几条正弦波可以直接相加。有意思的是耳朵的反应：

    - 当各个频率是同一个基础频率的**整数倍**（220、440、880……，这个基础频率叫**基频**），它们会“粘”成一个音色饱满的单音，听上去像管风琴，而不是三个音；
    - 一旦倍数不是整数（220、297、503），黏合就散了，你会听出好几个音同时响，声音也变得刺耳。

    这就是**加法合成**。反过来说，只要频率、振幅、相位配得合适，任何复杂的声音原则上都能这么堆出来，这也正是后面“反推”有戏可做的原因。

    调调下面三个滑块，再拨一下开关试试。
    """)
    return


@app.cell
def _(mo):
    h1_ui = mo.ui.slider(0.0, 1.0, 0.05, value=0.60, label="第 1 个分量 220 Hz", show_value=True)
    h2_ui = mo.ui.slider(0.0, 1.0, 0.05, value=0.30, label="第 2 个分量 440 / 297 Hz", show_value=True)
    h3_ui = mo.ui.slider(0.0, 1.0, 0.05, value=0.20, label="第 3 个分量 880 / 503 Hz", show_value=True)
    inharmonic_ui = mo.ui.switch(value=False, label="让后两个分量偏离整数倍（440→297，880→503）")
    return h1_ui, h2_ui, h3_ui, inharmonic_ui


@app.cell
def _(
    PRESETS,
    SR,
    adsr,
    fig_ax,
    h1_ui,
    h2_ui,
    h3_ui,
    inharmonic_ui,
    mo,
    np,
    play,
    sine,
):
    _freqs = (220.0, 297.0, 503.0) if inharmonic_ui.value else (220.0, 440.0, 880.0)
    _amps = (h1_ui.value, h2_ui.value, h3_ui.value)

    _parts = [sine(f, dur=1.0, amp=a)[1] for f, a in zip(_freqs, _amps)]
    _mixed = sum(_parts)

    _span = 1.2 * max(0.8, np.max(np.abs(_mixed)))  # 纵轴跟着波形高低走
    _fig, _ax = fig_ax(title="三个分量相加之后的波形", ylim=(-_span, _span))
    _t = np.arange(SR // 40) / SR
    for _f, _p in zip(_freqs, _parts):
        _ax.plot(_t, _p[: len(_t)], lw=1, alpha=0.5, label=f"{_f:.0f} Hz")
    _ax.plot(_t, _mixed[: len(_t)], lw=2.5, color="black", label="相加结果")
    _ax.legend(loc="upper right", ncol=2, fontsize=8)

    # 加上包络，听起来更像一件乐器
    _note = _mixed * adsr(1.0, **PRESETS["弦乐"], sr=SR)

    mo.vstack([
        mo.hstack([h1_ui, h2_ui, h3_ui], justify="start", gap=1.5, wrap=True),
        inharmonic_ui,
        _fig,
        mo.md("**直接相加**"),
        play(_mixed, normalize=True),
        mo.md("**加上包络，连奏三下**"),
        play(np.hstack([_note, _note, _note]), normalize=True),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    非整数倍的分量并不是只会捣乱。钟声就是典型：它的分音（每个正弦分量）刻意偏离整数倍，还各有各的衰减速度：高频那一下“当”消失得最快，低频的嗡鸣拖得最久。给每个分音配一条自己的包络，几行代码就能敲出一口钟。
    """)
    return


@app.cell
def _(SR, adsr, np, play, sine):
    def bell(root, dur=3.0, sr=SR):
        # （频率倍数，相对音量，衰减快慢），其中 1.19 和 4.1 都不是整数倍
        partials = [
            (0.50, 0.5, 0.50),  # 嗡鸣
            (1.00, 1.0, 0.40),  # 基频
            (1.19, 0.6, 0.30),  # 小三度
            (1.50, 0.4, 0.25),  # 五度
            (2.00, 0.5, 0.20),  # 八度
            (4.10, 0.7, 0.05),  # 敲下去那一瞬的高频
        ]
        x = np.zeros(int(dur * sr))
        for mult, amp, decay in partials:
            env = adsr(dur, attack=0.0, decay=decay, sustain=0.0, release=1.0 - decay, sr=sr)
            x += amp * sine(root * mult, dur=dur, sr=sr)[1] * env
        return x / np.max(np.abs(x)) * 0.85

    play(np.concatenate([bell(329.0, 3.0), bell(261.0, 2.0), bell(196.0, 2.0), bell(196.0, 2.0)]))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    1980 年代的游戏机声音芯片，能耐大致就到“几个简单振荡器 + 包络”为止，芯片音乐（chiptune）便是在这个限制里长出来的。手上的工具已经够了：一条低音打点、一层长音铺底、一条主旋律，叠在同一个时间轴上就行。
    """)
    return


@app.cell
def _(PRESETS, SR, adsr, np, play, sine):
    BPM = 120
    BEAT = 60.0 / BPM  # 每拍 0.5 秒

    def midi_freq(note):
        """MIDI 音符号 → 频率。69 号是 440 Hz 的 A4。"""
        return 440.0 * 2.0 ** ((note - 69) / 12.0)

    def add_note(track, start_beat, beats, note, amp, preset, sr=SR):
        """把一个音写进时间轴 track。"""
        dur = beats * BEAT
        i = int(start_beat * BEAT * sr)
        x = sine(midi_freq(note), dur=dur, sr=sr)[1] * adsr(dur, **PRESETS[preset], sr=sr)
        track[i : i + len(x)] += amp * x

    _track = np.zeros(int(9 * BEAT * SR))  # 8 拍，末尾留一点余量

    add_note(_track, 0, 8, 67, 0.10, "弦乐")  # 铺底长音 G4
    for _beat in range(8):
        add_note(_track, _beat, 1, 36, 0.45, "打击")  # 每拍一下低音 C2
    for _i, _note in enumerate([79, 79, 74, 75, 77, 75, 74, 72, 72, 75, 79, 77, 75]):
        add_note(_track, _i * 0.5, 0.4, _note, 0.30, "拨弦")  # 主旋律，八分音符

    play(_track, normalize=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec6"></a>

    ## 六、把问题倒过来问

    到这里，“合成”这条路已经走通了：给出频率、振幅、相位，就能造出声音。

    现在把箭头反过来：**只给一段采样数组，能不能算出它是由哪些正弦波、多大振幅拼成的？**

    这就是**分析**问题，它是加法合成的逆问题，也是音乐信息检索里几乎所有事情的起点：识别音高、辨认和弦、分析音色，都得先回答它。

    整个问题一次啃不下来，我们从最小的一块开始：**频率已知，只估振幅**。这个玩具问题里藏着 DFT 的全部核心。

    下面用一条 550 Hz、振幅 0.8 的正弦波当“标准答案”，再往里掺噪声，看几种办法各自能撑多久。
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    三种思路，从笨到聪明：

    **① 峰值**：取最大值。干净信号上完全正确，但它只看一个采样点，噪声随便冒个尖峰就能把答案带跑。

    **② RMS（均方根）**：让每个采样都参与，先平方、再平均、再开根号。

    $$
    \mathrm{RMS} = \sqrt{\frac{1}{N}\sum_{n=0}^{N-1} x[n]^2}
    $$

    正弦波的 RMS 是振幅的 $1/\sqrt{2}$，所以代码里补了一个 $\sqrt{2}$ 把它换算回振幅。它比峰值稳得多，可它照单全收：噪声的能量也算进去了，噪声一大就虚高。

    **③ 点积（相关）**：这一步要用上“频率已知”这个条件。造一条同频率、振幅为 1 的正弦波当**探针**（也叫**基**），拿它和信号逐点相乘再求平均：

    $$
    \langle x, p \rangle = \sum_{n=0}^{N-1} x[n]\, p[n]
    $$

    它衡量的是“信号里有多少成分长得像这条探针”。噪声和探针形状不像，乘出来正负相抵、平均下来趋近于零；只有那条同频同相的正弦波会稳定地留下来。**代价是探针必须和目标同频、并且相位对齐。**
    """)
    return


@app.cell
def _(SR, np, sine):
    TRUE_AMP, TARGET_FREQ = 0.8, 550.0
    _t, target = sine(TARGET_FREQ, dur=3.0, amp=TRUE_AMP)

    def peak_amp(x):
        return np.max(np.abs(x))

    def rms_amp(x):
        return np.sqrt(np.mean(np.square(x))) * np.sqrt(2.0)

    def dot_amp(x, freq, sr=SR):
        probe = np.sin(2 * np.pi * freq * np.arange(len(x)) / sr)  # 探针：同频、振幅 1
        return 2 * np.dot(x, probe) / len(x)

    return TARGET_FREQ, TRUE_AMP, dot_amp, peak_amp, rms_amp, target


@app.cell
def _(mo):
    noise_ui = mo.ui.slider(
        0.0, 1.5, 0.05, value=0.30, label="噪声强度（标准差）", show_value=True
    )
    return (noise_ui,)


@app.cell
def _(
    TARGET_FREQ,
    TRUE_AMP,
    dot_amp,
    fig_ax,
    mo,
    noise_ui,
    np,
    peak_amp,
    play,
    rms_amp,
    target,
):
    _noise = np.random.default_rng(0).normal(0, noise_ui.value, len(target))
    _mix = target + _noise

    _ests = [
        ("峰值", peak_amp(_mix), "tab:red"),
        ("RMS", rms_amp(_mix), "tab:orange"),
        ("点积", dot_amp(_mix, TARGET_FREQ), "tab:green"),
    ]

    _n = 1000
    _fig, _ax = fig_ax(
        title=f"真实振幅 {TRUE_AMP}，噪声标准差 {noise_ui.value:.2f}",
        xlabel="采样点",
        ylim=(-3.5, 3.5),
    )
    _ax.plot(_mix[:_n], color="0.75", lw=1, label="混合信号")
    _ax.plot(target[:_n], color="tab:blue", lw=1.5, label="被埋住的正弦波")
    for _name, _value, _color in _ests:
        _ax.axhline(_value, color=_color, lw=3, label=f"{_name} {_value:.2f}")
    # 真实振幅画在最上层，才不会被估计值的线盖住
    _ax.axhline(TRUE_AMP, color="black", ls=(0, (4, 3)), lw=2, zorder=6, label=f"真实振幅 {TRUE_AMP}")
    _ax.legend(loc="lower left", ncol=3, fontsize=8)

    _rows = "\n".join(
        f"| {n} | {v:.2f} | {abs(v - TRUE_AMP) / TRUE_AMP * 100:.0f}% |"
        for n, v, _ in _ests
    )

    mo.vstack([
        noise_ui,
        _fig,
        mo.md(f"| 方法 | 估计值 | 相对误差 |\n|---|---|---|\n{_rows}"),
        play(_mix, normalize=True),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    把滑块推到底：峰值和 RMS 会越飘越高，点积却几乎钉在 0.8 不动。而你的耳朵此刻仍然能在噪声里听出那个音。某种意义上，耳朵做的事和点积更像。

    点积为什么这么稳？看逐点相乘的结果就明白了。信号里和探针同频同相的那部分，正对正、负对负，乘完全是正数，平均值把它们攒了下来（正弦波的情形正好攒到振幅的一半，所以代码里乘 2）；噪声和探针没有固定的对应关系，乘出来正负掺半，平均之后彼此抵消。**分析用的片段越长，噪声抵消得越干净。**
    """)
    return


@app.cell
def _(SR, TARGET_FREQ, np, plt, target):
    _n = 600
    _probe = np.sin(2 * np.pi * TARGET_FREQ * np.arange(len(target)) / SR)
    _mix = target + np.random.default_rng(1).normal(0, 0.8, len(target))

    _fig, (_a1, _a2) = plt.subplots(1, 2, figsize=(11, 4), sharey=True)
    for _ax, _sig, _name in [(_a1, target, "干净的正弦波"), (_a2, _mix, "掺了噪声之后")]:
        _prod = _sig * _probe
        _ax.plot(_sig[:_n], color="0.75", lw=1, label="信号")
        _ax.plot(_probe[:_n], color="tab:blue", lw=1, alpha=0.7, label="探针")
        _ax.plot(_prod[:_n], color="tab:orange", lw=1.5, label="逐点相乘")
        _ax.axhline(np.mean(_prod), color="tab:purple", ls="--", lw=2, label=f"乘积的平均 {np.mean(_prod):.2f}")
        _ax.axhline(2 * np.mean(_prod), color="tab:green", lw=2.5, label=f"×2 = 振幅估计 {2 * np.mean(_prod):.2f}")
        _ax.set_title(_name)
        _ax.set_xlabel("采样点")
        _ax.set_ylim(-3, 3)
    _a1.set_ylabel("振幅")
    _a1.legend(loc="lower left", fontsize=8)

    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    换个更狠的干扰：不用噪声，直接拿一段小号独奏盖上去。小号比那条正弦波响好几倍，波形图上几乎看不出正弦波的影子，点积却照样把 0.8 找了回来。

    （下面这格第一次运行会联网下载 librosa 自带的小号示例。）
    """)
    return


@app.cell
def _(
    SR,
    TARGET_FREQ,
    TRUE_AMP,
    dot_amp,
    fig_ax,
    librosa,
    mo,
    np,
    play,
    target,
):
    trumpet, _ = librosa.load(librosa.ex("trumpet"), sr=SR)
    trumpet = trumpet / np.max(np.abs(trumpet))  # 归一化，后面还要用

    _n = min(len(trumpet), len(target))
    _loud = trumpet[:_n] * 4.0  # 放到正弦波的 5 倍响
    _mix = target[:_n] + _loud

    _est = dot_amp(_mix, TARGET_FREQ)

    _fig, _ax = fig_ax(
        title=f"小号当干扰：真实振幅 {TRUE_AMP}，点积估计 {_est:.2f}",
        xlabel="采样点",
        ylim=(-5, 5),
    )
    _ax.plot(_mix[:1500], color="0.75", lw=1, label="正弦波 + 小号")
    _ax.plot(target[:1500], color="tab:blue", lw=1.5, label="被埋住的正弦波")
    _ax.axhline(TRUE_AMP, color="black", ls="--", lw=2, label="真实振幅")
    _ax.axhline(_est, color="tab:green", lw=2, label="点积估计")
    _ax.legend(loc="lower left", ncol=2, fontsize=8)

    mo.vstack([_fig, play(_mix, normalize=True)])
    return (trumpet,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec7"></a>

    ## 七、还剩两道坎：相位和时间

    盘一下手上有什么：**知道频率、而且探针和目标的相位对得上，一次点积就能从一团乱响里把某条正弦波的振幅捞出来。**

    两个“而且”都很刺眼：

    - **相位**：真实的声音不会好心地从零点开始往上走。探针和目标错开一点，点积就偏小；错开四分之一周期，答案直接归零。
    - **时间**：音乐一直在变。一个音响半秒就换了，对整段录音做一次点积，等于把所有变化揉成一个数。

    这两道坎跨过去，DFT 就在门口了。
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec8"></a>

    ## 八、相位这道坎

    第六节的点积有个前提一直没挑明：**探针和目标得"同时出发"**。

    所谓相位 $\varphi$，说白了就是"这条波比探针晚出发了多少"。可真实录音里的一个音从哪儿开始，全看你什么时候按下录音键，没人有义务和我们的探针对齐。

    先看看错开之后有多惨。下面的目标是一条 440 Hz、振幅 0.8 的正弦波，探针是同频率、振幅 1、从零点起步的那条。拖动滑块改变目标的相位：

    - $\varphi = 0$（完全对齐）：两条波同起同落，逐点相乘处处为正，点积老老实实给出 0.8；
    - $\varphi = \pi/2$（错开四分之一周期）：答案变成 **0**。看图就明白：有一半时间两条波同号（乘积为正，加分），另一半时间反号（乘积为负，扣分），加起来正好抵消。这种"谁也占不到便宜"的关系叫**正交**；
    - $\varphi = \pi$（完全反相）：处处反号，全程扣分，答案变成 **−0.8**。

    规律很清楚：错得越多，得分越低。单条探针量到的其实不是振幅 $A$，而是 $A\cos\varphi$，它把振幅和相位搅成了一个数。不知道 $\varphi$，这个数就没法用。
    """)
    return


@app.cell
def _(SR, np):
    def sin_cos_amp(x, freq, sr=SR):
        """一对正弦／余弦探针：同时估出振幅和相位。

        返回 (振幅 R, 相位 φ, a, b)，其中 x ≈ a·sin(θ) + b·cos(θ)。
        """
        theta = 2 * np.pi * freq * np.arange(len(x)) / sr
        a = 2 * np.dot(x, np.sin(theta)) / len(x)  # 和正弦探针的点积
        b = 2 * np.dot(x, np.cos(theta)) / len(x)  # 和余弦探针的点积
        return np.hypot(a, b), np.arctan2(b, a), a, b

    def phase_scan(x, freq, sr=SR, steps=361):
        """笨办法：把探针的相位从 -π 扫到 π，每个位置都做一次点积。"""
        offsets = np.linspace(-np.pi, np.pi, steps)
        theta = 2 * np.pi * freq * np.arange(len(x)) / sr
        probes = np.sin(theta + offsets[:, None])  # 每一行是一条相位不同的探针
        return offsets, 2 * (probes @ x) / len(x)

    return phase_scan, sin_cos_amp


@app.cell
def _(mo):
    PH_FREQ, PH_AMP, PH_DUR = 440.0, 0.8, 0.05  # 440 Hz，振幅 0.8，取 50 ms
    phi_ui = mo.ui.slider(
        0, 12, 1, value=2, label="目标的相位 φ = k × π/6，k =", show_value=True
    )
    return PH_AMP, PH_DUR, PH_FREQ, phi_ui


@app.cell
def _(PH_AMP, PH_DUR, PH_FREQ, fig_ax, mo, np, phi_ui, sine):
    _phi = phi_ui.value * np.pi / 6
    _t, _x = sine(PH_FREQ, dur=PH_DUR, amp=PH_AMP, phase=_phi)
    _probe = sine(PH_FREQ, dur=PH_DUR, amp=1.0)[1]
    _single = 2 * np.dot(_x, _probe) / len(_x)  # 只用一条正弦探针

    _n = 150
    _fig, _ax = fig_ax(
        title=f"φ = {_phi:.2f}　真实振幅 {PH_AMP}　单探针估计 {_single:+.2f}",
        ylim=(-1.35, 1.35),
    )
    _ax.plot(_t[:_n], _x[:_n], lw=3, color="black", label="目标")
    _ax.plot(_t[:_n], _probe[:_n], lw=1.5, color="tab:blue", alpha=0.85, label="正弦探针")
    _ax.axhline(_single, color="tab:green", lw=2.5, label="单探针估计")
    _ax.axhline(PH_AMP, color="black", ls=(0, (4, 3)), lw=1.5, label="真实振幅")
    _ax.legend(loc="lower left", ncol=2, fontsize=8)

    mo.vstack([phi_ui, _fig])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 笨办法：把探针转一圈

    既然只差一个"出发时刻"，那就把出发时刻挨个试一遍：让探针的相位从 $-\pi$ 转到 $\pi$，每转一点算一次点积，最后挑得分最高的那次。峰值的**高度**就是振幅，峰值的**位置**就是目标的相位。这种"一边滑动一边做点积"的操作叫**互相关**（cross-correlation）。

    办法确实管用，但有两个毛病。一是费劲：扫 M 个位置就得做 M 次点积。二是扫出来的曲线太整齐了，它是一条标准的余弦曲线（拖着滑块看，整条曲线只是左右平移，形状纹丝不动）。

    而一条余弦曲线，有"高度"和"位置"两个数就完全确定了。这说明我们辛辛苦苦做的 M 次点积里，真正的新信息只有两个数。那能不能跳过扫描，直接把这两个数算出来？
    """)
    return


@app.cell
def _(PH_AMP, PH_DUR, PH_FREQ, fig_ax, mo, np, phase_scan, phi_ui, sine):
    _phi = phi_ui.value * np.pi / 6
    _phi_wrapped = (_phi + np.pi) % (2 * np.pi) - np.pi  # 折到 -π ~ π
    _x = sine(PH_FREQ, dur=PH_DUR, amp=PH_AMP, phase=_phi)[1]

    _offsets, _curve = phase_scan(_x, PH_FREQ)
    _best = _offsets[np.argmax(_curve)]

    _fig, _ax = fig_ax(
        title=f"峰值 {np.max(_curve):.2f}（真实振幅 {PH_AMP}）　峰值位置 {_best:+.2f}（真实相位 {_phi_wrapped:+.2f}）",
        xlabel="探针的相位偏移（弧度）",
        ylabel="点积估计",
        ylim=(-1.1, 1.1),
    )
    _ax.plot(_offsets, _curve, lw=2.5, color="tab:blue")
    _ax.axvline(_best, color="tab:red", ls="--", lw=2, label="峰值位置")
    _ax.axhline(PH_AMP, color="black", ls=":", lw=1.5, label="真实振幅")
    _ax.legend(loc="lower left", fontsize=8)

    mo.vstack([phi_ui, _fig])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 聪明办法：两条探针就够了

    能，而且只要两次点积。靠的是一条中学三角公式：

    $$
    A\sin(\theta + \varphi) \;=\; \underbrace{A\cos\varphi}_{a}\,\sin\theta \;+\; \underbrace{A\sin\varphi}_{b}\,\cos\theta
    $$

    念出来就是：**不管相位是多少，一条正弦波总能写成"一份正弦加一份余弦"**，配比由 $a$、$b$ 两个数决定。而正弦和余弦这一对，正好是互相正交的（它们刚好错开四分之一周期），互不干扰。于是：

    - 拿**正弦探针**做一次点积，量到的就是 $a$；
    - 拿**余弦探针**做一次点积，量到的就是 $b$。

    有了这两个数，振幅和相位就一起有了：

    $$
    R = \sqrt{a^2+b^2}\;(=A), \qquad \varphi = \operatorname{atan2}(b,\,a)
    $$

    这两个式子眼熟吗？它就是**直角坐标转极坐标**。可以这样想：把 $a$ 当横坐标、$b$ 当纵坐标，在平面上点一个点，从原点画一支箭头指过去，那么

    - 箭头的**长度**就是振幅（勾股定理）；
    - 箭头的**角度**就是相位。

    下面右边那张图画的就是这支箭头。拖动滑块你会看到：箭头只是绕着原点转（相位在变），长度纹丝不动（振幅一直是 0.8）。左边是同一件事的波形版：蓝色 $a\times$正弦、橙色 $b\times$余弦，两条加起来（绿虚线）严丝合缝地盖住目标（灰色粗线）。

    回头看笨办法扫出来的那条余弦曲线，它其实就是 $A\cos(\varphi-\varphi')$：高度是箭头长度，峰值位置是箭头角度。信息确实只有两个数，扫一圈是白费力气。

    （两点小提醒：代码里要用 `atan2(b, a)` 而不是 `arctan(b/a)`，后者分不清箭头指向左上还是右下，相位会差一个 $\pi$；另外要让 $a$、$b$ 量得准，这一帧里得放得下若干个完整周期，这一点下一节会变成正式的约束。）
    """)
    return


@app.cell
def _(PH_AMP, PH_DUR, PH_FREQ, mo, np, phi_ui, plt, sin_cos_amp, sine):
    _phi = phi_ui.value * np.pi / 6
    _t, _x = sine(PH_FREQ, dur=PH_DUR, amp=PH_AMP, phase=_phi)
    _R, _phi_hat, _a, _b = sin_cos_amp(_x, PH_FREQ)

    _sin_p = sine(PH_FREQ, dur=PH_DUR, amp=1.0)[1]
    _cos_p = sine(PH_FREQ, dur=PH_DUR, amp=1.0, phase=np.pi / 2)[1]

    _n = 150
    _fig, (_ax, _ap) = plt.subplots(
        1, 2, figsize=(11, 4), gridspec_kw={"width_ratios": [2.1, 1]}
    )

    # 左：波形版
    _ax.plot(_t[:_n], _x[:_n], lw=5, color="0.65", label="目标")
    _ax.plot(_t[:_n], (_a * _sin_p)[:_n], lw=1.5, color="tab:blue", label=f"a × 正弦（a = {_a:+.2f}）")
    _ax.plot(_t[:_n], (_b * _cos_p)[:_n], lw=1.5, color="tab:orange", label=f"b × 余弦（b = {_b:+.2f}）")
    _ax.plot(_t[:_n], (_a * _sin_p + _b * _cos_p)[:_n], lw=1.5, ls="--", color="tab:green", label="两者相加")
    _ax.set_ylim(-1.35, 1.35)
    _ax.set_xlabel("时间（秒）")
    _ax.set_ylabel("振幅")
    _ax.set_title("波形版：目标 = a × 正弦 + b × 余弦")
    _ax.legend(loc="lower left", ncol=2, fontsize=8)

    # 右：箭头版（横坐标 a、纵坐标 b，箭头长度是振幅、角度是相位）
    _ap.axhline(0, color="0.8", lw=1)
    _ap.axvline(0, color="0.8", lw=1)
    _ap.add_patch(plt.Circle((0, 0), _R, fill=False, ls=":", lw=1, color="0.6"))
    _ap.plot([0, _a], [0, 0], color="tab:blue", ls="--", lw=1.2)
    _ap.plot([_a, _a], [0, _b], color="tab:orange", ls="--", lw=1.2)
    _ap.annotate("", xy=(_a, _b), xytext=(0, 0),
                 arrowprops=dict(arrowstyle="-|>", lw=2.5, color="tab:red"))
    _ap.set_xlim(-1.15, 1.15)
    _ap.set_ylim(-1.15, 1.15)
    _ap.set_aspect("equal")
    _ap.set_xlabel("a（正弦方向）")
    _ap.set_ylabel("b（余弦方向）")
    _ap.set_title(f"箭头版：长 {_R:.2f}，角 {_phi_hat:+.2f}")

    _table = mo.md(f"""
    | 量 | 数值 |
    |---|---|
    | a（和正弦探针的点积 × 2） | {_a:+.3f} |
    | b（和余弦探针的点积 × 2） | {_b:+.3f} |
    | 只用正弦探针 → 振幅 | {_a:+.3f}　随相位缩水 |
    | 两条探针 → $R=\\sqrt{{a^2+b^2}}$ | **{_R:.3f}**　真实值 {PH_AMP}，纹丝不动 |
    | 两条探针 → 相位 | {_phi_hat % (2 * np.pi):.3f}　真实值 {_phi % (2 * np.pi):.3f} |
    """)

    mo.vstack([phi_ui, _fig, _table])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    小结一下：**一个频率配一对探针（正弦 + 余弦），两次点积就同时拿到振幅和相位，事先完全不用知道相位。**

    数学上习惯把 $a$、$b$ 这一对数打包成一个**复数**，指的就是刚才那支箭头：长度给振幅，角度给相位。这也是为什么后面 DFT 的公式里会冒出复数，它不是什么高深的东西，只是"平面上一支箭头"的紧凑写法。这一对探针，正是 DFT 的基函数。
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec9"></a>

    ## 九、时间这道坎：把声音切成小段

    一首曲子里，每个音只响一会儿。对整段录音做一次点积，等于把从头到尾的所有变化揉成一个数，那当然没用。

    办法朴素得可爱：**切开来做**。像电影分格一样把声音切成一小段一小段（每段叫一**帧**），每帧单独做一次上面那套分析，再把结果按时间排好，就得到"某个频率的强度怎么随时间变化"。这就是**短时分析**，后面所有跟时间有关的东西都建在它上面。

    帧长要两头兼顾：

    - 太短：一帧里连几个完整周期都放不下，$a$、$b$ 量不准（低频尤其吃亏，因为它周期长）；
    - 太长：一帧里跨了好几个音，变化又被抹平了。

    22050 Hz 下取 1024 点（约 46 ms）是个常见折中：523 Hz 在这段时间里振动了二十多次，够量了；而 46 ms 又比一般音符短得多，不至于把两个音糊在一起。

    下面把第三节那段「1 2 3 1」（带包络的版本）切成帧，每帧用三对探针分别量 do、re、mi 的振幅。三条曲线一画出来，谁在什么时候响一目了然：第四节我们乘上去的那条 ADSR 包络，被原样量了回来。再往前一步，每帧挑最响的那个音，就是**音乐转录**（把录音变回乐谱）最朴素的雏形。
    """)
    return


@app.cell
def _(NOTES, SCORE, SR, fig_ax, melody_wet, mo, np, sin_cos_amp):
    def track_amplitude(x, freq, win=1024, hop=512, sr=SR):
        """逐帧估计某个频率的振幅：返回（每帧中心时刻, 每帧振幅）。"""
        starts = np.arange(0, len(x) - win + 1, hop)
        amps = np.array([sin_cos_amp(x[s : s + win], freq, sr)[0] for s in starts])
        return (starts + win / 2) / sr, amps

    _names = list(NOTES)
    _curves = []
    for _name in _names:
        _times, _amps = track_amplitude(melody_wet, NOTES[_name])
        _curves.append(_amps)
    _curves = np.array(_curves)

    _fig, _ax = fig_ax(title="逐帧量出来的三条振幅包络", ylabel="估出的振幅")
    for _name, _curve in zip(_names, _curves):
        _ax.plot(_times, _curve, lw=2, label=f"{_name}（{NOTES[_name]:.0f} Hz）")
    _ax.legend(loc="upper right", ncol=3, fontsize=9)

    # 每帧挑最响的那个音，再把连续重复的合并起来
    _seq, _prev = [], None
    for _loud, _pick in zip(_curves.max(axis=0) > 0.08, np.array(_names)[_curves.argmax(axis=0)]):
        if not _loud:
            _prev = None
        elif _pick != _prev:
            _seq.append(_pick)
            _prev = _pick

    mo.vstack([
        _fig,
        mo.md(f"逐帧挑最响的音、合并连续重复之后：**{' '.join(_seq)}**　（原谱 {' '.join(SCORE)}）"),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec10"></a>

    ## 十、探针的频率对不准会怎样

    到这里我们一直假设"频率已知"。可要是探针的频率和目标差了那么一点呢？

    结果很像调收音机：**对准了最清楚，偏一点就变弱，偏远了还会串台。**

    下面把探针固定在 200 Hz，让目标频率从 170 慢慢扫到 230，帧长 0.2 秒。正中间估得准，往两边一偏就迅速掉下去，再远一点还冒出一串小鼓包（那就是"串台"，专业叫**旁瓣**）。

    有意思的是主峰的宽度，它由**帧长**决定：帧长 $T$ 秒，第一个零点就落在偏差 $1/T$ 的地方。

    $$
    \text{能分辨的频率间隔} \;\approx\; \frac{1}{T} \;=\; \frac{f_s}{N}
    $$

    这件事其实你的耳朵早就知道。两个频率很接近的音同时响，会听到"哇……哇……"的忽强忽弱，这叫**拍音**，每秒晃动的次数正好等于两个频率之差。想听出这是**两个**音而不是一个，至少得听到一次完整的忽强忽弱，也就是听够 $1/\Delta f$ 秒：差 5 Hz 要听 0.2 秒，差 1 Hz 就得听满 1 秒。分析程序和耳朵受的是同一条限制。

    所以：帧取 0.2 秒（$N=4410$）能分辨约 5 Hz；帧取 46 ms（$N=1024$）就只剩 21.5 Hz 了，而低音区相邻两个半音才差 4 Hz 左右，那是彻底分不开的。**想在频率上看得细，就得在时间上看得粗**，这笔账会一直跟到最后一节的声谱图。

    （这条曲线的形状叫 Dirichlet 核，是"硬切一刀取一帧"所对应的频率响应。那些旁瓣，正是后面要给每帧"加窗"的原因。）
    """)
    return


@app.cell
def _(np, plt, sin_cos_amp, sine):
    _probe_freq, _amp, _dur = 200.0, 0.75, 0.2  # 帧长 0.2 秒 → 1/T = 5 Hz

    def _estimate(freq):
        return sin_cos_amp(sine(freq, dur=_dur, amp=_amp)[1], _probe_freq)[0]

    _fig, (_a1, _a2) = plt.subplots(1, 2, figsize=(11, 4), sharey=True)
    for _ax, _rng, _title in [
        (_a1, np.arange(195, 205.01, 0.1), "近处：主峰有多宽"),
        (_a2, np.arange(170, 230.01, 0.25), "远处：旁瓣"),
    ]:
        _ax.plot(_rng, [_estimate(f) for f in _rng], lw=2, color="tab:blue")
        _ax.axvline(_probe_freq, color="black", ls=":", lw=1.5)
        for _zero in (195, 205):
            _ax.axvline(_zero, color="tab:red", ls="--", lw=1.2)
        _ax.set_xlabel("目标频率（Hz）")
        _ax.set_title(_title)
    _a1.set_ylabel("估出的振幅")
    _a1.text(195.2, _amp * 0.55, "零点\n±1/T = ±5 Hz", fontsize=8, color="tab:red")

    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec11"></a>

    ## 十一、DFT 就是一整排探针

    现在把零件拼起来。

    一个频率要一对探针；想知道"所有频率上各有多少"，那就摆**一整排**探针对。这有点像在声音旁边摆一排调好音的音叉：哪个音叉跟着共振得厉害，就说明声音里有那个频率、有多少。

    排在哪些频率上？取一帧 $N$ 个采样，最自然的选法是让第 $k$ 对探针在这一帧里**正好走完 $k$ 个整周期**：

    $$
    \cos\Big(\frac{2\pi k n}{N}\Big),\qquad \sin\Big(\frac{2\pi k n}{N}\Big),\qquad k=0,1,\dots,N-1
    $$

    为什么非得"整周期"？因为这样一来，任意两条不同 $k$ 的探针互相做点积都等于 0，也就是**彼此正交**，谁也不干扰谁：属于某个频率的能量，不会漏进隔壁频率的读数里。（上一节那条曲线的零点，落的正是这些整周期频率的位置，两件事说的是同一回事。）

    第 $k$ 对探针对应的真实频率是

    $$
    f_k = k \cdot \frac{f_s}{N}
    $$

    相邻两条探针差 $f_s/N$，这和上一节的 $1/T$ 是同一个数，**频率分辨率**至此有了两种等价说法。

    最后，把每个 $k$ 的两个点积按第八节的办法打包成一支箭头（也就是一个复数），就得到教科书上那行公式：

    $$
    X_k = \sum_{n=0}^{N-1} x_n\, e^{-j 2\pi k n / N}
        = \underbrace{\sum_{n} x_n \cos\frac{2\pi k n}{N}}_{\text{余弦探针}}
        \;-\; j \underbrace{\sum_{n} x_n \sin\frac{2\pi k n}{N}}_{\text{正弦探针}}
    $$

    别被 $e$ 和 $j$ 吓到，把它拆开看，等号右边两项全是老朋友：一项是和余弦探针的点积，一项是和正弦探针的点积。这一排 $X_k$ 就是**离散傅里叶变换**（DFT）。读法是：

    - **振幅**：$A_k = \dfrac{2\,|X_k|}{N}$，也就是箭头的长度（那个 2 和前面点积估计里的 2 是同一个；除以 $N$ 是因为求和没有取平均）
    - **相位**：$\arg X_k$，箭头的角度（它以余弦为参照，和我们前面拿正弦当参照差 $\pi/2$）
    - **只用看前一半**：$k$ 超过 $N/2$ 之后的读数只是前一半的镜像，没有新东西。这条分界线 $f_s/2$ 就叫**奈奎斯特频率**，也正是"采样率要取到最高频率的两倍以上"这条规矩的由来（第一节欠的账，在这里还上了）。另外 $k=0$ 是直流、$k=N/2$ 是奈奎斯特，这两条没有配对的另一半，所以不乘 2。

    下面先看看这些基函数长什么样：$k$ 越大，一帧里塞进的周期越多，频率也就越高。
    """)
    return


@app.cell
def _(np, plt):
    _N = 512
    _n = np.arange(_N)

    _fig, _axes = plt.subplots(3, 1, figsize=(9, 6), sharex=True)
    for _ax, _k in zip(_axes, [1, 4, 10]):
        _ax.plot(_n, np.cos(2 * np.pi * _k * _n / _N), lw=1.5, label="余弦探针")
        _ax.plot(_n, np.sin(2 * np.pi * _k * _n / _N), lw=1.5, label="正弦探针")
        _ax.set_ylabel(f"k = {_k}")
        _ax.set_ylim(-1.5, 1.5)
    _axes[0].set_title("DFT 的基函数：第 k 对探针在一帧里正好走完 k 个周期")
    _axes[0].legend(loc="upper right", ncol=2, fontsize=8)
    _axes[-1].set_xlabel("帧内采样点 n（N = 512）")

    _fig
    return


@app.cell
def _(SR, np):
    def dft_slow(x):
        """照定义算 DFT：对每个 k 做一对点积（余弦一次、正弦一次）。"""
        N = len(x)
        n = np.arange(N)
        re, im = np.zeros(N), np.zeros(N)
        for k in range(N):
            theta = 2 * np.pi * k * n / N
            re[k] = np.dot(x, np.cos(theta))
            im[k] = np.dot(x, np.sin(theta))
        return re, im

    def amp_spectrum(x, sr=SR):
        """用 FFT 算振幅谱，返回（频率 Hz, 振幅）。只保留前一半。"""
        N = len(x)
        mag = np.abs(np.fft.rfft(x)) * 2 / N
        mag[0] /= 2  # 直流不成对，不该乘 2
        if N % 2 == 0:
            mag[-1] /= 2  # 奈奎斯特分量同理
        return np.fft.rfftfreq(N, 1 / sr), mag

    return amp_spectrum, dft_slow


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    拿一个三分音的谐波音来试：三个分量的振幅是 0.8、0.4、0.2，频率正好落在第 6、12、24 对探针上。左图就是它的振幅谱，三根干净利落的线，高度分毫不差地把三个振幅还原了出来。

    右图把三个分量整体挪了半格（落到 $k=6.5, 12.5, 24.5$），也就是让它们卡在两条探针**中间**。这下没有哪条探针能对准，能量被涂抹到左邻右舍身上，这叫**频谱泄漏**。原因还是上一节那条曲线：频率对不准，读数就打折，还得漏一部分给旁瓣。

    真实世界的声音几乎不可能正好落在格子上，所以泄漏是常态。实用的对策是给每帧乘一条两头渐弱的**窗函数**（例如 Hann 窗），相当于让这一帧轻轻地淡入淡出，而不是硬切一刀。代价是主峰稍微变宽，好处是旁瓣被压得很低。
    """)
    return


@app.cell
def _(SR, amp_spectrum, dft_slow, mo, np, plt):
    _N = 512
    _n = np.arange(_N)

    def _tone(ks):
        return sum(a * np.sin(2 * np.pi * k * _n / _N) for k, a in zip(ks, [0.8, 0.4, 0.2]))

    _on, _off = _tone([6, 12, 24]), _tone([6.5, 12.5, 24.5])

    # 自己照定义算一遍，和 numpy 的 FFT 对一下
    _re, _im = dft_slow(_on)
    _mine = 2 * np.hypot(_re, _im) / _N
    _hz, _theirs = amp_spectrum(_on)
    _gap = np.max(np.abs(_mine[: len(_theirs)] - _theirs))

    _fig, (_a1, _a2) = plt.subplots(1, 2, figsize=(11, 4), sharey=True)
    for _ax, _mag, _title in [
        (_a1, _theirs, "正好落在探针上：三根干净的线"),
        (_a2, amp_spectrum(_off)[1], "挪半格：能量涂开了（频谱泄漏）"),
    ]:
        _markers, _stems, _ = _ax.stem(_hz[:40], _mag[:40], basefmt=" ")
        plt.setp(_stems, lw=1.5)
        plt.setp(_markers, ms=4)
        _ax.set_xlabel("频率（Hz）")
        _ax.set_title(_title)
    _a1.set_ylabel("估出的振幅")

    mo.vstack([
        _fig,
        mo.md(
            f"每条探针之间差 $f_s/N$ = {SR / _N:.1f} Hz。"
            f"照定义手算的振幅谱和 `np.fft.fft` 的结果最大相差 {_gap:.1e}，同一件事的两种写法。"
        ),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 那 FFT 又是什么？

    很多人以为 FFT 是另一种变换，其实不是：**它就是 DFT，只是换了一种算得飞快的算法。**

    上面的 `dft_slow` 是照定义老实算的：$N$ 个频率，每个都要做一对长度 $N$ 的点积，加起来约 $N^2$ 次乘加。而**快速傅里叶变换**（FFT）注意到这些探针之间有大量重复和对称（比如第 $k$ 对探针和第 $k+N/2$ 对，取值逐点只差一个正负号），于是把算过的中间结果反复利用，复杂度降到 $N\log N$。

    算出来的结果和定义式一模一样（上面那点微小差距纯粹是浮点误差）。它只是算得快，而正因为快，实时音频分析才成为可能。
    """)
    return


@app.cell
def _(dft_slow, mo, np):
    import time

    _x = np.random.default_rng(0).normal(0, 1, 1024)

    _t0 = time.perf_counter()
    dft_slow(_x)
    _slow = time.perf_counter() - _t0

    _reps = 200
    _t0 = time.perf_counter()
    for _ in range(_reps):
        np.fft.fft(_x)
    _fast = (time.perf_counter() - _t0) / _reps

    mo.md(f"""
    | N = 1024，算一次 | 耗时 |
    |---|---|
    | 照定义算（1024 对点积） | {_slow * 1000:.1f} ms |
    | `np.fft.fft` | {_fast * 1000:.3f} ms |

    这台机器上快了约 **{_slow / _fast:.0f} 倍**（这里面既有算法的功劳，也有 Python 逐个频率循环本身的开销）。
    光看乘加次数：$N^2 \\approx 10^6$ 对 $N\\log_2 N \\approx 10^4$，差两个数量级，而且 $N$ 越大差得越多。
    这就是为什么实际代码里永远只见 FFT。
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 真实声音的频谱

    终于可以对真家伙下手了。取小号录音中段的一帧（4096 点，约 186 ms），乘上 Hann 窗，做一次 FFT：

    一根根等距排开的尖峰，就是第五节讲过的**谐波列**，间隔等于基频。乐器的音色，说白了就是这些谐波的高低比例；把这张图和第五节那三个滑块对着看，加法合成和频谱分析其实是同一件事的两个方向。

    （加了窗之后整体幅度会打个折扣：Hann 窗的平均值是 0.5，需要绝对数值时乘 2 补回来。这里只看相对高低，就不折腾了。）
    """)
    return


@app.cell
def _(SR, amp_spectrum, fig_ax, np, trumpet):
    _N = 4096
    _start = len(trumpet) // 3  # 取中间一段，避开开头的起音
    _frame = trumpet[_start : _start + _N] * np.hanning(_N)
    _hz, _mag = amp_spectrum(_frame)

    # 最低的那个显著峰当作基频
    _is_peak = np.r_[False, (_mag[1:-1] > _mag[:-2]) & (_mag[1:-1] > _mag[2:]), False]
    _cands = _hz[_is_peak & (_mag > 0.1 * _mag.max()) & (_hz > 80)]
    _f0 = _cands[0] if len(_cands) else _hz[np.argmax(_mag)]

    _keep = _hz <= 4000
    _fig, _ax = fig_ax(
        title=f"小号一帧（{_N} 点 ≈ {_N / SR * 1000:.0f} ms）的振幅谱：基频约 {_f0:.0f} Hz，虚线是整数倍",
        xlabel="频率（Hz）",
        ylabel="振幅（相对）",
    )
    _ax.plot(_hz[_keep], _mag[_keep], lw=1.2, color="tab:blue")
    for _i in range(1, int(4000 / _f0) + 1):
        _ax.axvline(_f0 * _i, color="tab:red", ls=":", lw=1, alpha=0.7)
    _ax.set_ylim(bottom=0)

    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec12"></a>

    ## 十二、声谱图：把两道坎一起跨过去

    第九节的"切成帧"，加上第十一节的"一整排探针"，合起来就是**短时傅里叶变换**（STFT）：

    > 切一帧 → 乘上窗 → 做一次 FFT → 得到一列频谱 → 挪到下一帧

    每一帧给出一列数，写的是"这一小段时间里，各个频率上各有多少"。把这些列按时间顺序并排贴起来，用颜色深浅表示强弱，就是**声谱图**（spectrogram）：横轴时间，纵轴频率，亮的地方表示"这个时刻这个频率上有能量"。某种意义上，它就是机器自动记下来的一份乐谱。音乐信息检索里几乎一切都从这张图开始：识别音高、跟和弦、找节拍、分离人声。

    下面这张是小号录音的声谱图。换一下帧长，能直接看到第十节那个矛盾：

    - **256 点**：横向刀切一样利落，音的起始点清清楚楚；但纵向糊成一片，谐波挤在一起（分辨率只有 86 Hz）；
    - **4096 点**：谐波一根根分得清清楚楚（分辨率 5.4 Hz）；但换音的瞬间被抹成一段渐变。

    没有哪个更“对”，要看你想看什么。这就是时间与频率之间那笔永远付不清的账。
    """)
    return


@app.cell
def _(mo):
    win_ui = mo.ui.dropdown(
        options={
            "256 点（约 12 ms）": 256,
            "1024 点（约 46 ms）": 1024,
            "4096 点（约 186 ms）": 4096,
        },
        value="1024 点（约 46 ms）",
        label="每帧的长度",
    )
    return (win_ui,)


@app.cell
def _(SR, mo, np, plt, trumpet, win_ui):
    def stft_mag(x, win, hop, sr=SR):
        """短时傅里叶变换：逐帧加窗做 FFT，返回（时刻, 频率, 幅度矩阵）。"""
        window = np.hanning(win)
        starts = np.arange(0, len(x) - win + 1, hop)
        frames = np.stack([x[s : s + win] * window for s in starts])
        spec = np.abs(np.fft.rfft(frames, axis=1)) * 2 / win
        return (starts + win / 2) / sr, np.fft.rfftfreq(win, 1 / sr), spec.T

    _win = win_ui.value
    _times, _freqs, _spec = stft_mag(trumpet, _win, max(_win // 4, 64))

    _keep = _freqs <= 4000
    _db = 20 * np.log10(_spec[_keep] / _spec.max() + 1e-6)

    _fig, _ax = plt.subplots(figsize=(9, 4))
    _img = _ax.imshow(
        _db,
        origin="lower",
        aspect="auto",
        cmap="magma",
        vmin=-60,
        vmax=0,
        extent=[_times[0], _times[-1], 0, _freqs[_keep][-1]],
    )
    _ax.set_xlabel("时间（秒）")
    _ax.set_ylabel("频率（Hz）")
    _ax.set_title(f"小号的声谱图：每帧 {_win} 点，频率分辨率 {SR / _win:.1f} Hz")
    _fig.colorbar(_img, ax=_ax, label="相对强度（dB）")

    mo.vstack([win_ui, _fig])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec-end"></a>

    ## 收个尾

    从头到尾，我们只用了两样东西：**正弦波**，和**点积**。

    - 正弦波三个数就说完：振幅、频率、相位。把它们叠起来，能造出乐音、旋律、钟声和芯片音乐；
    - 反过来要拆解，一次点积就是一次提问：“这段声音里有多少成分长得像我这条探针？”
    - 相位对不上？一个频率配一对正弦／余弦探针，振幅和相位一次算清；
    - 频率不知道？把探针排成一整排，得到的就是频谱，这排点积就是 DFT，FFT 只是算得飞快的同一件事；
    - 声音在变？切成帧，逐帧来一次，得到声谱图。

    再往后的路都从这张图出发：音高与旋律提取、和弦识别、节拍跟踪、音源分离、音频指纹，还有各种音频神经网络的输入特征。回头看，起点真的只是一条正弦波。
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a id="sec-ref"></a>

    ## 其他参考资料

    **本文来源**

    - George Tzanetakis, [synthesizers_cs_perspective](https://github.com/gtzan/synthesizers_cs_perspective)：英文原文的配套 Jupyter 笔记本与代码仓库
    - [THX 片头音效的 Python 实现](https://musicinformationretrieval.com/content/11_fun/thx_logo_theme.html)：几百条正弦波随时间改变频率和振幅，本文的手法用到极致就是它

    **想把傅里叶再往深处啃**

    - 3Blue1Brown, [But what is the Fourier Transform? A visual introduction](https://www.youtube.com/watch?v=spUNpyF58BY)：从“绕圈”的角度看同一件事
    - Julius O. Smith, [Mathematics of the Discrete Fourier Transform](https://ccrma.stanford.edu/~jos/mdft/)：想要严格推导的话看这本
    - Meinard Müller, [Fundamentals of Music Processing](https://www.audiolabs-erlangen.de/fau/professor/mueller/bookFMP)：从声谱图一路讲到各种音乐信息检索任务，配套 Python 笔记本
    - [musicinformationretrieval.com](https://musicinformationretrieval.com/)：大量可以直接跑的音频分析示例

    **可以写代码的音乐工具**

    - [CSound](https://csound.com/)、[SuperCollider](https://supercollider.github.io/)、[ChucK](https://chuck.stanford.edu/)
    - 拖模块连线的：[Max](https://cycling74.com/products/max)、[PureData](https://puredata.info/)、[VCV Rack](https://vcvrack.com/)
    - 做音乐的：[Renoise](https://www.renoise.com/)、[Logic](https://www.apple.com/ca/logic-pro/)、[Ableton Live](https://www.ableton.com/en/live/)、[Reaper](https://www.reaper.fm/)

    **芯片音乐**

    - [BeepBox](https://www.beepbox.co/)：浏览器里就能写
    - [Battle of the Bits](https://battleofthebits.com/)、[Furnace](https://github.com/tildearrow/furnace)
    """)
    return


@app.cell(hide_code=True)
def _():
    import marimo as mo

    return (mo,)


if __name__ == "__main__":
    app.run()
