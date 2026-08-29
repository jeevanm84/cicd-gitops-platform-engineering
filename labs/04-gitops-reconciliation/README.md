# Lab 04 — GitOps Reconciliation

Treat `environments/` as reviewed intent and `.local/state` as observed state. Create a table of desired version, observed version, reconciliation age, and health. Describe how a production reconciler should behave when Git is unavailable, an admission policy denies the change, or a human mutates the workload.

Evidence: a reconciliation state machine with retry and alert conditions.

