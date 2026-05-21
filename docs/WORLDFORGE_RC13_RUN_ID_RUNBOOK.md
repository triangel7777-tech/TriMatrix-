# World-Forge RC13 Run ID Runbook

## Workflow

TriMatrix External Verifier

## Workflow file

.github/workflows/trimatrix-external-verifier.yml

## Artifact name

trimatrix-ci-verifier-outputs

## Steps

1. Open the repository Actions tab.
2. Open TriMatrix External Verifier.
3. Run the workflow on main, or open the latest completed run.
4. Copy the run ID from the run URL.
5. Confirm the run completed successfully.
6. Confirm the artifact named trimatrix-ci-verifier-outputs exists.
7. Record the run ID, run URL, artifact name, and artifact checksum.
8. Provide those values to the World-Forge final packet intake manifest.

## Run URL pattern

https://github.com/triangel7777-tech/TriMatrix-/actions/runs/RUN_ID

## Required before promotion review

- run ID
- run URL
- jobs
- logs
- artifact checksum
- parsed promotion report
- independent review attestation

## Boundary

This file is only a run ID collection runbook. It does not claim workflow success or Level 6 status.
