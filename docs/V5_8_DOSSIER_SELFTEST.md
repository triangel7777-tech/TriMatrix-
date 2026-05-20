# TriMatrix v5.8 Dossier Self-Test

## Purpose

This self-test validates the mechanics of `scripts/assemble_level6_dossier.py` without requiring the real downloaded GitHub Actions artifact.

It creates synthetic verifier-output files, runs the dossier assembler, and verifies that dossier JSON/Markdown are produced.

## Command

```bash
python scripts/selftest_level6_dossier.py
```

Expected outputs:

```text
selftest_outputs/level6_dossier_selftest/ci_verifier_outputs/
selftest_outputs/level6_dossier_selftest/level6_dossier/level6_closeout_dossier.json
selftest_outputs/level6_dossier_selftest/level6_dossier/level6_closeout_dossier.md
selftest_outputs/level6_dossier_selftest/selftest_summary.json
```

## Workflow

```text
TriMatrix Dossier Self-Test
```

uploads:

```text
trimatrix-dossier-selftest-outputs
```

## Truth Boundary

This self-test proves assembler mechanics only. It is synthetic and must not be treated as real Level 6 evidence. Real v5.8 completion still requires the downloaded `trimatrix-ci-verifier-outputs` artifact from the real TriMatrix External Verifier workflow.
