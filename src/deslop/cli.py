"""Command line interface."""

from __future__ import annotations

import argparse
import difflib
import json
import os
import sys

from . import __version__
from .engine import ScanResult, read_text, scan_text
from .fixer import apply_fixes
from .rules import ALL_RULES, Rule

LIMIT_DEFAULT = 40

RED = "\033[31m"
YELLOW = "\033[33m"
GREEN = "\033[32m"
CYAN = "\033[36m"
DIM = "\033[2m"
BOLD = "\033[1m"
RESET = "\033[0m"


class Painter:
    def __init__(self, enabled: bool) -> None:
        self.enabled = enabled

    def __call__(self, text: str, *codes: str) -> str:
        if not self.enabled:
            return text
        return "".join(codes) + text + RESET


def _use_color(no_color: bool) -> bool:
    if no_color or os.environ.get("NO_COLOR"):
        return False
    return sys.stdout.isatty()


def _score_color(paint: Painter, score: int) -> str:
    if score > 60:
        return RED
    if score > 35:
        return YELLOW
    if score > 15:
        return CYAN
    return GREEN


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="deslop",
        description="Lint and rewrite AI-sounding writing. Offline, no API key.",
    )
    parser.add_argument("--version", action="version", version=f"deslop {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    check = sub.add_parser("check", help="score files and list findings")
    check.add_argument("paths", nargs="+", metavar="FILE", help="files to check, or - for stdin")
    check.add_argument("--json", action="store_true", help="machine readable output")
    check.add_argument("--min-score", type=int, default=LIMIT_DEFAULT,
                       help=f"exit 1 when a file scores above this (default {LIMIT_DEFAULT})")
    check.add_argument("--top", type=int, default=6, help="show at most N findings per file")
    check.add_argument("--no-color", action="store_true", help="disable ANSI colours")

    fix = sub.add_parser("fix", help="apply the safe rewrites")
    fix.add_argument("paths", nargs="+", metavar="FILE")
    fix.add_argument("--write", action="store_true", help="write the result back to the file")
    fix.add_argument("--diff", action="store_true", help="show a unified diff")
    fix.add_argument("--no-color", action="store_true")

    rules = sub.add_parser("rules", help="list the rule packs")
    rules.add_argument("--json", action="store_true")
    rules.add_argument("--lang", choices=["en", "zh", "all"], default="all")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "check":
        return cmd_check(args)
    if args.command == "fix":
        return cmd_fix(args)
    if args.command == "rules":
        return cmd_rules(args)
    parser.error("unknown command")
    return 2


def cmd_check(args: argparse.Namespace) -> int:
    paint = Painter(_use_color(args.no_color))
    results: list[ScanResult] = []
    for path in args.paths:
        try:
            text = read_text(path)
        except OSError as error:
            print(f"deslop: cannot read {path}: {error}", file=sys.stderr)
            return 2
        results.append(scan_text(text, path=path if path != "-" else "<stdin>"))

    if args.json:
        print(json.dumps([_as_dict(r) for r in results], indent=2, ensure_ascii=False))
        return 1 if any(r.score > args.min_score for r in results) else 0

    print(paint(f"deslop {__version__}", BOLD) + paint(f" - {len(results)} file(s)", DIM))
    for result in results:
        print()
        _print_file(paint, result, args.top)

    over = [r for r in results if r.score > args.min_score]
    print()
    summary = f"{len(results)} file(s) checked"
    if over:
        names = ", ".join(r.path for r in over)
        print(paint(summary, DIM) + paint(f" - {len(over)} over the limit of {args.min_score}", YELLOW))
        print(paint(f"  {names}", DIM))
        return 1
    print(paint(summary, DIM) + paint(" - nothing over the limit", GREEN))
    return 0


def _print_file(paint: Painter, result: ScanResult, top: int) -> None:
    color = _score_color(paint, result.score)
    head = paint(f"{result.path}", BOLD)
    score = paint(f"{result.score:3d}/100", BOLD, color)
    print(f"  {head}  {score}  {paint(result.band, color)}")
    if not result.findings:
        print(paint("    no tells found", GREEN))
        return
    counts = []
    for severity, name in ((3, "strong"), (2, "medium"), (1, "mild")):
        n = len(result.by_severity(severity))
        if n:
            counts.append(f"{n} {name}")
    fixable = f"{len(result.fixable)} fixable"
    print(paint(f"    {len(result.findings)} findings: " + ", ".join(counts) + f", {fixable}", DIM))
    for finding in result.findings[:top]:
        loc = f"{finding.line}:{finding.column}"
        severity = {3: "strong", 2: "medium", 1: "mild"}[finding.severity]
        sev_color = RED if finding.severity == 3 else YELLOW if finding.severity == 2 else CYAN
        snippet = finding.match.replace("\n", " ")
        if len(snippet) > 42:
            snippet = snippet[:39] + "..."
        fix_hint = ""
        if finding.rule.fix is not None:
            fix_hint = paint(" -> " + (finding.rule.fix or "(delete)"), GREEN)
        print(f"    {paint(loc, DIM):>18}  {paint(severity, sev_color):<8} {snippet!r}{fix_hint}")
    if len(result.findings) > top:
        print(paint(f"    ... {len(result.findings) - top} more (raise --top to see them)", DIM))
    _print_metrics(paint, result)


def _print_metrics(paint: Painter, result: ScanResult) -> None:
    m = result.metrics
    if m is None:
        return
    parts = [f"{m.words} words", f"{m.cjk_chars} CJK chars",
             f"em-dash {m.em_density}/1000",
             f"sentence variation {m.variation_label}"]
    print(paint("    metrics  " + " | ".join(parts), DIM))


def _as_dict(result: ScanResult) -> dict:
    m = result.metrics
    return {
        "path": result.path,
        "score": result.score,
        "band": result.band,
        "metrics": {
            "words": m.words,
            "cjk_chars": m.cjk_chars,
            "sentences": m.sentences,
            "em_density": m.em_density,
            "sentence_cv": m.sentence_cv,
            "variation": m.variation_label,
        } if m else {},
        "findings": [
            {
                "line": f.line,
                "column": f.column,
                "severity": f.severity,
                "rule": f.rule.id,
                "match": f.match,
                "message": f.rule.message,
                "suggestion": f.rule.suggestion,
                "fix": f.rule.fix,
            }
            for f in result.findings
        ],
    }


def cmd_fix(args: argparse.Namespace) -> int:
    paint = Painter(_use_color(args.no_color))
    total = 0
    for path in args.paths:
        try:
            text = read_text(path)
        except OSError as error:
            print(f"deslop: cannot read {path}: {error}", file=sys.stderr)
            return 2
        rewritten, fixes = apply_fixes(text)
        total += len(fixes)
        print(paint(f"{path}: {len(fixes)} safe rewrite(s)", BOLD))
        for fix in fixes:
            print(f"    line {fix.line:<5} {paint(fix.rule_id, DIM):<24} {fix.before!r} -> {fix.after!r}")
        if args.diff and rewritten != text:
            diff = difflib.unified_diff(
                text.splitlines(keepends=True),
                rewritten.splitlines(keepends=True),
                fromfile=f"a/{path}",
                tofile=f"b/{path}",
            )
            sys.stdout.writelines(diff)
        if args.write and rewritten != text:
            with open(path, "w", encoding="utf-8") as handle:
                handle.write(rewritten)
            print(paint(f"    written to {path}", GREEN))
    if not total:
        print(paint("nothing to rewrite", DIM))
    return 0


def cmd_rules(args: argparse.Namespace) -> int:
    selected: list[Rule] = [r for r in ALL_RULES if args.lang in ("all", r.lang)]
    if args.json:
        print(json.dumps([
            {
                "id": r.id,
                "lang": r.lang,
                "severity": r.severity,
                "pattern": r.pattern,
                "message": r.message,
                "suggestion": r.suggestion,
                "fix": r.fix,
            }
            for r in selected
        ], indent=2, ensure_ascii=False))
        return 0
    for rule in selected:
        kind = "fixable" if rule.fix is not None else "manual"
        print(f"{rule.id:<24} sev{rule.severity}  {rule.lang}  {kind:<7} {rule.message}")
    print(f"\n{len(selected)} rules")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
