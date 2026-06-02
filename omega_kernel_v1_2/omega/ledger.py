"""Hash-chained evidence ledger for Ω transitions."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List

from .core import OmegaResult

GENESIS_HASH = "0" * 64


def _canonical_json(data: Any) -> str:
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False, default=str)


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class LedgerRecord:
    index: int
    previous_hash: str
    current_hash: str
    transition: Dict[str, Any]

    def body_for_hash(self) -> Dict[str, Any]:
        return {
            "index": self.index,
            "previous_hash": self.previous_hash,
            "transition": self.transition,
        }


class EvidenceLedger:
    """Append-only hash-chained transition ledger."""

    def __init__(self, initial_hash: str = GENESIS_HASH) -> None:
        self._records: List[LedgerRecord] = []
        self._latest_hash = initial_hash

    @property
    def records(self) -> List[LedgerRecord]:
        return list(self._records)

    @property
    def latest_hash(self) -> str:
        return self._latest_hash

    def append(self, result: OmegaResult[Any]) -> LedgerRecord:
        transition = asdict(result)
        index = len(self._records)
        previous_hash = self._latest_hash
        current_hash = _sha256_text(_canonical_json({
            "index": index,
            "previous_hash": previous_hash,
            "transition": transition,
        }))
        record = LedgerRecord(index=index, previous_hash=previous_hash, current_hash=current_hash, transition=transition)
        self._records.append(record)
        self._latest_hash = current_hash
        return record

    def extend(self, results: Iterable[OmegaResult[Any]]) -> List[LedgerRecord]:
        return [self.append(result) for result in results]

    def to_jsonl(self, path: str | Path) -> None:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as fh:
            for record in self._records:
                fh.write(_canonical_json(asdict(record)) + "\n")

    @classmethod
    def from_jsonl(cls, path: str | Path) -> "EvidenceLedger":
        ledger = cls()
        with Path(path).open("r", encoding="utf-8") as fh:
            for line in fh:
                data = json.loads(line)
                record = LedgerRecord(**data)
                ledger._records.append(record)
                ledger._latest_hash = record.current_hash
        return ledger


def verify_ledger(records: Iterable[LedgerRecord], initial_hash: str = GENESIS_HASH) -> Dict[str, Any]:
    previous_hash = initial_hash
    checked = 0
    for expected_index, record in enumerate(records):
        if record.index != expected_index:
            return {"valid": False, "checked_records": checked, "reason": f"index mismatch at record {expected_index}: got {record.index}"}
        if record.previous_hash != previous_hash:
            return {"valid": False, "checked_records": checked, "reason": f"previous_hash mismatch at record {expected_index}"}
        expected_hash = _sha256_text(_canonical_json(record.body_for_hash()))
        if record.current_hash != expected_hash:
            return {"valid": False, "checked_records": checked, "reason": f"current_hash mismatch at record {expected_index}"}
        previous_hash = record.current_hash
        checked += 1
    return {"valid": True, "checked_records": checked, "latest_hash": previous_hash}
