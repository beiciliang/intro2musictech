import marimo

__generated_with = "0.19.11"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 2026年，用 Claude Code 就可以无痛入门音乐科技

    想象一下：你在终端输入一句话，AI 就帮你写好代码、画好图、还能交互式调参——这就是2026年用 **Claude Code** 学音乐科技的体验。

    本文用 **marimo** 交互式笔记本来模拟一场与 Claude Code 的「结对编程」。每一节都以你可能会问 Claude Code 的问题开头，然后给出可直接运行的代码和交互式控件。

    > **如何运行本笔记本？**
    >
    > ```bash
    > uv sync
    > uv run marimo edit MIR-CC.py
    > ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(
        mo.md(
            """
            **什么是 Claude Code？**

            [Claude Code](https://docs.anthropic.com/en/docs/claude-code) 是 Anthropic 推出的命令行 AI 编程助手。
            你只需要在终端用自然语言描述需求，它就能帮你编写、调试和运行代码——非常适合零基础学习者快速上手编程。
            """
        ),
        kind="info",
    )
    return


@app.cell
def _():
    from pathlib import Path

    import librosa
    import librosa.display
    import marimo as mo
    import matplotlib.pyplot as plt
    import numpy as np

    ATTACHMENT = Path(__file__).parent / "attachment"
    return ATTACHMENT, librosa, mo, np, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Part 1: 加载音频并试听

    > **🧑 你对 Claude Code 说：** "帮我加载猫叫音频，让我听一下"
    """)
    return


@app.cell
def _(ATTACHMENT, librosa, mo):
    cat_audio_path = ATTACHMENT / "cat-meow.mp3"
    y_cat, sr_cat = librosa.load(cat_audio_path, sr=None)
    duration_cat = librosa.get_duration(y=y_cat, sr=sr_cat)

    mo.md(
        f"""
        **音频信息：**
        - 文件：`cat-meow.mp3`
        - 采样率：{sr_cat} Hz
        - 时长：{duration_cat:.2f} 秒
        - 采样点数：{len(y_cat):,}
        """
    )
    return sr_cat, y_cat


@app.cell
def _(ATTACHMENT, mo):
    mo.audio(src=ATTACHMENT / "cat-meow.mp3")
    return


@app.cell
def _(librosa, plt, sr_cat, y_cat):
    fig_wave, ax_wave = plt.subplots(figsize=(10, 3))
    librosa.display.waveshow(y_cat, sr=sr_cat, ax=ax_wave, color="#4a90d9")
    ax_wave.set_title("Cat Meow — Waveform", fontsize=14)
    ax_wave.set_xlabel("Time (s)")
    ax_wave.set_ylabel("Amplitude")
    plt.tight_layout()
    fig_wave
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Part 2: 交互式短时傅里叶变换 (STFT)

    > **🧑 你对 Claude Code 说：** "我想看频域表示，而且想自己调参数"
    """)
    return


@app.cell
def _(mo):
    audio_files = {
        "🐱 猫叫 cat-meow.mp3": "cat-meow.mp3",
        "🎵 音乐 mir01-music-example.wav": "mir01-music-example.wav",
        "🥁 咚哒 mir02-dongda.wav": "mir02-dongda.wav",
        "🎻 频谱质心 mir02-centroidaudio.wav": "mir02-centroidaudio.wav",
        "🎼 双簧管C6 mir02-oboe_C6_1046Hz.wav": "mir02-oboe_C6_1046Hz.wav",
    }
    file_dropdown = mo.ui.dropdown(
        options=audio_files,
        value="🐱 猫叫 cat-meow.mp3",
        label="选择音频文件",
    )
    file_dropdown
    return (file_dropdown,)


@app.cell
def _(ATTACHMENT, file_dropdown, librosa, mo):
    selected_path = ATTACHMENT / file_dropdown.value
    y_sel, sr_sel = librosa.load(selected_path, sr=22050)
    dur_sel = librosa.get_duration(y=y_sel, sr=sr_sel)
    mo.md(
        f"已加载 **{file_dropdown.value}** — 采样率 {sr_sel} Hz，时长 {dur_sel:.2f} 秒"
    )
    return sr_sel, y_sel


@app.cell
def _(mo):
    nfft_slider = mo.ui.slider(
        start=256,
        stop=4096,
        step=256,
        value=2048,
        label="n_fft（窗口长度）",
        show_value=True,
    )
    hop_slider = mo.ui.slider(
        start=64,
        stop=2048,
        step=64,
        value=512,
        label="hop_length（步长）",
        show_value=True,
    )
    mo.vstack(
        [
            nfft_slider,
            hop_slider,
            mo.callout(
                mo.md(
                    """
                    **Claude Code 小贴士 — 时频分辨率权衡：**
                    `n_fft` 越大，频率分辨率越高，但时间分辨率越低；`hop_length` 越小，时间分辨率越高，但计算量越大。试着拖动滑块感受这个 trade-off！
                    """
                ),
                kind="warn",
            ),
        ]
    )
    return hop_slider, nfft_slider


@app.cell
def _(hop_slider, librosa, nfft_slider, np, plt, sr_sel, y_sel):
    n_fft_val = nfft_slider.value
    hop_val = hop_slider.value

    fig_stft, axes_stft = plt.subplots(2, 1, figsize=(10, 6), sharex=True)

    # Waveform
    librosa.display.waveshow(y_sel, sr=sr_sel, ax=axes_stft[0], color="#4a90d9")
    axes_stft[0].set_title("Waveform", fontsize=12)
    axes_stft[0].set_ylabel("Amplitude")

    # STFT spectrogram
    S = np.abs(librosa.stft(y_sel, n_fft=n_fft_val, hop_length=hop_val))
    S_db = librosa.amplitude_to_db(S, ref=np.max)
    img = librosa.display.specshow(
        S_db,
        sr=sr_sel,
        hop_length=hop_val,
        x_axis="time",
        y_axis="hz",
        ax=axes_stft[1],
        cmap="magma",
    )
    axes_stft[1].set_title(
        f"STFT Spectrogram (n_fft={n_fft_val}, hop_length={hop_val})", fontsize=12
    )
    axes_stft[1].set_ylabel("Frequency (Hz)")
    axes_stft[1].set_xlabel("Time (s)")
    fig_stft.colorbar(img, ax=axes_stft[1], format="%+2.0f dB")
    plt.tight_layout()
    fig_stft
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Part 3: Mel 频谱图

    > **🧑 你对 Claude Code 说：** "人耳对频率的感知不是线性的，有更适合的频谱图吗？"
    """)
    return


@app.cell
def _(mo):
    n_mels_slider = mo.ui.slider(
        start=16,
        stop=256,
        step=16,
        value=128,
        label="n_mels（Mel 滤波器组数量）",
        show_value=True,
    )
    n_mels_slider
    return (n_mels_slider,)


@app.cell
def _(hop_slider, librosa, n_mels_slider, nfft_slider, np, plt, sr_sel, y_sel):
    n_fft_mel = nfft_slider.value
    hop_mel = hop_slider.value
    n_mels_val = n_mels_slider.value

    fig_mel, axes_mel = plt.subplots(1, 2, figsize=(14, 4))

    # Linear spectrogram (left)
    S_lin = np.abs(librosa.stft(y_sel, n_fft=n_fft_mel, hop_length=hop_mel))
    S_lin_db = librosa.amplitude_to_db(S_lin, ref=np.max)
    img_lin = librosa.display.specshow(
        S_lin_db,
        sr=sr_sel,
        hop_length=hop_mel,
        x_axis="time",
        y_axis="hz",
        ax=axes_mel[0],
        cmap="magma",
    )
    axes_mel[0].set_title("Linear Spectrogram", fontsize=12)
    fig_mel.colorbar(img_lin, ax=axes_mel[0], format="%+2.0f dB")

    # Mel spectrogram (right)
    M = librosa.feature.melspectrogram(
        y=y_sel, sr=sr_sel, n_fft=n_fft_mel, hop_length=hop_mel, n_mels=n_mels_val
    )
    M_db = librosa.power_to_db(M, ref=np.max)
    img_mel = librosa.display.specshow(
        M_db,
        sr=sr_sel,
        hop_length=hop_mel,
        x_axis="time",
        y_axis="mel",
        ax=axes_mel[1],
        cmap="magma",
    )
    axes_mel[1].set_title(f"Mel Spectrogram (n_mels={n_mels_val})", fontsize=12)
    fig_mel.colorbar(img_mel, ax=axes_mel[1], format="%+2.0f dB")

    plt.tight_layout()
    fig_mel
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Part 4: 实用 MIR 任务

    > **🧑 你对 Claude Code 说：** "能自动找到鼓点位置吗？"
    """)
    return


@app.cell
def _(ATTACHMENT, librosa, np, plt):
    y_drum, sr_drum = librosa.load(ATTACHMENT / "mir02-dongda.wav", sr=22050)
    onset_frames = librosa.onset.onset_detect(y=y_drum, sr=sr_drum)
    onset_times = librosa.frames_to_time(onset_frames, sr=sr_drum)

    fig_onset, ax_onset = plt.subplots(figsize=(10, 3))
    librosa.display.waveshow(y_drum, sr=sr_drum, ax=ax_onset, color="#4a90d9", alpha=0.6)
    ax_onset.vlines(
        onset_times, -1, 1, color="red", linewidth=1.5, alpha=0.8, label="Detected onsets"
    )
    ax_onset.legend(fontsize=10)
    ax_onset.set_title(
        f"Onset Detection — {len(onset_times)} onsets found", fontsize=12
    )
    ax_onset.set_xlabel("Time (s)")
    ax_onset.set_ylabel("Amplitude")
    ymin = float(np.min(y_drum)) * 1.1
    ymax = float(np.max(y_drum)) * 1.1
    ax_onset.set_ylim(ymin, ymax)
    plt.tight_layout()
    fig_onset
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **🧑 你对 Claude Code 说：** "能显示音乐的色度图吗？我想比较不同算法"
    """)
    return


@app.cell
def _(ATTACHMENT, librosa, mo):
    y_music, sr_music = librosa.load(
        ATTACHMENT / "mir01-music-example.wav", sr=22050
    )

    chroma_type_dropdown = mo.ui.dropdown(
        options=["stft", "cqt", "cens"],
        value="stft",
        label="Chroma 算法",
    )
    chroma_type_dropdown
    return chroma_type_dropdown, sr_music, y_music


@app.cell
def _(chroma_type_dropdown, librosa, plt, sr_music, y_music):
    chroma_funcs = {
        "stft": lambda: librosa.feature.chroma_stft(y=y_music, sr=sr_music),
        "cqt": lambda: librosa.feature.chroma_cqt(y=y_music, sr=sr_music),
        "cens": lambda: librosa.feature.chroma_cens(y=y_music, sr=sr_music),
    }
    chroma_data = chroma_funcs[chroma_type_dropdown.value]()

    fig_chroma, ax_chroma = plt.subplots(figsize=(10, 4))
    img_chroma = librosa.display.specshow(
        chroma_data,
        y_axis="chroma",
        x_axis="time",
        sr=sr_music,
        ax=ax_chroma,
        cmap="coolwarm",
    )
    ax_chroma.set_title(
        f"Chromagram ({chroma_type_dropdown.value})", fontsize=12
    )
    fig_chroma.colorbar(img_chroma, ax=ax_chroma)
    plt.tight_layout()
    fig_chroma
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **🧑 你对 Claude Code 说：** "能在频谱图上叠加频谱质心曲线吗？"
    """)
    return


@app.cell
def _(hop_slider, librosa, nfft_slider, np, plt, sr_sel, y_sel):
    n_fft_sc = nfft_slider.value
    hop_sc = hop_slider.value

    S_sc = np.abs(librosa.stft(y_sel, n_fft=n_fft_sc, hop_length=hop_sc))
    S_sc_db = librosa.amplitude_to_db(S_sc, ref=np.max)
    centroid = librosa.feature.spectral_centroid(
        y=y_sel, sr=sr_sel, n_fft=n_fft_sc, hop_length=hop_sc
    )
    times_sc = librosa.times_like(centroid, sr=sr_sel, hop_length=hop_sc)

    fig_sc, ax_sc = plt.subplots(figsize=(10, 4))
    librosa.display.specshow(
        S_sc_db,
        sr=sr_sel,
        hop_length=hop_sc,
        x_axis="time",
        y_axis="hz",
        ax=ax_sc,
        cmap="magma",
    )
    ax_sc.plot(times_sc, centroid[0], color="cyan", linewidth=2, label="Spectral Centroid")
    ax_sc.legend(loc="upper right", fontsize=10)
    ax_sc.set_title("Spectral Centroid Overlay", fontsize=12)
    ax_sc.set_ylabel("Frequency (Hz)")
    ax_sc.set_xlabel("Time (s)")
    plt.tight_layout()
    fig_sc
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Part 5: 特征仪表盘

    > **🧑 你对 Claude Code 说：** "能做一个仪表盘一次看所有特征吗？"
    """)
    return


@app.cell
def _(hop_slider, librosa, mo, nfft_slider, np, plt, sr_sel, y_sel):
    _n_fft = nfft_slider.value
    _hop = hop_slider.value

    def _make_tab_figure(title, plot_fn):
        fig, ax = plt.subplots(figsize=(10, 4))
        plot_fn(fig, ax)
        ax.set_title(title, fontsize=12)
        ax.set_xlabel("Time (s)")
        plt.tight_layout()
        return fig

    def _plot_waveform(fig, ax):
        librosa.display.waveshow(y_sel, sr=sr_sel, ax=ax, color="#4a90d9")
        ax.set_ylabel("Amplitude")

    def _plot_spectrogram(fig, ax):
        S = np.abs(librosa.stft(y_sel, n_fft=_n_fft, hop_length=_hop))
        S_db = librosa.amplitude_to_db(S, ref=np.max)
        img = librosa.display.specshow(
            S_db, sr=sr_sel, hop_length=_hop, x_axis="time", y_axis="hz",
            ax=ax, cmap="magma",
        )
        ax.set_ylabel("Frequency (Hz)")
        fig.colorbar(img, ax=ax, format="%+2.0f dB")

    def _plot_mel(fig, ax):
        M = librosa.feature.melspectrogram(
            y=y_sel, sr=sr_sel, n_fft=_n_fft, hop_length=_hop,
        )
        M_db = librosa.power_to_db(M, ref=np.max)
        img = librosa.display.specshow(
            M_db, sr=sr_sel, hop_length=_hop, x_axis="time", y_axis="mel",
            ax=ax, cmap="magma",
        )
        ax.set_ylabel("Mel Frequency")
        fig.colorbar(img, ax=ax, format="%+2.0f dB")

    def _plot_chroma(fig, ax):
        C = librosa.feature.chroma_stft(y=y_sel, sr=sr_sel, n_fft=_n_fft, hop_length=_hop)
        img = librosa.display.specshow(
            C, y_axis="chroma", x_axis="time", sr=sr_sel, hop_length=_hop,
            ax=ax, cmap="coolwarm",
        )
        fig.colorbar(img, ax=ax)

    def _plot_mfcc(fig, ax):
        mfccs = librosa.feature.mfcc(
            y=y_sel, sr=sr_sel, n_mfcc=13, n_fft=_n_fft, hop_length=_hop,
        )
        img = librosa.display.specshow(
            mfccs, x_axis="time", sr=sr_sel, hop_length=_hop, ax=ax,
        )
        ax.set_ylabel("MFCC Coefficients")
        fig.colorbar(img, ax=ax)

    def _plot_centroid_zcr(fig, ax):
        cent = librosa.feature.spectral_centroid(
            y=y_sel, sr=sr_sel, n_fft=_n_fft, hop_length=_hop,
        )
        zcr = librosa.feature.zero_crossing_rate(y_sel, frame_length=_n_fft, hop_length=_hop)
        t = librosa.times_like(cent, sr=sr_sel, hop_length=_hop)
        ax.plot(t, cent[0], color="#e74c3c", label="Spectral Centroid (Hz)", linewidth=1.5)
        ax.set_ylabel("Spectral Centroid (Hz)", color="#e74c3c")
        ax.tick_params(axis="y", labelcolor="#e74c3c")
        ax2 = ax.twinx()
        ax2.plot(t, zcr[0], color="#2ecc71", label="Zero Crossing Rate", linewidth=1.5)
        ax2.set_ylabel("Zero Crossing Rate", color="#2ecc71")
        ax2.tick_params(axis="y", labelcolor="#2ecc71")
        lines1, labels1 = ax.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax.legend(lines1 + lines2, labels1 + labels2, loc="upper right")

    dashboard_tabs = mo.ui.tabs(
        {
            "Waveform": _make_tab_figure("Waveform", _plot_waveform),
            "Spectrogram": _make_tab_figure("Spectrogram", _plot_spectrogram),
            "Mel Spectrogram": _make_tab_figure("Mel Spectrogram", _plot_mel),
            "Chromagram": _make_tab_figure("Chromagram", _plot_chroma),
            "MFCC": _make_tab_figure("MFCC", _plot_mfcc),
            "Centroid + ZCR": _make_tab_figure("Spectral Centroid & ZCR", _plot_centroid_zcr),
        }
    )
    dashboard_tabs
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 回顾与下一步

    在这篇文章中，我们用 Claude Code + marimo 交互式笔记本完成了以下 MIR 任务：

    1. **加载和试听**音频文件
    2. 用交互式滑块探索 **STFT 时频分析**的参数影响
    3. 对比**线性频谱图 vs Mel 频谱图**
    4. 自动检测**鼓点位置**（Onset Detection）
    5. 比较不同 **Chromagram** 算法
    6. 叠加**频谱质心**曲线
    7. 一键查看**特征仪表盘**

    ### 试着问 Claude Code 更多问题：

    - "帮我实现一个简单的节拍追踪器"
    - "用 MFCC 特征做一个音频分类器"
    - "帮我把两段音频的频谱图放在一起对比"
    - "什么是谐波打击乐分离？帮我实现一下"
    - "帮我用 librosa 提取音频的调性"
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ### 相关链接

    | 资源 | 链接 |
    |------|------|
    | 往期文章 | [无痛入门音乐科技](https://github.com/beiciliang/intro2musictech) |
    | marimo 文档 | [docs.marimo.io](https://docs.marimo.io) |
    | Claude Code | [docs.anthropic.com/en/docs/claude-code](https://docs.anthropic.com/en/docs/claude-code) |
    | librosa 文档 | [librosa.org](https://librosa.org) |

    欢迎微信关注公众号 **「无痛入门音乐科技」**
    """)
    return


if __name__ == "__main__":
    app.run()
