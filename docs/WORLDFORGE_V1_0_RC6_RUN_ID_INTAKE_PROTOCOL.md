# World-Forge v1.0 RC6 Run-ID Intake Protocol

This document records the exact next evidence dependency for World-Forge external proof promotion.

## Current evidence state

Confirmed:

- Repository: `triangel7777-tech/TriMatrix-`
- Workflow file: `.github/workflows/trimatrix-external-verifier.yml`
- Workflow name: `TriMatrix External Verifier`
- Expected artifact: `trimatrix-ci-verifier-outputs`
- Trigger commit: `2b73bf46ff2f1516b3df5eb9eb1788b7952c40cb`

Current boundary:

```text
No accepted run-specific GitHub Actions evidence has been imported yet.
```

This means the current evidence set does not include an accepted workflow run ID, job list, logs, downloaded artifact, promotion report, or independent attestation.

## Required input

Provide a successful GitHub Actions workflow run ID for:

```text
TriMatrix External Verifier
```

## Evidence import sequence

Once a run ID is available, import:

1. workflow run jobs;
2. workflow job steps;
3. workflow job logs;
4. workflow artifacts for `trimatrix-ci-verifier-outputs`;
5. downloaded artifact ZIP;
6. `promotion_report.json` from the artifact;
7. independent attestation.

## Promotion rule

World-Forge must not self-authorize Level 6. Even after evidence is imported, the correct status is external-review-ready until a real independent review accepts the packet.

## Truth boundary

This protocol does not claim Level 6, production deployment, independent audit, legal review, patent review, medical validation, or regulatory clearance. It only records the next evidence dependency and import sequence.
