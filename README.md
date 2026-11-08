# deslop

**Lint and rewrite AI-sounding writing. Offline, no API key.**

`deslop` scores a piece of text for the phrases that make it read like generated copy, prints the exact line and word, and rewrites the safe ones for you. 106 rules, 70 English and 36 Chinese. Stdlib only, runs in milliseconds.

```console
$ deslop check examples/before.md

  examples/before.md   99/100  heavy slop
    18 findings: 7 strong, 9 medium, 2 mild, 6 fixable
                   3:1  strong   "In today's fast-paced world" -> Today
                  3:53  strong   'game-changer'
                  3:82  medium   'seamless' -> smooth
                 3:103  strong   'unlock the power'
                   5:1  medium   'It is important to note that' -> Note:
    metrics  82 words | 0 CJK chars | em-dash 0.0/1000 | sentence variation flat
```

The same file after `deslop fix` plus one manual pass: **0/100 — reads like a person.**

[![CI](https://github.com/i-am-cie/deslop/actions/workflows/ci.yml/badge.svg)](https://github.com/i-am-cie/deslop/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue)](pyproject.toml)
[![Dependencies](https://img.shields.io/badge/dependencies-0-brightgreen)](pyproject.toml)
[![Rules](https://img.shields.io/badge/rules-106-orange)](docs/RULES.md)

---

## Why

I wrote the English version of my own site and every paragraph came out of it sounding like a press release. Sentences of identical length. "Game-changer". "Delve into". Three examples in a row, every time.

That is a countable problem. Stock phrases have fingerprints, and you can grep for them. So I did, in two languages: 70 English patterns and 36 Chinese ones. Now it is a command.

It is a **linter, not a ghostwriter**. It points at the phrase; deciding what the sentence should say instead is still your job.

## Install

```bash
pipx install deslop          # recommended
# or
pip install deslop
# or, from source
git clone https://github.com/i-am-cie/deslop && cd deslop && pip install -e .
```

Python 3.9+. No dependencies.

## Use

```bash
deslop check README.md                      # score + findings
deslop check docs/*.md --min-score 30       # fail CI earlier
deslop check - < notes.md                   # read stdin
deslop check article.md --json              # machine readable
deslop fix article.md --diff                # show what would change
deslop fix article.md --write               # apply the safe rewrites
deslop rules                                # list every rule
```

### What it catches

| English | Chinese |
| --- | --- |
| `delve into`, `dive deep`, `unlock the power`, `harness` | 赋能、助力、打造、一站式 |
| `game-changer`, `cutting-edge`, `revolutionize`, `seamless` | 闭环、抓手、颗粒度、底层逻辑 |
| `a myriad of`, `a plethora of`, `testament to`, `tapestry` | 具有重要意义、奠定了坚实基础 |
| `it's not just X, it's Y` | 在当今…的时代、随着…的不断发展 |
| `It is important to note that`, `In conclusion` | 值得一提的是、不可否认的是、众所周知 |
| `moreover` / `furthermore` / `additionally` at sentence start | 首先…其次…最后、综上所述 |
| structural: em-dash density, flat sentence length | structural: 排比递进、无数据的效果词 |

Full list: [docs/RULES.md](docs/RULES.md).

### Scoring

Each hit adds its severity (3 strong, 2 medium, 1 mild), normalised by text length, then pushed through a saturating curve so one stray "crucial" in a long document does not panic you:

| Score | Meaning |
| --- | --- |
| 0–15 | reads like a person |
| 16–35 | a few AI tells |
| 36–60 | clearly AI-flavoured |
| 61–99 | heavy slop |

Two structure signals are added on top: em-dash density above 4 per 1000 words, and a sentence-length variation (coefficient of variation) below 0.25, which is what uniform generated sentences look like.

## Use it in CI

`deslop check` exits `1` when a file scores above `--min-score` (default 40), `0` when clean, `2` on a read error.

```yaml
- name: No AI slop in the docs
  run: |
    pipx install deslop
    deslop check README.md docs/*.md --min-score 30
```

## Use it from an agent skill

`skill/SKILL.md` is written for Claude Code, Cursor and other agents that read skill folders. Drop it in and the agent can check its own drafts before handing them to you.

## Before / after

| | `examples/before.md` | `examples/after.md` |
| --- | --- | --- |
| Score | 99 / 100 | 0 / 100 |
| Text | "In today's fast-paced world, our new dashboard is a game-changer. It leverages a seamless pipeline to unlock the power of your workflow…" | "The new dashboard is out. It runs the whole build pipeline in one place, so there are fewer tabs and fewer copy-paste steps between them." |

The `after` file is what a person writes once the linter has removed the noise. `deslop fix` gets you part of the way: 26 of the 106 rules carry a safe replacement, the rest are judgement calls it refuses to make for you.

## Limitations

- **It is a heuristic, not a detector.** A text scoring 80 might be written by a careful human who likes "robust". A text scoring 5 might be generated. It measures vocabulary and rhythm, not authorship.
- Word-level rules are reported but never auto-fixed (inflection and grammar), by design.
- English and Chinese only. Japanese and Korean are on the roadmap.
- The Chinese pack covers 官话/公文 and marketing language, which is where the tells live; it does not catch translated-from-English slop.

## Roadmap

- [ ] config file (`.deslop.toml`) for per-project rule sets and thresholds
- [ ] Japanese and Korean rule packs
- [ ] `--format sarif` for GitHub code scanning
- [ ] VS Code extension and a pre-commit hook
- [ ] a small web demo that runs entirely in the browser

## Contributing

New rules are the easiest way to help: add an entry to `src/deslop/rules.py`, add a fixture line in `tests/`, run `pytest`. See [CONTRIBUTING.md](CONTRIBUTING.md).

## 中文说明

**deslop 是一个「去 AI 味」检查器：离线、零依赖、毫秒级。**

它把文本里常见的 AI 套话逐条标出来（英文 70 条、中文 36 条），给出分数（0–99）和所在行号，并把其中 26 条能安全替换的直接改掉。

```bash
pipx install deslop
deslop check 周报.md
deslop fix 周报.md --write
```

中文规则覆盖：赋能 / 助力 / 打造 / 一站式 / 闭环 / 抓手 / 颗粒度 / 底层逻辑 / 降本增效 / 具有重要意义 / 奠定了坚实基础 / 在当今…的时代 / 随着…的不断发展 / 值得一提的是 / 不可否认的是 / 众所周知 / 首先…其次…最后 等。

它只是检查器，不是写作机器人 —— 它负责指出哪句话像模板，改写成什么还是你自己的事。

## License

MIT. See [LICENSE](LICENSE).
