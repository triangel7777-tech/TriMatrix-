# Master Index Update — TriMatrix v5.8

## Active Project

TriMatrix Master Lifecycle

## Current Build State

```text
v5.7: Level 6 Candidate observed via GitHub Actions promotion output
v5.8: Artifact Import + Verified Level 6 Closeout Dossier branch created
```

## Evidence State

Confirmed from prior closeout:

```text
promotion_report.json printed decision=LEVEL_6_CANDIDATE
promotion_report.json printed max_level=6
reason: Real GitHub Actions evidence captured
PR #1 merged into main
v5.7 closeout committed to docs/LEVEL_6_CANDIDATE_CLOSEOUT_v5_7.md
```

v5.8 adds a dossier assembler for downloaded verifier artifacts.

## Required External Inputs

To complete v5.8 review, provide or place this directory locally:

```text
ci_verifier_outputs/
```

containing:

```text
promotion_report.json
github_run_evidence.json
ci_verifier_result.json
trimatrix_proof_packet.json
```

## Next Action Queue

1. Download the GitHub Actions artifact `trimatrix-ci-verifier-outputs`.
2. Extract it as `ci_verifier_outputs/`.
3. Run `python scripts/assemble_level6_dossier.py --artifact-dir ci_verifier_outputs --out-dir level6_dossier`.
4. Commit generated dossier outputs if review passes.
5. Preserve workflow run URL, commit SHA, artifact ID, and dossier SHA-256.

## Do Not Overclaim

Level 6 Candidate is not:

```text
production deployment
external security audit
legal/regulatory certification
cloud persistence proof
```

## Compact Memory Update Candidate

```text
TriMatrix v5.8 branch created for Artifact Import + Verified Level 6 Closeout Dossier. It adds scripts/assemble_level6_dossier.py plus dossier guide and Master Index update. The assembler verifies downloaded ci_verifier_outputs files, hashes, promotion_report decision/max_level, GitHub Actions evidence, CI verifier result, and proof-packet SHA-256. v5.8 still requires the actual downloaded GitHub Actions artifact to complete the permanent closeout dossier.
```
