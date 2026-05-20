from pathlib import Path

from trimatrix.cli import ci_verifier, proof, status, verify_proof


def test_status_shape():
    result = status()
    assert result["schema"] == "trimatrix.master_lifecycle.status"
    assert result["version"] == "0.5.7"


def test_proof_roundtrip(tmp_path: Path):
    packet = tmp_path / "packet.json"
    proof(str(packet))
    verification = verify_proof(str(packet))
    assert verification["ok"] is True


def test_ci_verifier_local_dry_run_holds_level5(tmp_path: Path):
    result = ci_verifier(str(tmp_path / "outputs"))
    assert result["passed"] is True
    assert result["real_github_actions_environment"] is False
    assert result["promotion"]["decision"] == "HOLD_AT_LEVEL_5"
    assert result["promotion"]["max_level"] == 5
