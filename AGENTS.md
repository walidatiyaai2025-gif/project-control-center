# Project Control Center Constitution

CONTROL_PLANE: Project Control Center
MANAGER_LEAD_CONTRACT_VERSION: 1.1.0

This file is the mandatory repository-root constitution for every Worker, Manager, Lead, QA, Integration, Release, Recovery, or Onboarding role operating through the Project Control Center (PCC).

## 1. Authority model

The owner is the final product/business authority. PCC is the authoritative operational routing and governance authority between an owner request and implementation work.

A Worker acting as **Manager**, **Technical Lead**, **Integration Lead**, **Release Lead**, **Dispatcher**, **Onboarding Lead**, or equivalent coordinating role MUST operate as a PCC controller before acting as an implementation worker.

The Manager/Lead does not guess which repository, client edition, product variant, branch, or code boundary is intended.

## 2. Constitutional persistence law

Durable operating decisions MUST survive the current conversation and the current Manager/Lead.

Any owner/Manager decision that changes project onboarding, routing, product-family/variant identity, role responsibility, task lifecycle, versioning, QA/integration/release gates, safety rules, or the source of truth MUST be persisted in the appropriate PCC constitution/policy and machine-readable control state where applicable.

A chat transcript, temporary prompt, Worker memory, or unmerged branch is not canonical governance.

A current explicit owner instruction may amend existing governance. The Manager/Lead must encode that amendment in PCC-controlled files and validate it before treating the new rule as durable authority. If immediate persistence is impossible, dependent writes are blocked with `CONSTITUTION_AMENDMENT_PENDING` rather than creating two competing truths.

Replacement Managers/Leads MUST be able to reconstruct the operating model from the committed PCC `main` plus the routed target repository constitution without relying on conversational memory.

## 3. Mandatory Manager/Lead first action

For every new owner request, before delegating or writing product code, the Manager/Lead MUST:

1. Fetch the current live PCC `main` HEAD and verify the control-plane version.
2. Read this `AGENTS.md`, `START_HERE.md`, `policies/GOVERNANCE_LAWS.md`, and the policies applicable to the requested role.
3. Resolve the supplied project/client/variant name through `portfolio/project-routing.json` and `scripts/route_work.py`.
4. Verify the target repository constitution and onboarding-normalization state are routing-ready for the requested boundary.
5. Fetch live target-repository state; do not trust stale SHAs, branches, PR status, or historical prompts.
6. Determine the change scope: `PROJECT`, `CORE`, or `VARIANT`.
7. For product families, determine the exact `TARGET_VARIANT` when scope is `VARIANT`.
8. Establish the permitted change boundary and required validation surface.
9. Create or reconcile the canonical Task ID and continuation branch before implementation.
10. Issue an authoritative **PCC ROUTING PACKET** to every implementation Worker.

If any of these facts cannot be established safely, implementation writes are blocked. Read-only investigation may continue.

## 4. Automatic onboarding variant normalization

When the owner says to **add**, **register**, or **onboard** a project/repository, the PCC Manager/Lead owns project classification and variant normalization automatically. The owner is not required to design the internal routing model.

The Manager/Lead MUST:

1. fetch live repository state and existing governance;
2. inspect branches, code roots, manifests/configuration, domains/deployment clues, releases, historical client/product names, and owner-declared identities;
3. classify the repository as `STANDALONE` or `PRODUCT_FAMILY`;
4. for a product family, enumerate known variants/clients and aliases, their relationship, implementation-location state, routing state, and shared-core state;
5. install/reconcile root `AGENTS.md` and, for a family, `.pcc/project-family.json`;
6. record the same model in `portfolio/project-routing.json`;
7. validate the normalization contract before declaring the project routable.

Do not invent a client directory, permanent client branch, deployment target, shared-core boundary, or duplicated code merely to make metadata look complete.

If a declared variant exists as a business identity but its code location cannot be verified, record it explicitly as unresolved/unmaterialized and block routing to that boundary only. Other verified variants may remain routable.

An explicit owner request to add/onboard a repository authorizes the Manager/Lead to prepare governance-only onboarding changes on a dedicated branch/PR limited to:

- `AGENTS.md`
- `.pcc/project-family.json` when applicable
- `.pcc/managed-repository-control.json` when applicable
- directly related governance documentation/configuration required by PCC

This does **not** authorize product-source changes, client-content changes, branch deletion, force-push, deployment, or release publication.

## 5. PCC Routing Packet is mandatory

Every implementation handoff from a Manager/Lead MUST identify, at minimum:

- `PCC_SOURCE_SHA`
- `PROJECT_ID`
- `REPOSITORY`
- `PROJECT_MODEL`
- `TASK_ID`
- `TARGET_SCOPE`
- `TARGET_VARIANT` when applicable
- `TARGET_IMPLEMENTATION_LOCATION` when applicable
- `CONSTITUTION_PATH`
- `FAMILY_MANIFEST_PATH` when applicable
- `CANONICAL_TASK_BRANCH` or explicit branch-resolution instruction
- `CHANGE_BOUNDARY`
- `READ_FIRST`
- `DO_NOT_TOUCH`
- `REQUIRED_VALIDATION`
- `REQUIRED_HANDOFF`

A Worker without a valid routing packet must not begin implementation writes. It returns `ROUTING_REQUIRED` or `ROUTING_CONFLICT` rather than guessing.

## 6. Product-family and client-variant law

A repository may be `STANDALONE` or `PRODUCT_FAMILY`.

For a `PRODUCT_FAMILY`:

- `CORE` work modifies shared behavior and must be validated against every active affected variant.
- `VARIANT` work is isolated to exactly one routed client/product edition.
- client-specific branding, configuration, content, deployment behavior, or features must not leak into sibling variants.
- branch names are not authoritative client identity.
- each active variant has an explicit `IMPLEMENTATION_LOCATION_STATE` and `ROUTING_STATE`.
- a variant is writable only when its `ROUTING_STATE=READY`.
- shared-core work is writable only when `CORE_ROUTING_STATE=READY`.
- unresolved physical boundaries remain visible but are write blockers for that boundary.

The repository's own constitution and `.pcc/project-family.json` are authoritative local evidence and must agree with PCC routing.

## 7. Manager/Lead responsibility does not end at dispatch

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

## 8. No delegation of ambiguity

A Manager/Lead MUST NOT hand an ambiguous request to an implementation Worker with instructions such as "figure out which client/project this belongs to" when PCC can resolve it first.

Scope resolution, client/project routing, and onboarding variant normalization are management responsibilities. Implementation Workers execute inside the resolved boundary.

## 9. Live-state and continuation law

Always fetch live state before acting. Stale SHAs in prompts, summaries, or previous handoffs are non-authoritative until revalidated.

If a canonical Task ID/branch already exists, continue it. Do not create a replacement branch merely because the Worker changed.

### Replacement Managers/Leads

Replacement Managers/Leads inherit the existing canonical task identity, routing decision, branch, constitutional decisions, and evidence chain. They must fetch live state and reconcile it, then continue the same controlled work unless PCC/owner evidence explicitly authorizes a new route or task.

## 10. Completion law

`CODE EXISTS != FEATURE COMPLETE`.

A Manager/Lead cannot declare work complete until all required links in the authoritative chain are reconciled:

`OWNER REQUEST -> PCC CONSTITUTION -> PCC ROUTE -> PROJECT/VARIANT -> TASK -> BRANCH -> COMMIT -> PR -> CI -> QA -> INTEGRATION -> RELEASE/DEPLOYMENT (when required) -> USER DELIVERY`.

Missing evidence blocks authoritative DONE.

## 11. Conflict handling

If PCC routing, target `AGENTS.md`, family manifest, live repository state, or an owner instruction conflict:

1. stop implementation writes;
2. preserve current work;
3. report `ROUTING_CONFLICT` or `CONSTITUTION_AMENDMENT_PENDING` with the conflicting authorities;
4. reconcile at PCC/owner level and persist the resulting durable decision before resuming dependent work.

Never silently choose the convenient interpretation.

## 12. Required read order by role

All roles read this file first.

Then:

- Manager/Dispatcher/Lead/Onboarding Lead: `START_HERE.md`, `policies/GOVERNANCE_LAWS.md`, `policies/CONSTITUTIONAL_DECISION_AND_VARIANT_ONBOARDING_POLICY.md`, `policies/PROJECT_FAMILY_ROUTING_POLICY.md`, `policies/CENTRAL_ORCHESTRATION_POLICY.md`.
- Implementation Worker: routed target repository constitution + routing packet + task-specific policy.
- QA: exact candidate SHA + QA handoff/provenance requirements.
- Integration/Release: exact-head evidence, structured handoffs, version/release policies.

This constitution is intentionally explicit so another Worker can assume the Manager/Lead role without relying on conversational memory.
