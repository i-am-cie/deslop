# Contributing

## Adding a rule

Most contributions are one rule. A rule is an entry in `src/deslop/rules.py`:

```python
_r(
    "en.example",                 # id: <lang>.<short-name>
    r"\bthe exact phrase\b",      # regex, case-insensitive by default
    2,                             # severity 1-3
    "what it signals",             # shown next to the line
    "what to write instead",       # advice
    None,                          # optional safe replacement, or None
)
```

Rules with a replacement must be safe in every context. If the word needs
inflection (`utilize` → `use`/`uses`/`using`) or changes grammar, set `fix=None`
and let a human decide.

## Checklist for a new rule

1. Add the rule to `ENGLISH_RULES` or `CHINESE_RULES`.
2. Add a fixture line that triggers it in `tests/fixtures/slop_en.md` or `slop_zh.md`,
   and confirm `tests/fixtures/human_*.md` does not trigger it.
3. Run `pytest`.
4. Run `python -m deslop rules --json | wc -l` and check the count is still sane.
5. Regenerate `docs/RULES.md` with the snippet in `docs/RULES.md`'s header (or ask a maintainer).

## Code layout

```
src/deslop/rules.py    rule packs, the only place patterns live
src/deslop/engine.py   text preparation, matching, metrics, scoring
src/deslop/fixer.py    safe rewrites
src/deslop/cli.py      argument parsing and output
tests/                 fixture based tests
```

## Pull requests

- One topic per PR.
- `pytest` and `ruff check src tests` must pass.
- Do not lower thresholds or delete rules to make a test pass.
- Say which real text triggered the rule; "it feels AI-ish" is not enough.
