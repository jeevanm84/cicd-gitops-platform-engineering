# Security and Software Supply Chain

## Threat model

Protect against credential theft, unreviewed workflow changes, dependency compromise, mutable artifacts, forged evidence, unauthorized promotion, and rollback to a known-vulnerable build.

## Controls

- Pin third-party workflow actions to full commit SHAs and allow automated dependency updates.
- Prefer workload identity/OIDC over stored cloud credentials.
- Build once, identify by digest, create an SBOM, scan, sign, and verify before promotion.
- Protect workflow, policy, and production desired-state files with review rules and ownership.
- Treat forked pull requests as untrusted and never expose privileged secrets to them.
- Separate build identity from deployment identity and scope both to the minimum environment.
- Record actor, evidence, approval, digest, result, and rollback event in tamper-resistant logs.

## Secret handling

This repository requires no secret. In production, store secret material in a secrets manager, deliver it at runtime, rotate it, and prevent it from entering logs or artifact layers. Redact diagnostic bundles before sharing them.

## Promotion invariant

The digest verified after build must equal the digest admitted to and observed in every environment. If the identity changes, it is a different release and must repeat verification.

