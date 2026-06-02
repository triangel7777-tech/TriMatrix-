"""Small CLI for the Ω Kernel v1.2 repository bootstrap subset."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from . import EvidenceLedger, Omega, verify_ledger


def run_validation() -> dict:
    omega = Omega(
        transition=lambda s: [s - 1, s, s + 1, s + 2],
        invariant=lambda s: 0 <= s <= 10,
        utility=lambda s: -abs(10 - s),
        tiebreak=lambda s: s,
    )
    results = omega.run(0, 8)
    ledger = EvidenceLedger()
    ledger.extend(results)
    verification = verify_ledger(ledger.records)
    selected = [r.selected_state for r in results]
    return {
        "valid": selected[:5] == [2, 4, 6, 8, 10] and verification["valid"],
        "selected_states": selected,
        "ledger": verification,
        "truth_boundary": "Repository bootstrap validation only; Level 6 is not claimed.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(prog="omega-bootstrap")
    sub = parser.add_subparsers(dest="command", required=True)
    validate = sub.add_parser("validate", help="run bootstrap validation")
    validate.add_argument("--output", default=None)
    args = parser.parse_args()

    if args.command == "validate":
        report = run_validation()
        text = json.dumps(report, indent=2, sort_keys=True)
        if args.output:
            path = Path(args.output)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text + "\n", encoding="utf-8")
        print(text)
        if not report["valid"]:
            raise SystemExit(1)


if __name__ == "__main__":
    main()
