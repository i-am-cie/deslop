# Changelog

All notable changes to this project are documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-11-08

### Added

- `deslop check` with a 0–99 score, per-finding line and column, severity counts and structural metrics
- `deslop fix` with 26 safe rewrites and a `--diff` mode
- `deslop rules` listing every rule, with `--lang` and `--json`
- 70 English rules and 36 Chinese rules
- scoring by weighted density with a saturating curve, plus em-dash density and sentence-length variation
- stdin support (`-`), `--json` output, `--min-score` threshold for CI, exit codes 0/1/2
- agent skill in `skill/SKILL.md`
- test suite over before/after fixtures, GitHub Actions matrix for Python 3.9–3.13
