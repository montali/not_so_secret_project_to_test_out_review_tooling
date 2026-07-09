from pathlib import Path

import pytest
from typer.testing import CliRunner

from calcstack.cli.main import app

runner = CliRunner()


@pytest.fixture(autouse=True)
def isolated_history(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CALCSTACK_HISTORY", str(tmp_path / "history.json"))


def test_calc_prints_result() -> None:
    result = runner.invoke(app, ["calc", "2 + 3 * 4"])
    assert result.exit_code == 0
    assert "14" in result.stdout


def test_calc_leading_minus_expression() -> None:
    # A leading '-' must be treated as part of the expression, not an option.
    result = runner.invoke(app, ["calc", "-2 ^ 2"])
    assert result.exit_code == 0
    assert "-4" in result.stdout


def test_calc_invalid_expression_exits_nonzero() -> None:
    result = runner.invoke(app, ["calc", "1 +"])
    assert result.exit_code == 1
    assert "Error" in result.stdout


def test_calc_records_history_then_show_lists_it() -> None:
    runner.invoke(app, ["calc", "6 * 7"])
    result = runner.invoke(app, ["history", "show"])
    assert result.exit_code == 0
    assert "6 * 7" in result.stdout
    assert "42" in result.stdout


def test_no_save_option_skips_history() -> None:
    runner.invoke(app, ["calc", "1 + 1", "--no-save"])
    result = runner.invoke(app, ["history", "show"])
    assert "No history yet" in result.stdout


def test_history_clear() -> None:
    runner.invoke(app, ["calc", "1 + 1"])
    runner.invoke(app, ["history", "clear"])
    result = runner.invoke(app, ["history", "show"])
    assert "No history yet" in result.stdout
