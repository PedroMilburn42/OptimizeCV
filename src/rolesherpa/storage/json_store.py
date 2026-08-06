"""JSON StoragePort adapter — generic load/save for a single JSON file
(e.g. seen_jobs.json). No schema is imposed here: seen_jobs.json's shape
grows additively (rank_score, rank_verdict, rank_date from /rank), so the
skill layer owns that contract, not this adapter (design.md D2).
"""

import copy
import json
from pathlib import Path


class JsonStore:
    def __init__(self, path: Path, default: dict | list | None = None):
        self._path = Path(path)
        self._default = {} if default is None else default

    def load(self) -> dict | list:
        if not self._path.exists():
            return copy.deepcopy(self._default)
        return json.loads(self._path.read_text())

    def save(self, data: dict | list) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._path.write_text(json.dumps(data, indent=2, ensure_ascii=False))
