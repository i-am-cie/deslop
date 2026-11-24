"""Regression tests for the safe-rewrite engine."""

from pathlib import Path

from deslop.fixer import apply_fixes, count_fixable

FIXTURES = Path(__file__).parent / "fixtures"


def read(name: str) -> str:
    return (FIXTURES / name).read_text(encoding="utf-8")


def test_deleted_opener_leaves_no_leading_space():
    text = "It should be noted that this works."
    rewritten, fixes = apply_fixes(text)
    assert rewritten == "this works."
    assert not rewritten.startswith(" ")
    assert [fix.rule_id for fix in fixes] == ["en.it-should-be-noted"]


def test_code_fence_indentation_is_preserved_when_nothing_matches():
    text = "Plain prose.\n\n```\n    def add(a, b):\n        return a + b\n```\n"
    rewritten, fixes = apply_fixes(text)
    assert fixes == []
    assert rewritten == text


def test_inline_code_is_not_rewritten():
    text = "Use `delve into` here, in order to test it."
    rewritten, fixes = apply_fixes(text)
    assert "`delve into`" in rewritten
    assert "in order to" not in rewritten.lower()
    assert any(fix.rule_id == "en.in-order-to" for fix in fixes)


def test_replacement_preserves_initial_capital():
    rewritten, _ = apply_fixes("Due to the fact that it is fast.")
    assert rewritten == "Because it is fast."
    rewritten_lower, _ = apply_fixes("due to the fact that it is fast.")
    assert rewritten_lower == "because it is fast."


def test_rewrite_leaves_no_double_space_or_punctuation_space():
    text = "In order to ship, prior to launch, we test due to the fact that it works."
    rewritten, fixes = apply_fixes(text)
    assert "  " not in rewritten
    assert " ," not in rewritten
    assert len(fixes) >= 3


def test_count_fixable_matches_fixable_findings():
    text = "In order to do it, due to the fact that x."
    assert count_fixable(text) == 2


def test_chinese_deletion_leaves_no_residue():
    rewritten, fixes = apply_fixes("值得一提的是，这个方案可行。")
    assert rewritten == "这个方案可行。"
    assert any(fix.rule_id == "zh.zhideyiti" for fix in fixes)


def test_human_chinese_text_has_no_fixes():
    _, fixes = apply_fixes(read("human_zh.md"))
    assert fixes == []
