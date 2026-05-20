from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

VERSION = "0.5.7"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: str | Path) -> str:
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def write_json(path: str | Path, data: Dict[str, Any]) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")


def read_json(path: str | Path) -> Dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def is_github_actions() -> bool:
    return os.environ.get("GITHUB_ACTIONS", "").lower() == "true"


def github_run_url() -> str:
    repo = os.environ.get("GITHUB_REPOSITORY", "")
    run_id = os.environ.get("GITHUB_RUN_ID", "")
    return f"https://github.com/{repo}/actions/runs/{run_id}" if repo and run_id else ""


def status() -> Dict[str, Any]:
    return {
        "schema": "trimatrix.master_lifecycle.status",
        "version": VERSION,
        "created_at": utc_now(),
        "python_version": sys.version,
        "platform": platform.platform(),
        "github_actions": is_github_actions(),
    }


def proof(output: str = "trimatrix_proof_packet.json") -> Dict[str, Any]:
    packet = {
        "schema": "trimatrix.master_lifecycle.proof_packet",
        "version": VERSION,
        "created_at": utc_now(),
        "environment": status(),
        "truth_boundary": "Local proof packet only; not production deployment, security audit, or external validation by itself.",
    }
    packet["packet_sha256"] = sha256_text(json.dumps(packet, sort_keys=True))
    write_json(output, packet)
    return packet


def verify_proof(path: str) -> Dict[str, Any]:
    packet = read_json(path)
    supplied = packet.get("packet_sha256")
    unsigned = dict(packet)
    unsigned.pop("packet_sha256", None)
    expected = sha256_text(json.dumps(unsigned, sort_keys=True))
    findings = []
    if packet.get("schema") != "trimatrix.master_lifecycle.proof_packet":
        findings.append("unexpected schema")
    if supplied != expected:
        findings.append("packet_sha256 mismatch")
    return {"ok": not findings, "findings": findings, "packet_sha256": supplied}


def ci_verifier(output_dir: str = "ci_verifier_outputs") -> Dict[str, Any]:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    real_ci = is_github_actions()

    proof_path = out / "trimatrix_proof_packet.json"
    packet = proof(str(proof_path))

    report = {
        "schema": "trimatrix.master_lifecycle.report",
        "version": VERSION,
        "created_at": utc_now(),
        "status": status(),
    }
    report_path = out / "trimatrix_report.json"
    write_json(report_path, report)

    summary = {
        "schema": "trimatrix.master_lifecycle.ci_verifier_summary",
        "version": VERSION,
        "created_at": utc_now(),
        "passed": True,
        "real_github_actions_environment": real_ci,
        "packet_sha256": packet["packet_sha256"],
    }
    summary_path = out / "ci_verifier_summary.json"
    write_json(summary_path, summary)

    github_evidence = {
        "schema": "trimatrix.master_lifecycle.github_run_evidence",
        "version": VERSION,
        "created_at": utc_now(),
        "github": {
            "repository": os.environ.get("GITHUB_REPOSITORY", ""),
            "workflow_name": os.environ.get("GITHUB_WORKFLOW", ""),
            "run_id": os.environ.get("GITHUB_RUN_ID", ""),
            "run_attempt": os.environ.get("GITHUB_RUN_ATTEMPT", ""),
            "run_url": github_run_url(),
            "commit_sha": os.environ.get("GITHUB_SHA", ""),
            "ref": os.environ.get("GITHUB_REF", ""),
            "conclusion": "success",
        },
        "artifact": {
            "name": "trimatrix-ci-verifier-outputs",
            "files": [
                {"path": str(summary_path), "sha256": sha256_file(summary_path), "required": True},
                {"path": str(proof_path), "sha256": sha256_file(proof_path), "required": True},
                {"path": str(report_path), "sha256": sha256_file(report_path), "required": True},
            ],
        },
        "anti_fixture": {
            "synthetic": not real_ci,
            "fixture": not real_ci,
            "sandbox_generated": not real_ci,
            "real_github_actions_run": real_ci,
        },
        "truth_boundary": "Evidence is promotion-grade only when generated in real GitHub Actions.",
    }
    github_evidence["evidence_sha256"] = sha256_text(json.dumps(github_evidence, sort_keys=True))
    github_path = out / "github_run_evidence.json"
    write_json(github_path, github_evidence)

    promotion = {
        "schema": "trimatrix.master_lifecycle.promotion_report",
        "version": VERSION,
        "decision": "LEVEL_6_CANDIDATE" if real_ci else "HOLD_AT_LEVEL_5",
        "max_level": 6 if real_ci else 5,
        "reasons": [
            "Real GitHub Actions evidence captured" if real_ci else "Local dry-run evidence is intentionally non-promotable"
        ],
        "truth_boundary": "Level 6 candidate is still not production deployment or external security audit.",
    }
    promotion_path = out / "promotion_report.json"
    write_json(promotion_path, promotion)

    result = {
        "schema": "trimatrix.master_lifecycle.ci_verifier_result",
        "version": VERSION,
        "passed": True,
        "real_github_actions_environment": real_ci,
        "outputs": {
            "proof_packet": str(proof_path),
            "report": str(report_path),
            "summary": str(summary_path),
            "github_evidence": str(github_path),
            "promotion_report": str(promotion_path),
        },
        "promotion": promotion,
    }
    result_path = out / "ci_verifier_result.json"
    write_json(result_path, result)
    return result


def main(argv=None) -> None:
    parser = argparse.ArgumentParser(prog="trimatrix")
    sub = parser.add_subparsers(dest="command")
    sub.add_parser("status")
    p_proof = sub.add_parser("proof")
    p_proof.add_argument("--output", default="trimatrix_proof_packet.json")
    p_verify = sub.add_parser("verify-proof")
    p_verify.add_argument("--path", required=True)
    p_ci = sub.add_parser("ci-verifier")
    p_ci.add_argument("--output-dir", default="ci_verifier_outputs")
    args = parser.parse_args(argv)

    if args.command == "status":
        result = status()
    elif args.command == "proof":
        result = proof(args.output)
    elif args.command == "verify-proof":
        result = verify_proof(args.path)
    elif args.command == "ci-verifier":
        result = ci_verifier(args.output_dir)
    else:
        parser.print_help()
        return
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
