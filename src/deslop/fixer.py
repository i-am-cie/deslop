"""Safe automatic rewrites.

Only rules that ship an explicit replacement are applied. Anything that needs
judgement (a claim to rewrite, a superlative to back up) is reported but never
touched, because a wrong rewrite is worse than a flagged line.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from .engine import CODE_FENCE_RE, INLINE_CODE_RE, prepare, scan_text
from .rules import FIXABLE


@dataclass
class Fix:
    line: int
    rule_id: str
    before: str
    after: str


def _preserve_case(original: str, replacement: str) -> str:
    if not replacement:
        return replacement
    if original[:1].isupper():
        return replacement[:1].upper() + replacement[1:]
    return replacement


def _tidy_prose(text: str) -> str:
    """Collapse whitespace left behind by rewrites, outside code blocks.

    Code fences and inline code are stashed first so their indentation and
    layout are preserved; the cleanup only touches the surrounding prose.
    """
    stash: list[str] = []

    def _keep(match: re.Match[str]) -> str:
        stash.append(match.group(0))
        return f"\x00{len(stash) - 1}\x00"

    protected = CODE_FENCE_RE.sub(_keep, text)
    protected = INLINE_CODE_RE.sub(_keep, protected)

    protected = re.sub(r"[ \t]{2,}", " ", protected)
    protected = re.sub(r" +([,.;:!?])", r"\1", protected)
    # a deleted opener can leave a leading space at the start of a line
    protected = re.sub(r"(?m)^[ \t]+", "", protected)
    protected = re.sub(r"\n{3,}", "\n\n", protected)

    for index, block in enumerate(stash):
        protected = protected.replace(f"\x00{index}\x00", block)
    return protected


def apply_fixes(text: str) -> tuple[str, list[Fix]]:
    """Return the rewritten text and the list of changes made."""
    fixes: list[Fix] = []
    result = text

    # longest first so "due to the fact that" wins over "to"
    for rule in sorted(FIXABLE, key=lambda r: len(r.pattern), reverse=True):
        regex = rule.compile()
        cleaned = prepare(result)
        spans = [m.span() for m in regex.finditer(cleaned)]
        if not spans:
            continue
        for start, end in reversed(spans):
            line = result.count("\n", 0, start) + 1
            original = result[start:end]
            replacement = _preserve_case(original, rule.fix or "")
            fixes.append(Fix(line=line, rule_id=rule.id, before=original, after=replacement))
            result = result[:start] + replacement + result[end:]

    result = _tidy_prose(result)
    return result, fixes


def count_fixable(text: str) -> int:
    return len(scan_text(text).fixable)
