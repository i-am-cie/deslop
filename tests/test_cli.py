import io
import json
from pathlib import Path

from deslop.cli import main

FIXTURES = Path(__file__).parent / "fixtures"


def test_check_json_reports_scores(capsys):
    code = main(["check", str(FIXTURES / "slop_en.md"), str(FIXTURES / "human_en.md"), "--json"])
    payload = json.loads(capsys.readouterr().out)
    by_path = {Path(item["path"]).name: item for item in payload}
    assert by_path["slop_en.md"]["score"] > by_path["human_en.md"]["score"]
    assert by_path["slop_en.md"]["band"] == "heavy slop"
    assert by_path["human_en.md"]["band"] == "reads like a person"
    assert code == 1


def test_check_exit_code_clean_file(capsys):
    code = main(["check", str(FIXTURES / "human_en.md"), "--no-color"])
    out = capsys.readouterr().out
    assert code == 0
    assert "nothing over the limit" in out


def test_check_threshold_option(capsys):
    code = main(["check", str(FIXTURES / "slop_en.md"), "--min-score", "100", "--no-color"])
    assert code == 0
    capsys.readouterr()


def test_check_reads_stdin(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("In today's fast-paced world, we delve into synergy.\n"))
    code = main(["check", "-", "--no-color"])
    out = capsys.readouterr().out
    assert "<stdin>" in out
    assert code == 1


def test_fix_write_rewrites_file(tmp_path, capsys):
    target = tmp_path / "note.md"
    target.write_text("In order to test, prior to shipping, we do it.\n", encoding="utf-8")
    code = main(["fix", str(target), "--write", "--no-color"])
    capsys.readouterr()
    assert code == 0
    text = target.read_text(encoding="utf-8")
    assert "in order to" not in text.lower()
    assert "prior to" not in text.lower()
    assert "before shipping" in text


def test_rules_json_lists_both_languages(capsys):
    code = main(["rules", "--json"])
    rules = json.loads(capsys.readouterr().out)
    assert code == 0
    assert len(rules) > 80
    assert {r["lang"] for r in rules} == {"en", "zh"}
    assert any(r["fix"] for r in rules)


def test_rules_lang_filter(capsys):
    main(["rules", "--json", "--lang", "zh"])
    rules = json.loads(capsys.readouterr().out)
    assert rules and all(r["lang"] == "zh" for r in rules)


def test_missing_file_returns_error(capsys):
    code = main(["check", "does-not-exist.md", "--no-color"])
    assert code == 2

