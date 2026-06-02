from dataclasses import replace

from omega import EvidenceLedger, Omega, verify_ledger


def test_ledger_verifies_valid_chain():
    omega = Omega(lambda s: [s + 1], lambda s: s <= 3, lambda s: float(s))
    results = omega.run(0, 3)
    ledger = EvidenceLedger()
    ledger.extend(results)
    verification = verify_ledger(ledger.records)
    assert verification["valid"] is True
    assert verification["checked_records"] == 3


def test_ledger_detects_tampering():
    omega = Omega(lambda s: [s + 1], lambda s: s <= 2, lambda s: float(s))
    ledger = EvidenceLedger()
    ledger.extend(omega.run(0, 2))
    records = ledger.records
    tampered_transition = dict(records[0].transition)
    tampered_transition["selected_state"] = 999
    tampered = [replace(records[0], transition=tampered_transition), records[1]]
    verification = verify_ledger(tampered)
    assert verification["valid"] is False
    assert "current_hash mismatch" in verification["reason"]


def test_ledger_jsonl_roundtrip(tmp_path):
    omega = Omega(lambda s: [s + 1], lambda s: s <= 2, lambda s: float(s))
    ledger = EvidenceLedger()
    ledger.extend(omega.run(0, 2))
    path = tmp_path / "ledger.jsonl"
    ledger.to_jsonl(path)
    loaded = EvidenceLedger.from_jsonl(path)
    assert verify_ledger(loaded.records)["valid"] is True
