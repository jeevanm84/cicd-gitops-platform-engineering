# Cost and Production Readiness

## Cost optimization

- Scale ephemeral build workers to demand and apply concurrency limits.
- Cache dependencies only with trustworthy keys and measurable hit rates.
- Retain logs, artifacts, SBOMs, and attestations by regulatory and rollback need—not forever by default.
- Use preview environments with expiry ownership and automatic teardown.
- Measure cost per successful deployment and the engineering cost of failed change recovery.

## Production-readiness checklist

- [ ] Builds are reproducible and artifacts are immutable.
- [ ] Provenance, SBOM, signatures, scans, and exceptions are retained.
- [ ] Deployment identities are short-lived and environment-scoped.
- [ ] Production changes require protected review and authenticated approval.
- [ ] Desired/actual digest drift is monitored.
- [ ] Progressive rollout analysis uses release-correlated service signals.
- [ ] Rollback and roll-forward procedures are tested under pressure.
- [ ] Registry and control-plane recovery meet documented RTO/RPO.
- [ ] Break-glass access is time-limited, audited, and rehearsed.
- [ ] Preview and test resources have owners, budgets, and expiry.

## Future improvements

- Add a real OCI registry build with signed provenance.
- Integrate a policy engine and admission controller.
- Reconcile Kubernetes desired state with a GitOps controller.
- Add metric-driven canary analysis and fault injection.
- Export deployment events to an OpenTelemetry collector and durable audit store.

