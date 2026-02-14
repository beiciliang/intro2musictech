# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Educational Jupyter Notebook tutorials on Music Information Retrieval (MIR) and music technology fundamentals. Accompanies the Chinese WeChat public account "无痛入门音乐科技". Target audience is beginners with no programming background.

This is **not** a production service — it is purely educational content that runs locally in notebooks.

## Setup & Running

```bash
# Install dependencies
uv sync

# Launch notebooks
uv run jupyter notebook
```

Validate setup by running all cells in `00-Hello.ipynb`.

Verify a notebook executes cleanly:
```bash
uv run jupyter nbconvert --to notebook --execute <notebook.ipynb>
```

## Core Dependencies

- **librosa** — audio and music analysis
- **numpy / scipy** — numerical computing
- **matplotlib** — visualization
- **scikit-learn** — machine learning utilities

## Repository Structure

- `00-Hello.ipynb` — setup validation and Jupyter intro
- `MIR-01.ipynb` — music visualization basics
- `MIR-02_*.ipynb` — audio feature extraction series (time-domain, frequency-domain, musical features)
- `MIR-CC.py` — interactive Claude Code + MIR tutorial (marimo notebook, run with `uv run marimo edit MIR-CC.py`)
- `attachment/` — audio samples (.wav, .mp3) and educational images used by notebooks
- `INFO-ResearchGroups.md` — curated list of MIR research groups worldwide
- `README.md` — detailed setup guide and index of articles with publication dates

## Content Conventions

- Notebooks are self-contained tutorials with Markdown explanations and inline comments **in Chinese**
- Each notebook corresponds to a WeChat article linked in the README table
- Audio/image assets go in `attachment/`
- Progressive complexity: start from `00-Hello`, then `MIR-01`, then `MIR-02_*` series
- No formal test suite — notebooks validate themselves through visible output (plots, audio playback)
- No CI/CD pipeline

## Adding a New Tutorial

1. Create a new `.ipynb` or `.py` (marimo) notebook with explanation and code cells
2. Place any audio/image assets in `attachment/`
3. Update the article table in `README.md` with the publication date and link

### marimo Notebooks

marimo notebooks are stored as `.py` files and run with `uv run marimo edit <file>.py`. They use reactive cells (`@app.cell` decorators) and support interactive widgets (`mo.ui.slider`, `mo.ui.dropdown`, etc.).
