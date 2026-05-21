# World-Forge v1.0 RC8 Independent Attestation Template

Use this template to provide the independent review evidence required before any World-Forge packet can be treated as externally review-ready.

## Scope

This attestation must review the imported evidence for:

- repository identity;
- workflow identity;
- workflow run ID and URL;
- workflow job list;
- workflow job logs;
- uploaded artifact `trimatrix-ci-verifier-outputs`;
- downloaded artifact checksum;
- parsed `promotion_report.json`;
- claim boundary and non-overclaiming language.

## Attestation fields

```json
{
  "attestation_schema": "worldforge.independent_attestation.v1",
  "reviewer_name_or_handle": null,
  "reviewer_contact_or_profile": null,
  "reviewer_independence_statement": null,
  "review_scope": "workflow run evidence, artifact, promotion report, and claim boundary",
  "reviewed_repo_full_name": "triangel7777-tech/TriMatrix-",
  "reviewed_workflow": "TriMatrix External Verifier",
  "reviewed_run_id": null,
  "reviewed_artifact_name": "trimatrix-ci-verifier-outputs",
  "reviewed_artifact_sha256": null,
  "review_result": null,
  "conditions_or_limitations": [],
  "signature_or_public_reference": null,
  "review_timestamp_utc": null
}
```

## Acceptable review result values

```text
approved_for_external_review_packet
changes_required
rejected
incomplete
```

## Non-authorization rule

This attestation must not be treated as automatic Level 6 approval. World-Forge must still report the evidence level conservatively and must not self-authorize Level 6.

## Truth boundary

This template does not claim independent audit, production deployment, legal review, patent review, medical validation, regulatory clearance, or Level 6 status. It only defines the independent attestation input required for the next evidence-import pass.
