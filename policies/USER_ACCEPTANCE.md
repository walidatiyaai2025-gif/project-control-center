# User Acceptance and Delivery Gateway

Only the DELIVERY / CONTROL LEAD may publish authoritative overall project status. Individual Workers report Task/Feature-local state only.

Authoritative delivery references `CANONICAL_INTEGRATION_SHA`, `PRODUCTION_SHA`, `LATEST_RELEASE`, product version/build identity, requested review scope, Feature Delivery Matrix results, Screen Inventory, Screen Action connectivity, QA state and customer-ready evidence.

`READY_FOR_USER` requires the requested customer-review scope to have no unresolved applicable `IMPLEMENTED_NOT_CONNECTED`, `UI_ONLY`, `BACKEND_ONLY`, `UNREACHABLE_SCREEN`, `MISSING_UI_BINDING`, `PERSISTENCE_GAP`, `FALSE_SUCCESS_RISK`, fake-data path or official-build-identity gap unless explicitly waived by documented policy exception.

The user-facing handoff distinguishes code completion, connectivity completion, QA completion, customer-ready completion and release completion. Competing Worker summaries and raw code percentages are non-authoritative.
