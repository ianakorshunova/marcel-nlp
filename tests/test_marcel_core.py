import sys
from pathlib import Path

# Allow tests to import marcel_core.py from the project root
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from marcel_core import analyze_sentence


def test_wrong_classifier():
    result = analyze_sentence("两本猫")

    assert result["corrected_sentence"] == "两只猫"
    assert result["total_errors"] == 1
    assert result["errors"][0]["type"] == "wrong_classifier"


def test_missing_classifier():
    result = analyze_sentence("三猫")

    assert result["corrected_sentence"] == "三只猫"
    assert result["total_errors"] == 1
    assert result["errors"][0]["type"] == "missing_classifier"


def test_liang_vs_er():
    result = analyze_sentence("二只猫")

    assert result["corrected_sentence"] == "两只猫"
    assert result["total_errors"] == 1
    assert result["errors"][0]["type"] == "liang_vs_er"


def test_missing_classifier_with_adjective():
    result = analyze_sentence("三漂亮猫")

    assert result["corrected_sentence"] == "三只漂亮猫"
    assert result["total_errors"] == 1
    assert result["errors"][0]["type"] == "missing_classifier"


def test_missing_classifier_with_de():
    result = analyze_sentence("三漂亮的猫")

    assert result["corrected_sentence"] == "三只漂亮的猫"
    assert result["total_errors"] == 1
    assert result["errors"][0]["type"] == "missing_classifier"


def test_correct_sentence_has_no_errors():
    result = analyze_sentence("三只猫")

    assert result["corrected_sentence"] == "三只猫"
    assert result["total_errors"] == 0
    assert result["errors"] == []