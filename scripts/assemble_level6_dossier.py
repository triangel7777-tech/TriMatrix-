#!/usr/bin/env python3
"""Assemble a TriMatrix Level 6 candidate closeout dossier from verifier outputs.

Usage:
  python scripts/assemble_level6_dossier.py --artifact-dir ci_verifier_outputs --out-dir level6_dossier

This script uses only the Python standard library. It verifies the expected verifier-output files,
calculates SHA-256 hashes, checks the promotion report, and writes a reviewable dossier JSON and Markdown.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

REQUIRED_FILES = [
    "promotion_report.json",
    "github_run_evidence.json",
    "ci_verifier_result.json",
    "trimatrix_proof_packet.json",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def verify_artifact_dir(artifact_dir: Path) -> Dict[str, Any]:
    findings: List[str] = []
    files: Dict[str, Dict[str, Any]] = {}

    for name in REQUIRED_FILES:
        path = artifact_dir / name
        if not path.exists():
            findings.append(f"missing required file: {name}")
            continue
        files[name] = {
            "path": str(path),
            "sha256": sha256_file(path),
            "size_bytes": path.stat().st_size,
        }

    promotion = None
    github = None
    result = None
    proof = None

    try:
        if (artifact_dir / "promotion_report.json").exists():
            promotion = load_json(artifact_dir / "promotion_report.json")
    except Exception as exc:
        findings.append(f"promotion_report.json invalid: {exc}")

    try:
        if (artifact_dir / "github_run_evidence.json").exists():
            github = load_json(artifact_dir / "github_run_evidence.json")
    except Exception as exc:
        findings.append(f"github_run_evidence.json invalid: {exc}")

    try:
        if (artifact_dir / "ci_verifier_result.json").exists():
            result = load_json(artifact_dir / "ci_verifier_result.json")
    except Exception as exc:
        findings.append(f"ci_verifier_result.json invalid: {exc}")

    try:
        if (artifact_dir / "trimatrix_proof_packet.json").exists():
            proof = load_json(artifact_dir / "trimatrix_proof_packet.json")
    except Exception as exc:
        findings.append(f"trimatrix_proof_packet.json invalid: {exc}")

    if promotion:
        if promotion.get("decision") != "LEVEL_6_CANDIDATE":
            findings.append("promotion_report decision is not LEVEL_6_CANDIDATE")
        if promotion.get("max_level") != 6:
            findings.append("promotion_report max_level is not 6")

    if github:
        anti = github.get("anti_fixture", {})
        if anti.get("real_github_actions_run") is not True:
            findings.append("github_run_evidence does not confirm real GitHub Actions run")
        if anti.get("fixture") is True or anti.get("synthetic") is True or anti.get("sandbox_generated") is True:
            findings.append("github_run_evidence is marked fixture/synthetic/sandbox")

    if result:
        if result.get("passed") is not True:
            findings.append("ci_verifier_result passed is not true")
        if result.get("real_github_actions_environment") is not True:
            findings.append("ci_verifier_result does not confirm real GitHub Actions environment")

    if proof:
        if proof.get("schema") != "trimatrix.master_lifecycle.proof_packet":
            findings.append("proof packet schema mismatch")
        supplied = proof.get("packet_sha256")
        unsigned = dict(proof)
        unsigned.pop("packet_sha256", None)
        expected = hashlib.sha256(json.dumps(unsigned, sort_keys=True).encode("utf-8")).hexdigest()
        if supplied != expected:
            findings.append("proof packet sha256 mismatch")

    return {
        "schema": "trimatrix.master_lifecycle.level6_artifact_verification",
        "version": "0.5.8",
        "created_at": utc_now(),
        "artifact_dir": str(artifact_dir),
        "ok": len(findings) == 0,
        "findings": findings,
        "files": files,
        "promotion_summary": promotion,
        "github_summary": github,
        "ci_verifier_summary": result,
        "truth_boundary": (
            "This verifies verifier-output files and hashes. It does not prove production deployment, "
            "external security audit, regulatory approval, or cloud persistence."
        ),
    }


def write_dossier(verification: Dict[str, Any], out_dir: Path) -> Dict[str, Any]:
    out_dir.mkdir(parents=True, exist_ok=True)
    packet = {
        "schema": "trimatrix.master_lifecycle.level6_closeout_dossier",
        "version": "0.5.8",
        "created_at": utc_now(),
        "candidate_status": "VERIFIED_LEVEL_6_CANDIDATE_DOSSIER" if verification["ok"] else "DOSSIER_BLOCKED",
        "verification": verification,
    }
    unsigned = json.dumps(packet, sort_keys=True)
    packet["dossier_sha256"] = hashlib.sha256(unsigned.encode("utf-8")).hexdigest()

    json_path = out_dir / "level6_closeout_dossier.json"
    md_path = out_dir / "level6_closeout_dossier.md"
    json_path.write_text(json.dumps(packet, indent=2, sort_keys=True), encoding="utf-8")

    md = [
        "# TriMatrix Level 6 Candidate Closeout Dossier",
        "",
        f"Generated: {packet['created_at']}",
        "",
        f"Candidate status: `{packet['candidate_status']}`",
        "",
        f"Dossier SHA-256: `{packet['dossier_sha256']}`",
        "",
        "## Verification",
        "",
        f"Passed: `{verification['ok']}`",
        "",
        "## Findings",
        "",
    ]
    if verification["findings"]:
        for item in verification["findings"]:
            md.append(f"- {item}")
    else:
        md.append("- No blocking findings.")

    md.extend(["", "## Files", ""])
    for name, meta in verification["files"].items():
        md.append(f"- `{name}` — SHA-256 `{meta['sha256']}` — {meta['size_bytes']} bytes")

    md.extend([
        "",
        "## Truth Boundary",
        "",
        verification["truth_boundary"],
        "",
    ])
    md_path.write_text("\n".join(md), encoding="utf-8")

    return {"json": str(json_path), "markdown": str(md_path), "packet": packet}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact-dir", required=True)
    parser.add_argument("--out-dir", default="level6_dossier")
    args = parser.parse_args()

    verification = verify_artifact_dir(Path(args.artifact_dir))
    result = write_dossier(verification, Path(args.out_dir))
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if verification["ok"] else 1)


if __name__ == "__main__":
    main()
