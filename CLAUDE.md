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
- `music-language-tutorial/` — Jupyter Book: Chinese translation of ISMIR 2024 "Bridging Music Audio and Natural Language" tutorial (source in `main`, rendered HTML on `gh-pages`)
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
4. If providing a static HTML export, add it to the `gh-pages` branch and add a card entry in `index.html`

### marimo Notebooks

marimo notebooks are stored as `.py` files and run with `uv run marimo edit <file>.py`. They use reactive cells (`@app.cell` decorators) and support interactive widgets (`mo.ui.slider`, `mo.ui.dropdown`, etc.).

### Jupyter Book (`music-language-tutorial/`)

The `music-language-tutorial/` directory is a Jupyter Book v1 project (Sphinx-based, using `_config.yml` and `_toc.yml`). The project's `uv` environment installs Jupyter Book v2 (MyST-based), which is **not compatible** with the v1 config format.

To rebuild the book:

```bash
# Create a temp venv with Jupyter Book v1
python3 -m venv /tmp/jb-build
/tmp/jb-build/bin/pip install "jupyter-book<2" sphinxcontrib-mermaid

# Build
/tmp/jb-build/bin/jupyter-book build music-language-tutorial/

# Output is in music-language-tutorial/_build/html/
```

To deploy the built HTML to `gh-pages`:

1. Copy `music-language-tutorial/_build/html/` contents to `music-language-tutorial/` on the `gh-pages` branch
2. Ensure `.nojekyll` exists at the root of `gh-pages` (required for `_static/` directories)
3. Add a card entry in `index.html` on `gh-pages`
4. Commit and push

## GitHub Pages

The `gh-pages` branch serves the site at `https://beiciliang.github.io/intro2musictech/`. It contains:

- `index.html` — landing page with tutorial cards
- `MIR-CC.html` — static export of the marimo MIR tutorial
- `music-language-tutorial/` — rendered Jupyter Book site
- `.nojekyll` — disables Jekyll processing
