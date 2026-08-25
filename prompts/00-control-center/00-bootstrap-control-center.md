# 00 — Bootstrap Control Center

PROMPT_ID: PCC-00
VERSION: 1.0.0
APPLIES_TO: PROJECT_CONTROL_CENTER
PREVIOUS_STEP: NONE
NEXT_STEP: PCC-01
REQUIRES_WRITE_ACCESS: true
CONTROL_PLANE_VERSION: v1.0.0

## Must exist before running

- An accessible target repository intended only for the Project Control Center.
- Permission to create/update files and workflows.
- The governance specification defining project/task/portfolio control.

## Mission

Bootstrap the repository as a control plane, not as a product repository. Create the entry point, prompt library structure, policies, templates, schemas, portfolio registry, canonical status area, dashboard foundation, validation workflows, and control-plane version marker.

## Execute

1. Inspect the live repository first; preserve any unique existing governance work.
2. Establish `START_HERE.md` as the operator entry point.
3. Install all mandatory prompt families and ensure each prompt contains the required metadata.
4. Install the 16 governance laws and worker lease lifecycle.
5. Add machine-readable templates/schemas for projects, tasks, status, release evidence, worker leases, and user acceptance.
6. Add portfolio registry/priorities/status and dashboard projection.
7. Add CODEOWNERS and CI validation.
8. Record `CONTROL_PLANE_VERSION` and repository identity.
9. Do not modify any pilot/product repository during bootstrap.

## Required output

Return exact control-plane version, immutable HEAD SHA, created files/workflows/prompts, START_HERE status, dashboard status, self-audit status, limitations, and the next exact pilot prompt.
