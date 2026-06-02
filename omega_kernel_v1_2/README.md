# Ω Kernel v1.2 — Repository Bootstrap Subset

This directory is the first real-repository bootstrap for Ω Kernel v1.2 inside `triangel7777-tech/TriMatrix-`.

## Core law

```text
S[t+1] = argmax_{s' in T(S[t])}(U(s'), -tau(s')) subject to I(s') = true
```

## What this bootstrap includes

- Minimal executable Ω transition kernel.
- Hash-chained evidence ledger.
- Local unit tests.
- GitHub Actions workflow for bootstrap validation.
- Operator handoff and proof-capture documentation.

## Current validation status

This repository bootstrap does **not** claim Level 6.

The source artifact baseline remains:

```text
Artifact: omega_kernel_v1_2.zip
SHA-256: 2533c79f16e2a158d6a22de19c9a9e4769ed93e6529274d5531c5b9e7f40e1ca
Local validation: Level 5 local deterministic validation with clean virtualenv proof
Level 6 claimed: false
```

## Local run

From this directory:

```bash
python -m pip install -e . pytest
python -m pytest -q
omega-bootstrap validate
```

## Truth boundary

This bootstrap proves only that the repository path, minimal package, and local tests are wired. Level 6 requires live GitHub Actions evidence, signed independent verifier evidence, verifier key-custody proof, authoritative release-publication proof, matching asset hashes, and strict closeout admission.
