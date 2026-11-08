from pathlib import Path

from deslop.engine import compute_metrics, prepare, scan_text
from deslop.fixer import apply_fixes

FIXTURES = Path(__file__).parent / "fixtures"


def read(name: str) -> str:
    return (FIXTURES / name).read_text(encoding="utf-8")


def test_slop_scores_much_higher_than_human_english():
    slop = scan_text(read("slop_en.md"))
    human = scan_text(read("human_en.md"))
    assert slop.score >= 90
    assert human.score <= 10
    assert slop.score - human.score >= 60


def test_slop_scores_much_higher_than_human_chinese():
    slop = scan_text(read("slop_zh.md"))
    human = scan_text(read("human_zh.md"))
    assert slop.score >= 80
    assert human.score <= 10


def test_bands_are_ordered():
    assert scan_text(read("human_en.md")).band == "reads like a person"
    assert scan_text(read("slop_en.md")).band == "heavy slop"


def test_severity_counts_add_up():
    result = scan_text(read("slop_en.md"))
    counted = sum(len(result.by_severity(n)) for n in (1, 2, 3))
    assert counted == len(result.findings)


def test_code_blocks_are_not_scanned():
    text = "```\ndelve into the tapestry, seamless synergy\n```\nA plain sentence about code.\n"
    result = scan_text(text)
    assert result.findings == []


def test_inline_code_and_urls_are_not_scanned():
    text = "Run `delve into` and see https://example.com/game-changer today.\n"
    assert scan_text(text).findings == []


def test_prepare_keeps_line_numbers():
    text = "line one\n```\ncode\n```\nline five\n"
    prepared = prepare(text)
    assert prepared.count("\n") == text.count("\n")
    assert "code" not in prepared


def test_metrics_count_words_and_cjk():
    en = compute_metrics("One two three four five.")
    assert en.words >= 5
    assert en.cjk_chars == 0
    zh = compute_metrics("这是一个测试句子。")
    assert zh.cjk_chars >= 6


def test_fix_applies_phrases_and_keeps_sentences_valid():
    text = "In order to ship this, we utilize the tool due to the fact that it is fast."
    rewritten, fixes = apply_fixes(text)
    assert "in order to" not in rewritten.lower()
    assert "utilize" in rewritten.lower()  # word-level rules are manual only
    assert "due to the fact that" not in rewritten.lower()
    assert "  " not in rewritten
    assert len(fixes) >= 2


def test_fix_never_touches_code_blocks():
    text = "```\ndelve into\n```\n"
    rewritten, fixes = apply_fixes(text)
    assert rewritten == text
    assert fixes == []


def test_human_text_has_no_fixable_findings():
    _, fixes = apply_fixes(read("human_en.md"))
    assert fixes == []


