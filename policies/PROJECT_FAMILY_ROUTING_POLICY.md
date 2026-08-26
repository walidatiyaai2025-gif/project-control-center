# Project Family & Worker Routing Policy

POLICY_ID: PROJECT_FAMILY_ROUTING_POLICY
ROUTING_CONTRACT_VERSION: 1.2.0

## Purpose

Make the Project Control Center the authoritative dispatcher for repository, product-family, client-variant, implementation-location, and change-scope selection before implementation workers modify code.

The owner may identify work using only a project name, client name, variant name, or registered alias. The Manager/Lead resolves that label to the canonical repository and target boundary and emits a routing packet. Workers do not guess.

## Canonical hierarchy

`OWNER REQUEST -> PCC MANAGER/LEAD -> PROJECT/REPOSITORY -> PRODUCT FAMILY (optional) -> VARIANT/CLIENT (optional) -> IMPLEMENTATION LOCATION -> TASK -> WORKER -> QA -> INTEGRATION/RELEASE`

A repository is either `STANDALONE` or `PRODUCT_FAMILY`. A long-lived client variant is not defined by a Git branch. Branches are implementation state. Variant identity is explicit governance metadata.

## Mandatory repository constitution

Every newly enrolled repository must declare its worker contract in a repository-root constitution, normally `AGENTS.md`.

For product families, the repository must also contain a machine-readable family manifest, normally `.pcc/project-family.json`.

A project with `CONSTITUTION_STATE=PENDING` is not worker-routable. `LEGACY_PENDING` preserves fleet visibility for pre-contract repositories but is not routing readiness.

## Automatic family normalization during onboarding

Project classification is mandatory onboarding work owned by the PCC Manager/Lead.

`ONBOARDING_NORMALIZATION_STATE=READY` means the repository has been classified from evidence, even if a known variant is explicitly unresolved. It does not mean every variant is writable.

A product family declares:
- `VARIANT_GOVERNANCE_STATE=READY|PARTIAL`;
- `CORE_ROUTING_STATE=READY|BLOCKED_UNRESOLVED`;
- each active variant's `IMPLEMENTATION_LOCATION`, `IMPLEMENTATION_LOCATION_STATE`, and `ROUTING_STATE`.

Allowed implementation-location states are `MAPPED`, `EXTERNAL_REPOSITORY`, `UNRESOLVED`, and `UNMATERIALIZED`.

A variant with `ROUTING_STATE=READY` must have a verified mapped/external implementation location. `UNRESOLVED` and `UNMATERIALIZED` variants remain visible but cannot receive implementation writes.

`VARIANT_GOVERNANCE_STATE=READY` means every active variant route and shared-core route are ready. `PARTIAL` means classification is complete but at least one known boundary is intentionally blocked.

Do not invent a directory, client branch, repository, domain, or shared-core architecture to force READY.

## Manager/Lead routing responsibility

Any Worker assuming Manager/Lead/Dispatcher responsibility MUST perform routing before assigning implementation work. This is a management responsibility and cannot be delegated as ambiguity to the implementation Worker.

The Manager/Lead must fetch live PCC state, resolve aliases, verify constitution and normalization readiness, fetch live target state, determine scope/change boundary, reconcile the canonical Task ID/branch, and issue the routing packet.

If the owner names only a client/variant alias, that is sufficient input for the Manager/Lead to resolve the parent project/repository through PCC.

## Worker start law

Every implementation worker MUST receive an authoritative PCC routing packet before write operations.

The routing packet must contain at least `PCC_SOURCE_SHA`, `PROJECT_ID`, `REPOSITORY`, `PROJECT_MODEL`, `TASK_ID`, `TARGET_SCOPE`, `TARGET_VARIANT` when applicable, `TARGET_IMPLEMENTATION_LOCATION` when applicable, constitution/family paths, branch resolution, `READ_FIRST`, `CHANGE_BOUNDARY`, `DO_NOT_TOUCH`, validation requirements, and required handoff/evidence.

If no valid route exists, the worker may inspect read-only but must return `ROUTING_REQUIRED` or the specific routing blocker. It must not infer the client or target from branch names, filenames, deployment names, or historical habit.

## Alias resolution

Aliases are case-insensitive and punctuation/spacing-insensitive for routing purposes. A variant alias may resolve directly to its parent project. Alias collisions are governance blockers.

## Product-family scope

A product-family task resolves to `CORE` or `VARIANT`.

`CORE` requires `CORE_ROUTING_STATE=READY`; it affects every active relevant variant and requires cross-variant validation.

`VARIANT` requires exactly one active target whose `ROUTING_STATE=READY`. Client-specific branding, configuration, content, deployment settings, or behavior must not leak to siblings.

If a physical boundary is unresolved, only that boundary is blocked. The Manager/Lead must not expand the block to verified siblings unless evidence shows shared impact.

## Central dispatcher operating contract

The owner can start a task by providing the PCC Manager/Lead with a project/client label and requested work. The Manager/Lead must fetch live PCC, read root constitution, resolve the label, verify constitution/normalization state, fetch live target, determine scope, verify target boundary routing state, reconcile task/branch, emit the packet, coordinate QA/integration/release against exact SHAs, and reconcile final evidence.

## Onboarding gate

`portfolio/project-routing.json` must contain exactly one routing record for every registered project in `portfolio/projects.yml`.

Newly added projects must not be treated as normalized while `ONBOARDING_NORMALIZATION_STATE=PENDING` or their routing declaration is missing. Product-family route readiness is boundary-specific; unresolved variants are explicit blockers for themselves, not fabricated as ready.

This routing contract does not weaken existing product-write authorization, CANARY/ENFORCE, lineage, break-glass, artifact provenance, or QA gates.
