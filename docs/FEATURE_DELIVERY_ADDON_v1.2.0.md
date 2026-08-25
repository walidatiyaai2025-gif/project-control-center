# PCC v1.2.0 — Feature Delivery Matrix & End-to-End Connectivity Add-on

This is an in-place, backward-compatible PCC capability upgrade from v1.1.0. It preserves task identity, version governance, orchestration and existing project history.

## Added

- `END_TO_END_FEATURE_DELIVERY_POLICY`
- canonical Feature Delivery Matrix, Screen Inventory and Screen Action Matrix templates/schemas
- deterministic feature-state derivation
- explicit `IMPLEMENTED_NOT_CONNECTED`, `BACKEND_ONLY`, `UI_ONLY` and `UNREACHABLE_SCREEN` handling
- persistence/reload and false-success gates
- fake-data and official-build presence findings
- reusable feature-delivery governance workflow
- Worker/QA/Integration/Release/User Delivery contract integration
- dashboard metrics separating code, connectivity, QA, customer-ready and release completion
- `FALSE_DONE_FEATURES` portfolio invariant

## Migration

Existing managed products are not rewritten. During their next reconciliation/onboarding update, discover current feature/screen/action reality and seed canonical matrices from live evidence. Unknown dimensions remain `NOT_STARTED`/explicitly unknown; irrelevant dimensions are `NOT_APPLICABLE`. Do not backfill historical DONE claims as verified without evidence.
