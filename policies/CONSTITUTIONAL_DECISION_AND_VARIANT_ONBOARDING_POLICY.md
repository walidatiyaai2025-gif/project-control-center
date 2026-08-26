# Constitutional Decision & Variant Onboarding Policy

POLICY_ID: CONSTITUTIONAL_DECISION_AND_VARIANT_ONBOARDING_POLICY
CONTROL_PLANE_VERSION: v1.6.0
POLICY_VERSION: 1.0.0

## Purpose

Ensure that operating decisions survive any individual Manager/Lead and that project/client variants are normalized automatically when a repository is added to PCC.

## Constitutional persistence

A durable decision affecting governance, onboarding, routing, project-family identity, versioning, task lifecycle, QA/integration/release gates, safety, or canonical sources is complete only when it is represented in committed PCC constitution/policy and machine-readable state where applicable.

Conversation, temporary prompts, local notes, and Worker memory are not canonical governance.

A current explicit owner instruction may amend governance. The Manager/Lead must persist the amendment and validate it before dependent work relies on it. If persistence cannot be completed safely, return `CONSTITUTION_AMENDMENT_PENDING` and block dependent writes.

## Automatic project classification

An owner instruction to add/register/onboard a repository triggers classification automatically. The owner does not need to prescribe the internal variant architecture.

The onboarding Manager/Lead must perform live evidence collection including repository tree, branches, open/merged work, manifests/configuration, domains/deployment clues, existing governance, releases/tags, historical naming, and owner-declared product/client identities.

Classify the repository as:
- `STANDALONE`; or
- `PRODUCT_FAMILY`.

## Product-family normalization

For every known family variant/client record at minimum:
- stable `VARIANT_ID` and display name;
- aliases;
- type/relationship (`PRIMARY`, `CLIENT_VARIANT`, or `PRODUCT_VARIANT` and `DERIVED_FROM` where applicable);
- lifecycle status;
- `IMPLEMENTATION_LOCATION` if verified;
- `IMPLEMENTATION_LOCATION_STATE`;
- `ROUTING_STATE`;
- evidence SHA/source for the boundary decision when available.

For the family record:
- `ONBOARDING_NORMALIZATION_STATE`;
- `VARIANT_GOVERNANCE_STATE`;
- `SHARED_CORE_STATE`;
- `CORE_ROUTING_STATE`.

Do not duplicate source, invent folders, create permanent client branches, or fabricate external repositories/domains to make normalization appear complete.

## Boundary states

Implementation-location states:
- `MAPPED`: verified location in this repository;
- `EXTERNAL_REPOSITORY`: verified distinct repository location;
- `UNRESOLVED`: business identity exists but implementation location is not proven;
- `UNMATERIALIZED`: variant is intentionally declared but no implementation exists yet.

Routing states:
- `READY`;
- `BLOCKED_UNRESOLVED`;
- `BLOCKED_UNMATERIALIZED`;
- `ARCHIVED`.

A `READY` variant must have a `MAPPED` or `EXTERNAL_REPOSITORY` location. Unresolved/unmaterialized variants stay visible and block only their own implementation route unless shared evidence requires a broader block.

## Shared core

`CORE_ROUTING_STATE=READY` only when the shared-core boundary is proven. Otherwise use `BLOCKED_UNRESOLVED`.

A core change requires validation against all affected active variants.

## Target repository governance installation

The explicit owner request to add/onboard the repository authorizes a dedicated governance-only onboarding branch/PR for PCC control files required to establish the contract, normally:
- `AGENTS.md`;
- `.pcc/project-family.json` for product families;
- `.pcc/managed-repository-control.json` where applicable;
- directly related governance docs/configuration.

This authorization excludes product source/content changes, deployment, release publication, force-push, branch deletion, or arbitrary cleanup.

Existing governance files must be reconciled; do not overwrite unique valid local instructions blindly.

## PCC synchronization

The target repository constitution/family manifest and `portfolio/project-routing.json` must describe the same project model and active variants. A mismatch is `ROUTING_CONFLICT`.

## Readiness semantics

`ONBOARDING_NORMALIZATION_STATE=READY` means classification is complete and all known uncertainty is explicitly represented.

For product families:
- `VARIANT_GOVERNANCE_STATE=READY` when all active variant routes and the shared-core route are ready;
- `VARIANT_GOVERNANCE_STATE=PARTIAL` when classification is complete but one or more known boundaries are explicitly blocked.

`PARTIAL` is not false completion. It is an evidence-backed state that permits verified boundaries to route while preventing guesses on unresolved ones.

## Replacement Lead law

A replacement Manager/Lead must recover this operating model from committed PCC `main`, the routing registry, and the target repository constitution/manifest. No handoff may require private conversational memory to understand which client lives where.
