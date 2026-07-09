"""Persistent calculation history, stored as JSON on disk.

Both the CLI and the web API record every successful calculation here, so a
user can see what they computed earlier. The storage location can be overridden
with the ``CALCSTACK_HISTORY`` environment variable, which keeps tests hermetic.
"""

from __future__ import annotations

import json
import os
from datetime import UTC, datetime
from pathlib import Path

from pydantic import BaseModel

DEFAULT_HISTORY_PATH = Path.home() / ".calcstack" / "history.json"


class HistoryEntry(BaseModel):
    """A single recorded calculation."""

    expression: str
    result: str
    timestamp: datetime

class History:
    """Append-only JSON-backed log of calculations."""

    def __init__(self, path: Path = DEFAULT_HISTORY_PATH) -> None:
        self.path = path

    def add(self, expression: str, result: str) -> HistoryEntry:
        entry = HistoryEntry(
            expression=expression,
            result=result,
            timestamp=datetime.now(UTC),
        )
        entries = self.all()
        entries.append(entry)
        self._save(entries)
        return entry

    def all(self) -> list[HistoryEntry]:
        if not self.path.exists():
            return []
        raw = json.loads(self.path.read_text(encoding="utf-8"))
        return [HistoryEntry.model_validate(item) for item in raw]

    def clear(self) -> None:
        self.path.unlink(missing_ok=True)

    def _save(self, entries: list[HistoryEntry]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = [entry.model_dump(mode="json") for entry in entries]
        self.path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def default_history() -> History:
    """Return a :class:`History` honouring the ``CALCSTACK_HISTORY`` override."""
    override = os.environ.get("CALCSTACK_HISTORY")
    return History(Path(override)) if override else History()
