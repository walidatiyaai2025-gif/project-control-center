# 32 — Reactivate Legacy Project

PROMPT_ID: PCC-32
VERSION: 1.0.0
APPLIES_TO: LEGACY_REACTIVATION
PREVIOUS_STEP: PCC-31_OR_APPROVED_REACTIVATION_REQUEST
NEXT_STEP: PCC-20
REQUIRES_WRITE_ACCESS: true
CONTROL_PLANE_VERSION: v1.0.0

## Must exist before running

- A legacy project inventory/portfolio record, or enough evidence to establish one.
- Approved reason for reactivation.
- Repository read access and control-center write access.

## Mission

Move a legacy project into discovery without assuming historical branches are still valid.

## Execute

Record the reactivation request as a canonical requirement/task context, set lifecycle/maturity to a truthful transitional state such as `ACTIVE` + `DISCOVERY`, and preserve all archived/maintenance evidence.

Do not begin implementation. Historical production/default/develop branches are only discovery inputs. The next step must perform a fresh live Existing Project discovery.

## Required output

Return reactivation requirement/task reference, portfolio transition, known historical anchors, and direct the operator to PCC-20. PCC-20 must re-discover current live lineage from scratch.
