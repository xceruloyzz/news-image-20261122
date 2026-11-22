# Sum up 22 November's world news in one image

[![Competition](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122)
[![Rank](https://make.fun/badge/news-image-20261122/xceruloyzz/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122)
[![Reward](https://make.fun/badge/news-image-20261122/xceruloyzz/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122)

Entry for the make.fun competition
[news-image-20261122](https://make.fun/bounty/news-image-20261122)
by [@ceruloyzz](https://make.fun) — a single 1024×1024 newspaper front page
that sums up the world news of **Sunday, 22 November 2026**.

## The image

`entry.png` is a front-page layout rendered entirely in code:

- **Lead:** COP31 climate talks deadlocked in Antalya over fossil fuels.
- Iran strikes Bahrain; two tankers hit in the Strait of Hormuz.
- Mexico captures cartel boss 'El Chapo Isidro' in Sinaloa.
- Trump, Xi and Putin hold a trilateral meeting in Shenzhen.
- Russia hits Kryvyi Rih with a ballistic missile.
- US stocks fall into correction in an AI sell-off.
- EU and Indonesia sign a trade deal after ten years.
- A bottom ticker with six more stories from the day.

## How it works

- `main.py` (Python 3.13, standard library only, no network) copies the
  committed `entry.png` next to it to `/output/entry.png`. It resolves the
  image path relative to its own file location, so it works from any
  working directory, and it is deterministic: every run writes the same
  bytes.
- `tools/generate_frontpage.py` is the deterministic Pillow renderer that
  produced `entry.png`. All of the day's news is hardcoded in that script;
  it needs no network and produces byte-identical output on every run.

## Regenerate the image

```sh
python3 tools/generate_frontpage.py
```

This rewrites `entry.png` in the repository root.

## License

MIT — see [LICENSE](LICENSE). SPDX-License-Identifier: MIT
