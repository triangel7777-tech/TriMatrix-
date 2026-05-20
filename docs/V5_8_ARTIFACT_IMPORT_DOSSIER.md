# TriMatrix Master Lifecycle v5.8 — Artifact Import + Verified Level 6 Closeout Dossier

## Purpose

v5.8 converts downloaded GitHub Actions verifier outputs into a durable review dossier.

Input artifact directory:

```text
ci_verifier_outputs/
```

Required files:

```text
promotion_report.json
github_run_evidence.json
ci_verifier_result.json
trimatrix_proof_packet.json
```

## Command

```bash
python scripts/assemble_level6_dossier.py \
  --artifact-dir ci_verifier_outputs \
  --out-dir level6_dossier
```

Expected outputs:

```text
level6_dossier/level6_closeout_dossier.json
level6_dossier/level6_closeout_dossier.md
```

## Verification Rules

The assembler checks:

1. all required files exist
2. each required file has a SHA-256 digest
3. `promotion_report.decision == LEVEL_6_CANDIDATE`
4. `promotion_report.max_level == 6`
5. `github_run_evidence.anti_fixture.real_github_actions_run == true`
6. `ci_verifier_result.passed == true`
7. `ci_verifier_result.real_github_actions_environment == true`
8. proof-packet SHA-256 integrity

## Truth Boundary

The dossier verifies the downloaded verifier outputs and hash consistency. It does not prove production deployment, external security audit, legal/regulatory certification, or cloud persistence.

## Current Continuity State

v5.7 reached Level 6 Candidate based on observed GitHub Actions promotion output. v5.8 is the artifact-import and permanent closeout-dossier layer.
