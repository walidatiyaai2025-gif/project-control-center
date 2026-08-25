# ADR-0001 — Declarative orchestration and immutable product version identity

Status: ACCEPTED
Control plane: v1.1.0

## Context

PCC v1.0.0 governed task/branch/QA/release flow but lacked portfolio-wide desired-vs-observed orchestration and an enforceable customer-version identity contract.

## Decision

1. Central orchestration is declarative and dry-run first, using OBSERVE → WARN → CANARY → ENFORCE with wave metadata.
2. Cross-repository credentials remain runtime abstractions, never repository data.
3. Safe self-healing is restricted to allow-listed derived PCC metadata.
4. Product versions are immutable mappings to source state once externally distributed.
5. Managed product repositories expose one canonical version source and official CI emits a version manifest.
6. Existing repositories discover and lock their real version baseline before enforcement.

## Consequences

PCC can detect drift and plan controlled rollouts without silently rewriting live repositories. Release pipelines gain deterministic version/source identity. Historical ambiguity is represented explicitly by confidence rather than guessed away.
