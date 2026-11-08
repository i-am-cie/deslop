"""Scanning, metrics and scoring."""

from __future__ import annotations

import math
import re
import statistics
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field

from .rules import ALL_RULES, Rule

CJK_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]")
WORD_RE = re.compile(r"[A-Za-z][A-Za-z'\-]*")
CODE_FENCE_RE = re.compile(r"```.*?```|~~~.*?~~~", re.DOTALL)
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")
URL_RE = re.compile(r"https?://\S+|www\.\S+")
HTML_TAG_RE = re.compile(r"</?[a-zA-Z][^>\n]{0,200}>")
MD_LINK_RE = re.compile(r"\[([^\]]*)\]\([^)]*\)")
HR_RE = re.compile(r"^\s*(?:[-*_]\s*){3,}$", re.MULTILINE)
FRONT_MATTER_RE = re.compile(r"\A---\n.*?\n---\n", re.DOTALL)

SEVERITY_NAMES = {3: "strong", 2: "medium", 1: "mild"}

# controls how fast the score saturates; tuned on the fixtures in tests/
SATURATION = 120.0


@dataclass
class Finding:
    line: int
    column: int
    rule: Rule
    match: str

    @property
    def severity(self) -> int:
        return self.rule.severity


@dataclass
class Metrics:
    words: int
    cjk_chars: int
    units: int
    sentences: int
    em_dashes: int
    em_density: float
    sentence_cv: float | None
    lines: int

    @property
    def variation_label(self) -> str:
        if self.sentence_cv is None:
            return "n/a"
        if self.sentence_cv < 0.25:
            return "flat"
        if self.sentence_cv < 0.4:
            return "some"
        return "healthy"


@dataclass
class ScanResult:
    path: str
    text: str
    findings: list[Finding] = field(default_factory=list)
    metrics: Metrics | None = None
    score: int = 0
    structural_penalty: float = 0.0

    @property
    def band(self) -> str:
        return score_band(self.score)

    def by_severity(self, severity: int) -> list[Finding]:
        return [f for f in self.findings if f.severity == severity]

    @property
    def fixable(self) -> list[Finding]:
        return [f for f in self.findings if f.rule.fix is not None]


def prepare(text: str) -> str:
    """Blank out everything that should not be scanned, keeping line numbers.

    Code, URLs and link targets are not prose. They are replaced with spaces so
    that character positions and line numbers stay valid.
    """
    out = FRONT_MATTER_RE.sub(lambda m: _blank(m.group(0)), text)
    out = CODE_FENCE_RE.sub(lambda m: _blank(m.group(0)), out)
    out = INLINE_CODE_RE.sub(lambda m: _blank(m.group(0)), out)
    out = HTML_TAG_RE.sub(lambda m: _blank(m.group(0)), out)
    out = MD_LINK_RE.sub(lambda m: m.group(1) + " " * (len(m.group(0)) - len(m.group(1))), out)
    out = URL_RE.sub(lambda m: _blank(m.group(0)), out)
    out = HR_RE.sub(lambda m: _blank(m.group(0)), out)
    return out


def _blank(text: str) -> str:
    return "".join("\n" if ch == "\n" else " " for ch in text)


def _detect_language(text: str) -> str:
    cjk = len(CJK_RE.findall(text))
    words = len(WORD_RE.findall(text))
    return "zh" if cjk > words * 0.5 else "en"


def compute_metrics(text: str) -> Metrics:
    cleaned = prepare(text)
    words = len(WORD_RE.findall(cleaned))
    cjk = len(CJK_RE.findall(cleaned))
    units = words + cjk
    sentences = _sentences(cleaned)
    lengths = [len(WORD_RE.findall(s)) + len(CJK_RE.findall(s)) for s in sentences]
    lengths = [n for n in lengths if n > 0]
    cv = None
    if len(lengths) >= 4:
        mean = statistics.fmean(lengths)
        if mean:
            cv = statistics.pstdev(lengths) / mean
    # an em dash between two words, not a horizontal rule
    em = len(re.findall(r"\w\s*\u2014\s*\w", cleaned))
    per_1000 = (em / units * 1000) if units else 0.0
    return Metrics(
        words=words,
        cjk_chars=cjk,
        units=units,
        sentences=len(sentences),
        em_dashes=em,
        em_density=round(per_1000, 1),
        sentence_cv=round(cv, 2) if cv is not None else None,
        lines=cleaned.count("\n") + 1,
    )


def _sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+|\u3002|\uff01|\uff1f", text)
    return [p.strip() for p in parts if p.strip()]


def scan_text(text: str, path: str = "<text>", rules: Iterable[Rule] | None = None) -> ScanResult:
    cleaned = prepare(text)
    lang = _detect_language(cleaned)
    relevant = [r for r in (rules or ALL_RULES) if r.lang == lang]

    line_starts = [0]
    for i, ch in enumerate(cleaned):
        if ch == "\n":
            line_starts.append(i + 1)

    def locate(pos: int) -> tuple[int, int]:
        lo, hi = 0, len(line_starts) - 1
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if line_starts[mid] <= pos:
                lo = mid
            else:
                hi = mid - 1
        return lo + 1, pos - line_starts[lo] + 1

    result = ScanResult(path=path, text=text)
    for rule in relevant:
        for m in rule.compile().finditer(cleaned):
            line, col = locate(m.start())
            result.findings.append(Finding(line=line, column=col, rule=rule, match=m.group(0)))

    result.findings.sort(key=lambda f: (f.line, f.column))
    result.metrics = compute_metrics(text)
    _score(result)
    return result


def _score(result: ScanResult) -> None:
    metrics = result.metrics
    assert metrics is not None
    weights = sum(f.severity for f in result.findings)
    penalty = 0.0
    if metrics.em_density > 4:
        penalty += min(6.0, (metrics.em_density - 4) * 0.9)
    if metrics.sentence_cv is not None:
        if metrics.sentence_cv < 0.25:
            penalty += 4.0
        elif metrics.sentence_cv < 0.35:
            penalty += 2.0
    result.structural_penalty = round(penalty, 1)

    units = max(metrics.units, 40)
    density = (weights + penalty) / units * 1000
    # saturating curve: a couple of tells in a long text should not read as
    # heavy slop, while a text that is mostly stock phrases should approach 100
    result.score = max(0, min(99, round(100 * (1 - math.exp(-density / SATURATION)))))


def score_band(score: int) -> str:
    if score <= 15:
        return "reads like a person"
    if score <= 35:
        return "a few AI tells"
    if score <= 60:
        return "clearly AI-flavoured"
    return "heavy slop"


def check_paths(paths: Sequence[str], threshold: int = 40) -> tuple[list[ScanResult], int]:
    results: list[ScanResult] = []
    for path in paths:
        text = read_text(path)
        results.append(scan_text(text, path=path))
    exit_code = 1 if any(r.score > threshold for r in results) else 0
    return results, exit_code


def read_text(path: str) -> str:
    if path == "-":
        import sys

        return sys.stdin.read()
    with open(path, encoding="utf-8", errors="replace") as handle:
        return handle.read()
