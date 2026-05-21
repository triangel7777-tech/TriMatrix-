# World-Forge v1.0 RC7 Run-ID Submission Template

Use this template to provide the missing run-specific GitHub Actions evidence for the World-Forge external proof packet.

## Required repository

```text
triangel7777-tech/TriMatrix-
```

## Required workflow

```text
TriMatrix External Verifier
.github/workflows/trimatrix-external-verifier.yml
```

## Required run evidence

Fill in the values below before the next evidence-import pass:

```json
{
  "repo_full_name": "triangel7777-tech/TriMatrix-",
  "workflow_name": "TriMatrix External Verifier",
  "workflow_path": ".github/workflows/trimatrix-external-verifier.yml",
  "run_id": null,
  "run_url": null,
  "expected_artifact_name": "trimatrix-ci-verifier-outputs",
  "independent_attestation_reference": null,
  "attestation_reviewer": null,
  "attestation_scope": "review of workflow run evidence, artifact, promotion report, and claim boundary"
}
```

## Acceptance checklist

The next evidence packet may only advance to external-review-ready if all of the following are available:

- workflow run ID;
- job list;
- job steps;
- job logs;
- uploaded artifact named `trimatrix-ci-verifier-outputs`;
- downloaded artifact checksum;
- parsed `promotion_report.json`;
- real independent attestation;
- promotion gate showing no missing evidence blockers.

## Non-authorization rule

World-Forge must not self-authorize Level 6. Even with complete imported evidence, the correct status is external-review-ready until accepted by a real independent reviewer.

## Truth boundary

This template does not claim Level 6, production deployment, independent audit, legal review, patent review, medical validation, or regulatory clearance. It only defines the input required for the next evidence-import pass.
