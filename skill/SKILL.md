---
name: deslop
description: Check a draft for AI-sounding stock phrases before handing it to a human. Use when writing or editing prose, README files, release notes, docs, or any text that should sound like a person wrote it.
---

# deslop

Use `deslop` to score a draft and find the phrases that make it read like generated copy.

## When to use it

- You finished a README, release note, blog post, or doc and are about to hand it over.
- The user says the text "sounds like AI", "is too corporate", or "去一下 AI 味".
- You are about to write user-facing prose and want the rules in mind beforehand.

## How to run it

```bash
deslop check <files>            # score + findings, exit 1 if over the limit
deslop check <files> --json     # structured findings
deslop fix <files> --diff       # see the safe rewrites
deslop fix <files> --write      # apply them
```

If `deslop` is not installed: `pipx install deslop`, or run it from source with
`PYTHONPATH=src python -m deslop`.

## Workflow

1. Write the draft.
2. Run `deslop check draft.md`.
3. For every finding, rewrite the sentence in plain words. Do not only run `deslop fix`:
   it removes 26 mechanical phrases and cannot replace a claim with a fact.
4. Re-run until the score is under 20.
5. Read it aloud. If a sentence could belong to any company's blog, cut it.

## Rules of thumb the checker encodes

- Say what happened, with a number or a date, instead of praising it.
- One claim per sentence. Cut the "not just X, it's Y" pattern entirely.
- No em-dash chains; they are the loudest tell in English.
- Vary sentence length. Uniform length is what generated text looks like.
- Chinese: 赋能 / 助力 / 打造 / 一站式 / 闭环 / 抓手 / 颗粒度 / 降本增效 / 具有重要意义 are banned unless quoting someone.

## Do not

- Do not disable rules to make the score pass.
- Do not claim the text is human-written because the score is low; the score measures phrases, not authorship.
