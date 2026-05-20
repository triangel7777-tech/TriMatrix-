# TriMatrix Master Lifecycle

TriMatrix Master Lifecycle v5.7 is a local-first continuity and proof harness seed.

## Current branch purpose

This branch adds a compact installable Python package with:

- `trimatrix status`
- `trimatrix proof`
- `trimatrix verify-proof`
- `trimatrix ci-verifier`
- GitHub Actions workflow: `TriMatrix External Verifier`
- artifact upload: `trimatrix-ci-verifier-outputs`

## Local run

```bash
python -m pip install -e .
python -m pytest -q
trimatrix status
trimatrix proof --output trimatrix_proof_packet.json
trimatrix verify-proof --path trimatrix_proof_packet.json
trimatrix ci-verifier --output-dir ci_verifier_outputs
```

Local dry runs intentionally hold at Level 5 because they are not external CI proof.

## GitHub Actions proof path

Run:

```text
Actions -> TriMatrix External Verifier -> Run workflow
```

The workflow uploads:

```text
trimatrix-ci-verifier-outputs
```

Key files:

```text
ci_verifier_outputs/github_run_evidence.json
ci_verifier_outputs/promotion_report.json
ci_verifier_outputs/ci_verifier_result.json
ci_verifier_outputs/trimatrix_proof_packet.json
```

## Truth boundary

This package creates evidence for review. A Level 6 candidate is not production deployment, security audit, regulatory approval, external certification, or cloud persistence proof.
