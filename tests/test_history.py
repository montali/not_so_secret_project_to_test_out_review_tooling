from pathlib import Path

import pytest

from calcstack.history import History, HistoryEntry, default_history


def test_add_and_read_roundtrip(tmp_path: Path) -> None:
    history = History(tmp_path / "history.json")
    history.add("2 + 2", "4")
    history.add("10 / 4", "2.5")

    entries = history.all()
    assert [e.expression for e in entries] == ["2 + 2", "10 / 4"]
    assert [e.result for e in entries] == ["4", "2.5"]
    assert all(isinstance(e, HistoryEntry) for e in entries)


def test_empty_history_when_missing(tmp_path: Path) -> None:
    assert History(tmp_path / "nope.json").all() == []


def test_clear_is_idempotent(tmp_path: Path) -> None:
    history = History(tmp_path / "history.json")
    history.add("1 + 1", "2")
    history.clear()
    history.clear()  # no error the second time
    assert history.all() == []


def test_default_history_honours_env(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    target = tmp_path / "custom.json"
    monkeypatch.setenv("CALCSTACK_HISTORY", str(target))
    default_history().add("7 * 6", "42")
    assert target.exists()
    assert default_history().all()[0].result == "42"
