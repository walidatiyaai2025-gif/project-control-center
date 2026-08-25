# 00 — Bootstrap Control Center

PROMPT_ID: PCC-00
VERSION: 1.1.0
APPLIES_TO: PROJECT_CONTROL_CENTER
PREVIOUS_STEP: NONE
NEXT_STEP: PCC-01
REQUIRES_WRITE_ACCESS: true
CONTROL_PLANE_VERSION: v1.1.0

## Must exist before running

- An accessible target repository intended only for the Project Control Center.
- Permission to create/update files and workflows.
- The governance specification defining project/task/portfolio control, orchestration, and product-version identity.

## Mission

Bootstrap the repository as a control plane, not as a product repository. Create the entry point, prompt library, policies, templates, schemas, portfolio registry, canonical status area, central orchestration foundation, immutable version governance, dashboard foundation, validation workflows, and control-plane version marker.

## Execute

1. Inspect the live repository first; preserve any unique existing governance work.
2. Establish `START_HERE.md` as the operator entry point.
3. Install all mandatory prompt families and ensure each prompt contains the required metadata.
4. Install the 16 governance laws and worker lease lifecycle.
5. Add machine-readable templates/schemas for projects, tasks, status, release evidence, worker leases, user acceptance, project profiles, orchestration operations, and version manifests.
6. Add portfolio registry/priorities/status and version-aware dashboard projection.
7. Add declarative desired-vs-observed orchestration with dry run, staged rollout, locks, idempotency, failure isolation, auth abstraction and audit ledger.
8. Add `IMMUTABLE_CUSTOMER_VERSION_POLICY`, no-same-version/different-code guard and reusable version-governance workflow.
9. Add CODEOWNERS and CI validation.
10. Record `CONTROL_PLANE_VERSION` and repository identity.
11. Do not modify any pilot/product repository during bootstrap.

## Required output

Return exact control-plane version, immutable HEAD SHA, created/reused files/workflows/prompts, START_HERE status, orchestration status, version-governance status, dashboard status, self-audit status, limitations, and the next exact pilot prompt.
