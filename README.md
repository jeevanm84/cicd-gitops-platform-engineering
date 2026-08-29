# CI/CD and GitOps Platform Engineering

[![Delivery CI](https://github.com/jeevanm84/cicd-gitops-platform-engineering/actions/workflows/ci.yml/badge.svg)](https://github.com/jeevanm84/cicd-gitops-platform-engineering/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

A local-first engineering laboratory for designing trustworthy software delivery: immutable release evidence, environment promotion, policy gates, deployment history, and deterministic rollback.

This repository is not a collection of vendor snippets. It provides an executable delivery control plane that beginners can run locally and experienced engineers can use to discuss production trade-offs.

## Engineering problem

Teams often rebuild artifacts per environment, depend on mutable tags, keep approvals outside the deployment record, and discover rollback gaps during an incident. This project models a safer path:

```text
source + tests
      │
      ▼
immutable release evidence ──► policy validation
      │
      ▼
development ──► staging ──► production
      │              │              │
      └──────── append-only deployment history
                                     │
                                     ▼
                              deterministic rollback
```

## What you will prove

- One artifact is promoted without rebuilding it.
- Every release has a commit, digest, SBOM reference, signature result, and test evidence.
- Staging cannot be skipped; production additionally requires an approval reference.
- Environment state records current and prior deployments.
- Rollback selects known-good immutable evidence rather than rebuilding old source.
- Pull requests run unit, policy, documentation, and example-pipeline checks.

## Quick start

Requirements: Python 3.11+, Git, and a POSIX shell. No cloud account is required.

```bash
./scripts/check.sh
./scripts/demo.sh
./scripts/delivery.py status --state-dir .local/state
./scripts/delivery.py rollback --environment production --state-dir .local/state
```

The demo operates only in ignored `.local/` state. Remove it safely with:

```bash
./scripts/clean.sh
```

## Repository map

```text
.
├── app/                   # Small testable service used as delivery input
├── delivery/              # Promotion, policy, history, and rollback engine
├── environments/          # Version-controlled environment requirements
├── examples/releases/     # Valid immutable release evidence
├── policies/              # Machine-readable organizational controls
├── scripts/               # Check, demo, delivery CLI, and safe cleanup
├── tests/                 # Unit and end-to-end delivery tests
├── labs/                  # Progressive hands-on exercises
├── docs/                  # Architecture, operations, security, and interviews
└── .github/               # CI, ownership, dependency, and contribution controls
```

## Learning path

| Level | Outcome | Start here |
|---|---|---|
| Beginner | Understand stages, artifacts, and checks | [End-to-end guide](docs/END_TO_END_GUIDE.md), Labs 01–02 |
| Intermediate | Promote one release and inspect history | Labs 03–05 |
| Advanced | Diagnose policy failures and rehearse rollback | Labs 06–07 |
| Senior / Platform | Design governance, progressive delivery, and recovery | Lab 08, [architecture](docs/ARCHITECTURE.md), [interviews](docs/INTERVIEW_QUESTIONS.md) |

## Production design flow

Problem → Requirements → Architecture → Implementation → Deployment → Security → High Availability → Scalability → Observability → Disaster Recovery → Cost Optimization → Troubleshooting → Lessons Learned

The local engine intentionally models control-plane behavior without claiming to be a production deployment controller. A production implementation would connect the same contracts to a registry, an attestation/signing system, a GitOps reconciler, workload identity, progressive delivery metrics, and an external audit store.

## Portfolio roadmap

[Git foundations](https://github.com/jeevanm84/git-command-master-map) → [AWS architecture](https://github.com/jeevanm84/aws-well-architected-production-labs) → [Terraform](https://github.com/jeevanm84/terraform-aws-ha-web-platform) → [Packer](https://github.com/jeevanm84/packer-aws-golden-image-pipeline) → [Kubernetes](https://github.com/jeevanm84/kubernetes-zero-to-production) → **CI/CD and GitOps** → Observability → SRE → DevSecOps → Troubleshooting → [MjCart capstone](https://github.com/jeevanm84/mjcart-ecommerce-microservices)

## Safety and cost

- The default workflow creates no cloud resources and costs nothing beyond your local machine and GitHub Actions allowance.
- Examples contain no credentials, account IDs, customer data, or employer material.
- Secrets must never be committed; production systems should use short-lived workload identity.
- `.local/` is the only default runtime state directory and cleanup refuses any other path.

## Contributing and support

Read [CONTRIBUTING.md](CONTRIBUTING.md). Use Issues for reproducible defects and Discussions for design or learning questions. Report security issues through GitHub private vulnerability reporting as described in [SECURITY.md](SECURITY.md).

