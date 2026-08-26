# Project Family & Worker Routing Policy

POLICY_ID: PROJECT_FAMILY_ROUTING_POLICY
ROUTING_CONTRACT_VERSION: 1.0.0

## Purpose

Make the Project Control Center the authoritative dispatcher for repository, product-family, client-variant, and change-scope selection before implementation workers modify code.

The owner may identify work using only a project name, client name, variant name, or registered alias. The dispatcher resolves that label to the canonical repository and target boundary and emits a routing packet. Workers do not guess.

## Canonical hierarchy

`PORTFOLIO -> PROJECT/REPOSITORY -> PRODUCT FAMILY (optional) -> VARIANT/CLIENT (optional) -> TASK -> WORKER`

A repository is either:
- `STANDALONE`: one canonical product/project boundary; or
- `PRODUCT_FAMILY`: one product lineage containing multiple long-lived variants or client editions.

A long-lived client variant is not defined by a Git branch. Branches are implementation state. Variant identity is explicit governance metadata.

## Mandatory repository constitution

Every newly enrolled repository must declare its worker contract in a repository-root constitution, normally `AGENTS.md`.

For product families, the repository must also contain a machine-readable family manifest, normally `.pcc/project-family.json`.

A newly enrolled project with `CONSTITUTION_STATE=PENDING` is not worker-routable. Fleet enrollment may collect it read-only, but implementation dispatch remains blocked until the constitution is installed and centrally marked `READY`.

`LEGACY_PENDING` is allowed only for repositories enrolled before this routing contract. It preserves fleet visibility but is not equivalent to routing readiness and must be migrated before implementation workers are centrally dispatched there.

## Worker start law

Every implementation worker MUST receive an authoritative PCC routing packet before write operations.

The routing packet must contain at least:
- `PROJECT_ID`
- `REPOSITORY`
- `PROJECT_MODEL`
- `TARGET_SCOPE`
- `TARGET_VARIANT` when applicable
- `CONSTITUTION_PATH`
- `FAMILY_MANIFEST_PATH` when applicable
- `READ_FIRST`
- `CHANGE_BOUNDARY`
- cross-variant validation requirements

If no valid route exists, the worker may inspect read-only but must return `ROUTING_REQUIRED` or the specific routing blocker. It must not infer the client or target from branch names, filenames, deployment names, or historical habit.

## Alias resolution

The routing registry may define aliases for projects and variants. Aliases are case-insensitive and punctuation/spacing-insensitive for routing purposes.

A variant alias may resolve directly to its parent project. Example: a user request naming a client variant is sufficient to route to the owning repository when the alias is unique.

Alias collisions are governance blockers.

## Product-family scope

A product-family task must resolve to one of:
- `CORE`: shared product behavior; potentially affects every active variant.
- `VARIANT`: one explicitly named client/product variant.

`CORE` changes require validation across all active variants.

`VARIANT` changes must not leak client branding, configuration, content, deployment settings, or behavior to siblings.

If the physical boundary is unknown, the target repository constitution must treat `UNKNOWN` as a write blocker until discovery establishes the correct boundary.

## Central dispatcher operating contract

The owner can start a task by providing the PCC dispatcher with a project/client label and the requested work. The dispatcher must:
1. fetch live PCC state;
2. resolve the label using `portfolio/project-routing.json`;
3. verify constitution/routing readiness;
4. fetch live target-repository state;
5. determine `CORE`, `VARIANT`, or `PROJECT` scope from the request and evidence;
6. emit the worker routing packet with exact repository and variant identity;
7. only then hand implementation to a worker.

If scope is ambiguous and evidence cannot resolve it safely, implementation is blocked instead of guessed.

## Onboarding gate

`portfolio/project-routing.json` must contain exactly one routing record for every registered project in `portfolio/projects.yml`.

Newly added projects must not reach fleet onboarding readiness while their routing declaration is missing or `CONSTITUTION_STATE=PENDING`.

This routing contract does not weaken existing write authorization, CANARY/ENFORCE, lineage, break-glass, artifact provenance, or QA gates.
