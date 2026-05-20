#!/usr/bin/env python3
"""Self-test for scripts/assemble_level6_dossier.py.

This creates synthetic verifier-output files to validate dossier assembler mechanics.
It is not real GitHub Actions evidence and must not be used as final Level 6 proof.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / "selftest_outputs" / "level6_dossier_selftest"
ARTIFACT = WORK / "ci_verifier_outputs"
DOSSIER = WORK / "level6_dossier"


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")


def build_synthetic_artifact() -> None:
    ARTIFACT.mkdir(parents=True, exist_ok=True)

    promotion = {
        "schema": "trimatrix.master_lifecycle.promotion_report",
        "version": "0.5.8-selftest",
        "decision": "LEVEL_6_CANDIDATE",
        "max_level": 6,
        "reasons": ["Synthetic self-test only"],
        "truth_boundary": "Synthetic self-test artifact; not real external evidence."
    }
    write_json(ARTIFACT / "promotion_report.json", promotion)

    github = {
        "schema": "trimatrix.master_lifecycle.github_run_evidence",
        "version": "0.5.8-selftest",
        "anti_fixture": {
            "real_github_actions_run": True,
            "fixture": False,
            "synthetic": False,
            "sandbox_generated": False
        },
        "truth_boundary": "Synthetic structure only; not final proof."
    }
    write_json(ARTIFACT / "github_run_evidence.json", github)

    result = {
        "schema": "trimatrix.master_lifecycle.ci_verifier_result",
        "version": "0.5.8-selftest",
        "passed": True,
        "real_github_actions_environment": True,
        "truth_boundary": "Synthetic self-test result; not final proof."
    }
    write_json(ARTIFACT / "ci_verifier_result.json", result)

    proof = {
        "schema": "trimatrix.master_lifecycle.proof_packet",
        "version": "0.5.8-selftest",
        "created_at": "selftest",
        "truth_boundary": "Synthetic self-test proof packet; not final proof."
    }
    proof["packet_sha256"] = sha256_text(json.dumps(proof, sort_keys=True))
    write_json(ARTIFACT / "trimatrix_proof_packet.json", proof)


def run_selftest() -> dict:
    build_synthetic_artifact()
    cmd = [
        sys.executable,
        str(ROOT / "scripts" / "assemble_level6_dossier.py"),
        "--artifact-dir",
        str(ARTIFACT),
        "--out-dir",
        str(DOSSIER),
    ]
    proc = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)

    dossier_json = DOSSIER / "level6_closeout_dossier.json"
    dossier_md = DOSSIER / "level6_closeout_dossier.md"

    ok = proc.returncode == 0 and dossier_json.exists() and dossier_md.exists()
    packet = json.loads(dossier_json.read_text(encoding="utf-8")) if dossier_json.exists() else None
    if packet and packet.get("candidate_status") != "VERIFIED_LEVEL_6_CANDIDATE_DOSSIER":
        ok = False

    summary = {
        "schema": "trimatrix.master_lifecycle.level6_dossier_selftest",
        "version": "0.5.8",
        "passed": ok,
        "returncode": proc.returncode,
        "stdout_tail": proc.stdout[-4000:],
        "stderr_tail": proc.stderr[-4000:],
        "outputs": {
            "artifact_dir": str(ARTIFACT),
            "dossier_json": str(dossier_json),
            "dossier_markdown": str(dossier_md),
        },
        "truth_boundary": "This validates assembler mechanics with synthetic files only. It is not real Level 6 evidence."
    }
    summary_path = WORK / "selftest_summary.json"
    write_json(summary_path, summary)
    return summary


def main() -> None:
    summary = run_selftest()
    print(json.dumps(summary, indent=2, sort_keys=True))
    raise SystemExit(0 if summary["passed"] else 1)


if __name__ == "__main__":
    main()
