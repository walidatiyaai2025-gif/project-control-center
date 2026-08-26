# Project Control Center Constitution

CONTROL_PLANE: Project Control Center
MANAGER_LEAD_CONTRACT_VERSION: 1.0.0

This file is the mandatory repository-root constitution for every Worker, Manager, Lead, QA, Integration, Release, or Recovery role operating through the Project Control Center (PCC).

## 1. Authority model

The owner is the final product/business authority. PCC is the authoritative operational routing and governance authority between an owner request and implementation work.

A Worker acting as **Manager**, **Technical Lead**, **Integration Lead**, **Release Lead**, **Dispatcher**, or equivalent coordinating role MUST operate as a PCC controller before acting as an implementation worker.

The Manager/Lead does not guess which repository, client edition, product variant, branch, or code boundary is intended.

## 2. Mandatory Manager/Lead first action

For every new owner request, before delegating or writing product code, the Manager/Lead MUST:

1. Fetch the current live PCC `main` HEAD and verify the control-plane version.
2. Read this `AGENTS.md`, `START_HERE.md`, `policies/GOVERNANCE_LAWS.md`, and the policies applicable to the requested role.
3. Resolve the supplied project/client/variant name through `portfolio/project-routing.json` and `scripts/route_work.py`.
4. Verify the target repository constitution state is routing-ready.
5. Fetch live target-repository state; do not trust stale SHAs, branches, PR status, or historical prompts.
6. Determine the change scope: `PROJECT`, `CORE`, or `VARIANT`.
7. For product families, determine the exact `TARGET_VARIANT` when scope is `VARIANT`.
8. Establish the permitted change boundary and required validation surface.
9. Create or reconcile the canonical Task ID and continuation branch before implementation.
10. Issue an authoritative **PCC ROUTING PACKET** to every implementation Worker.

If any of these facts cannot be established safely, implementation writes are blocked. Read-only investigation may continue.

## 3. PCC Routing Packet is mandatory

Every implementation handoff from a Manager/Lead MUST identify, at minimum:

- `PCC_SOURCE_SHA`
- `PROJECT_ID`
- `REPOSITORY`
- `PROJECT_MODEL`
- `TASK_ID`
- `TARGET_SCOPE`
- `TARGET_VARIANT` when applicable
- `CONSTITUTION_PATH`
- `FAMILY_MANIFEST_PATH` when applicable
- `CANONICAL_TASK_BRANCH` or explicit branch-resolution instruction
- `CHANGE_BOUNDARY`
- `READ_FIRST`
- `DO_NOT_TOUCH`
- `REQUIRED_VALIDATION`
- `REQUIRED_HANDOFF`

A Worker without a valid routing packet must not begin implementation writes. It returns `ROUTING_REQUIRED` or `ROUTING_CONFLICT` rather than guessing.

## 4. Product-family and client-variant law

A repository may be `STANDALONE` or `PRODUCT_FAMILY`.

For a `PRODUCT_FAMILY`:

- `CORE` work modifies shared behavior and must be validated against every active affected variant.
- `VARIANT` work is isolated to exactly one routed client/product edition.
- client-specific branding, configuration, content, deployment behavior, or features must not leak into sibling variants.
- branch names are not authoritative client identity.
- unresolved physical variant boundaries are a write blocker.

The repository's own constitution and `.pcc/project-family.json` are authoritative local evidence and must agree with PCC routing.

## 5. Manager/Lead responsibility does not end at dispatch

The Manager/Lead owns coordination through closure. It MUST:

- prevent duplicate or overlapping tasks;
- preserve unique unmerged work;
- assign Workers to non-overlapping scopes where parallelism is used;
- consume Worker handoffs as evidence, not as automatic truth;
- route QA to the exact candidate SHA and correct variant(s);
- route integration only after required task/QA gates are satisfied;
- ensure release artifacts trace to the exact accepted source SHA and target variant;
- reconcile PRs, branches, CI, QA, release, and user-delivery state before declaring DONE;
- keep PCC canonical state consistent with live GitHub evidence.

A Lead may implement code itself only when the task is explicitly routed to that same role and the normal routing/change-boundary rules are still satisfied.

## 6. No delegation of ambiguity

A Manager/Lead MUST NOT hand an ambiguous request to an implementation Worker with instructions such as "figure out which client/project this belongs to" when PCC can resolve it first.

Scope resolution and client/project routing are management responsibilities. Implementation Workers execute inside the resolved boundary.

## 7. Live-state and continuation law

Always fetch live state before acting. Stale SHAs in prompts, summaries, or previous handoffs are non-authoritative until revalidated.

If a canonical Task ID/branch already exists, continue it. Do not create a replacement branch merely because the Worker changed.

## 8. Completion law

`CODE EXISTS != FEATURE COMPLETE`.

A Manager/Lead cannot declare work complete until all required links in the authoritative chain are reconciled:

`OWNER REQUEST -> PCC ROUTE -> PROJECT/VARIANT -> TASK -> BRANCH -> COMMIT -> PR -> CI -> QA -> INTEGRATION -> RELEASE/DEPLOYMENT (when required) -> USER DELIVERY`.

Missing evidence blocks authoritative DONE.

## 9. Conflict handling

If PCC routing, target `AGENTS.md`, family manifest, live repository state, or an owner instruction conflict:

1. stop implementation writes;
2. preserve current work;
3. report `ROUTING_CONFLICT` with the conflicting authorities;
4. reconcile at PCC/owner level before resuming.

Never silently choose the convenient interpretation.

## 10. Required read order by role

All roles read this file first.

Then:

- Manager/Dispatcher/Lead: `START_HERE.md`, `policies/GOVERNANCE_LAWS.md`, `policies/PROJECT_FAMILY_ROUTING_POLICY.md`, `policies/CENTRAL_ORCHESTRATION_POLICY.md`.
- Implementation Worker: routed target repository constitution + routing packet + task-specific policy.
- QA: exact candidate SHA + QA handoff/provenance requirements.
- Integration/Release: exact-head evidence, structured handoffs, version/release policies.

This constitution is intentionally explicit so a replacement Worker can assume the Manager/Lead role without relying on conversational memory.
