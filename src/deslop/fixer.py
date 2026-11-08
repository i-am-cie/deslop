"""Safe automatic rewrites.

Only rules that ship an explicit replacement are applied. Anything that needs
judgement (a claim to rewrite, a superlative to back up) is reported but never
touched, because a wrong rewrite is worse than a flagged line.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from .engine import prepare, scan_text
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

    # tidy the mess a deletion can leave behind
    result = re.sub(r"[ \t]{2,}", " ", result)
    result = re.sub(r" +([,.;:!?])", r"\1", result)
    result = re.sub(r"\n{3,}", "\n\n", result)
    return result, fixes


def count_fixable(text: str) -> int:
    return len(scan_text(text).fixable)

