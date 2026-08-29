# End-to-End Guide

## Outcome

You will validate release evidence, promote two immutable releases through three environments, inspect deployment history, and roll production back to a known-good release. Everything runs locally.

## 1. Establish the mental model

Read [Architecture](ARCHITECTURE.md). Separate the continuous integration responsibility—producing trustworthy evidence—from continuous delivery—promoting that same evidence under environment policy.

## 2. Validate the repository

```bash
./scripts/check.sh
```

Expected result: six unit tests pass, both example releases validate, the environment definitions parse, and documentation checks succeed.

## 3. Inspect immutable evidence

```bash
./scripts/delivery.py verify --release examples/releases/1.0.0.json
```

Open the JSON and locate its source commit, digest-pinned image, SBOM reference, signature result, and five required checks. In a real system, the build stage would generate and attest this record.

## 4. Prove that gates fail closed

Attempt to skip development:

```bash
./scripts/delivery.py promote \
  --release examples/releases/1.0.0.json \
  --environment staging
```

The command must fail. A useful delivery platform makes an invalid path harder than the correct path.

## 5. Run the complete promotion

```bash
./scripts/demo.sh
```

The demo promotes versions 1.0.0 and 1.1.0 through development, staging, and production. It rebuilds neither release. Inspect `.local/state/production.json` to see current and prior evidence.

## 6. Rehearse rollback

```bash
./scripts/delivery.py rollback \
  --environment production \
  --state-dir .local/state
```

Confirm that production returns to `delivery-demo-1.0.0` and records `rollback_from`. The rollback uses a prior digest; it does not compile historical source during the incident.

## 7. Diagnose an incident

Work through [Lab 07](../labs/07-rollback-game-day/README.md), then compare your response to [Troubleshooting](TROUBLESHOOTING.md).

## 8. Map the model to production

Replace each local component deliberately:

| Local model | Production capability |
|---|---|
| Release JSON | Signed provenance/attestation in an artifact registry |
| Policy JSON | Policy engine and protected deployment environments |
| State files | Git desired state plus reconciler and external audit store |
| Approval string | Authenticated change approval with separation of duties |
| Rollback command | Git revert or progressive-delivery controller action |

## 9. Clean up

```bash
./scripts/clean.sh
```

Cleanup only removes the ignored repository `.local/` directory. No cloud resources were created.

