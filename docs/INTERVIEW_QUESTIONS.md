# Interview Questions and Scenario Guide

Answers should state an invariant, failure mode, control, evidence, and trade-off—not only a tool name.

## Fundamentals

1. What is the difference between continuous integration, delivery, and deployment?
2. Why should one artifact move through all environments?
3. What problem does a digest solve that a tag does not?

## Intermediate

1. Where should environment configuration live, and how should secrets differ?
2. How do readiness and liveness affect safe rollout behavior?
3. Which evidence should block promotion?

## Advanced

1. Design a canary decision using service-level indicators and a rollback threshold.
2. How do you prevent a compromised pull request workflow from stealing deployment credentials?
3. How would you prove that the deployed workload matches reviewed source?

## Production

1. A GitOps controller is down while production is healthy. What changes, alerts, and recovery actions follow?
2. A critical vulnerability is found in the prior release during a current-release incident. How does rollback policy change?
3. The registry is unreachable during regional recovery. Which artifacts and metadata must already exist elsewhere?

## Senior engineer

1. Define platform golden paths without blocking teams with exceptional requirements.
2. Which delivery metrics reveal quality versus merely deployment frequency?
3. How do you introduce separation of duties without making recovery dangerously slow?

## Architect / SRE scenarios

1. Design delivery for 200 services across three regions with independent failure domains.
2. Define error-budget policy for automatic promotion and freeze decisions.
3. Design a tamper-evident audit trail spanning source, build, admission, deployment, and runtime identity.

