# Ω Kernel v1.2 Live Proof Capture Checklist

This checklist separates repository bootstrap evidence from Level 6 evidence.

## Bootstrap CI evidence

Required fields:

```text
repository_full_name
branch
commit_sha
workflow_name
run_id
run_attempt
conclusion
started_at
completed_at
artifact_name
artifact_sha256_if_available
```

The bootstrap workflow validates only:

```text
package install
source compile
unit tests
bootstrap CLI validation
artifact upload
```

## Level 6 evidence gates

The bootstrap workflow is not enough. Level 6 candidacy requires all of the following:

```text
1. live_github_connector_proof
2. signed_independent_verifier_transcript
3. verifier_key_custody_packet
4. authoritative_release_publication
5. matching_release_asset_hash
6. manifest_signature_verification
7. public_key_signature_verification when used
8. private_key_material_scan_pass
9. strict_closeout_admitted
```

## Refusal rule

If evidence is fixture, captured-only, synthetic, manually typed without source binding, or missing repository/run identity, the status remains:

```text
Level 5 hold
```
