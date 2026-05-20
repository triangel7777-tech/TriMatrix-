# External Verifier Workflow Trigger

This file intentionally triggers the `TriMatrix External Verifier` workflow on `main`.

Purpose:

```text
Run the external verifier workflow using the corrected standard-library smoke-test path and upload trimatrix-ci-verifier-outputs.
```

Expected workflow:

```text
.github/workflows/trimatrix-external-verifier.yml
```

Expected artifact:

```text
trimatrix-ci-verifier-outputs
```

Boundary:

```text
This trigger does not by itself prove production deployment, external audit, or long-term operations.
```
