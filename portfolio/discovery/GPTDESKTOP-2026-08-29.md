# GPTDeskTop Existing-Project Discovery — 2026-08-29

PROJECT_ID: GPTDESKTOP
REPOSITORY: walidatiyaai2025-gif/GPTDeskTop
PROJECT_MODEL: STANDALONE
TARGET_SCOPE: PROJECT
POLICY_ENFORCEMENT_MODE: OBSERVE
WRITE_AUTHORIZED: false

## Live evidence

- Default branch: `main`.
- Main was `1e8bc02f7d8e8a6f4dcd3a9752fb0655c9b93d37` before PCC governance installation.
- Governance onboarding PR #324 merged to main at `61b7ef91f53a7f4e1312da770fbbe88f7d21068f`.
- Repository root contains one .NET solution: `GPTDeskTop.sln`.
- README identifies a .NET 8 WinForms ChatGPT Chrome/CDP monitoring application.
- Product code is under `src/`; tests are under `tests/`.
- Active premium/runtime development exists outside default main, including `ui/premium-real-runtime-v1`, observed at `69775cdce4352894ff9367c87cae2d71f784e113` during onboarding.
- Because active work is materially ahead of default main, `CANONICAL_DEVELOPMENT_LINEAGE` remains `UNRESOLVED` until PCC reconciliation establishes the authoritative continuation path.

## Classification

Evidence supports `STANDALONE`:

- one repository/product identity;
- no verified long-lived client/product variant boundaries;
- no family manifest required;
- project-scope routing is appropriate.

## Monitor enrollment

GPTDeskTop is enrolled in the PCC fleet desired state in `OBSERVE` mode. This makes it a live read/compare monitor target while prohibiting autonomous fleet repair writes.

## Safety

Onboarding does not authorize product-source modifications, deployment, release publication, force-push, branch deletion, or selection of a canonical development branch by guesswork.
