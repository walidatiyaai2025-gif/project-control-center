# PCC v1.6.0 — Constitutional Decision & Variant Onboarding

## Goal

Make two behaviors durable and replacement-Lead-safe:

1. decisions that change operating governance are persisted to committed PCC constitution/policy rather than living only in chat;
2. project/client variant organization is automatically owned by PCC during onboarding.

## Accepted model

- Owner says which repository/project to add; PCC Manager performs classification.
- `STANDALONE` and `PRODUCT_FAMILY` are evidence-backed classifications.
- Family variants are explicit governance entities, not permanent branch names.
- Each active variant records implementation-location state and routing state.
- Unresolved/unmaterialized variants stay visible and block only their own route.
- Shared-core work is blocked until the core boundary is proven.
- A project can be normalized with `VARIANT_GOVERNANCE_STATE=PARTIAL` without fabricating missing code locations.
- The owner's add/onboard instruction authorizes only governance-only onboarding changes, never product-source changes or deployment.

## Continuity law

A replacement Manager/Lead must be able to recover the complete routing/variant model from committed PCC `main` plus the target repository constitution/family manifest. Conversational memory is not required or authoritative.

## First pilot

`NOTONLYBOOK` is the first product-family pilot. Current live evidence proves the repository root theme is the NotOnlyBook theme. ArabiasWonders is owner-declared but no implementation location is proven in the current repository/branch set, so it must remain visible and routing-blocked until mapped/materialized rather than guessed.
