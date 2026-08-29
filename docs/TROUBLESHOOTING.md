# Production Troubleshooting

Use this sequence for every delivery incident:

Incident → Symptoms → Investigation → Metrics → Logs → Commands → Root Cause → Immediate Mitigation → Permanent Fix → Prevention

## Deployment is healthy but traffic fails

- Symptoms: rollout reports available replicas while error rate rises.
- Investigation: compare application readiness, ingress/gateway status, endpoint membership, and dependency errors by release digest.
- Metrics: request rate, error rate, latency, saturation, readiness failures, and upstream resets.
- Commands: inspect desired and actual digest; query rollout events; compare Service endpoints; test the health route from inside and outside the workload network.
- Immediate mitigation: pause traffic progression and restore the last known-good digest.
- Permanent fix: use representative synthetic checks and error-budget-aware automated analysis.
- Prevention: require release-correlated dashboards and game-day validation before production onboarding.

## Git says new version; cluster runs old version

- Symptoms: desired-state commit changed, reconciliation did not.
- Investigation: check controller health, source authentication, sync status, admission denials, and image pull errors.
- Root cause examples: expired credential, unreachable Git provider, rejected policy, or missing registry digest.
- Mitigation: do not rebuild or manually change the workload. Restore controller access or revert desired state, then reconcile.
- Prevention: alert on reconciliation age and desired/actual digest drift.

## Rollback command has no prior release

- Symptoms: rollback fails closed.
- Investigation: inspect the deployment ledger and retention settings.
- Immediate mitigation: select a separately verified known-good release through the normal promotion path.
- Permanent fix: make history retention and artifact availability a production-readiness gate.
- Prevention: rehearse rollback routinely and monitor registry retention policies.

