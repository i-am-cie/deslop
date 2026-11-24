"""Consistency checks over the rule pack itself.

These guard the metadata that JSON Schema-style tests cannot cover: unique
ids, compilable patterns, legal severity/language values and the counts that
the README and docs/RULES.md quote.
"""

import re

import pytest

from deslop.rules import ALL_RULES, CHINESE_RULES, ENGLISH_RULES, FIXABLE, RULES_BY_ID

SEVERITIES = {1, 2, 3}
LANGS = {"en", "zh"}


def test_rule_ids_are_unique():
    ids = [rule.id for rule in ALL_RULES]
    assert len(ids) == len(set(ids))


def test_every_pattern_compiles():
    for rule in ALL_RULES:
        try:
            rule.compile()
        except re.error as exc:  # pragma: no cover - failure path
            pytest.fail(f"{rule.id}: invalid regex {rule.pattern!r}: {exc}")


def test_rule_fields_are_valid():
    for rule in ALL_RULES:
        assert rule.severity in SEVERITIES, rule.id
        assert rule.lang in LANGS, rule.id
        assert isinstance(rule.message, str) and rule.message.strip(), rule.id
        assert isinstance(rule.suggestion, str) and rule.suggestion.strip(), rule.id
        assert rule.fix is None or isinstance(rule.fix, str), rule.id


def test_rule_id_prefix_matches_language():
    for rule in ALL_RULES:
        prefix, _, rest = rule.id.partition(".")
        assert rest, rule.id
        assert prefix == rule.lang, f"{rule.id} prefix does not match lang {rule.lang}"


def test_rules_by_id_matches_all_rules():
    assert set(RULES_BY_ID) == {rule.id for rule in ALL_RULES}
    for rule in ALL_RULES:
        assert RULES_BY_ID[rule.id] is rule


def test_fixable_is_exactly_the_rules_with_a_replacement():
    assert FIXABLE == [rule for rule in ALL_RULES if rule.fix is not None]
    for rule in FIXABLE:
        assert rule.fix is not None


def test_rule_counts_match_documentation():
    # README.md and docs/RULES.md quote these numbers; keep them in sync.
    assert len(ENGLISH_RULES) == 70
    assert len(CHINESE_RULES) == 36
    assert len(ALL_RULES) == len(ENGLISH_RULES) + len(CHINESE_RULES) == 106
    assert len(FIXABLE) == 26


def test_no_duplicate_patterns_within_a_language():
    seen: dict[str, str] = {}
    for rule in ALL_RULES:
        previous = seen.get(rule.pattern)
        assert previous is None, f"duplicate pattern: {rule.id} and {previous}"
        seen[rule.pattern] = rule.id
