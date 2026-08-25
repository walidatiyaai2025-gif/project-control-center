# Definition of Ready / Definition of Done

## Definition of Ready

A task is READY only when it has: canonical Task ID; requirement/source request; duplicate check; project ID; intended base lineage; canonical task branch name or creation plan; scope/non-scope; acceptance criteria; risk/dependencies; required validation; escalation path; and, for product functionality, linked Feature ID(s), applicable Screen/Action IDs, target version, and Feature Delivery Matrix dimensions.

## Definition of Done

DONE is terminal, evidence-based, and derived. Required evidence includes, when applicable: implementation commit SHA; PR; CI at exact SHA; QA; integration SHA; release/build identity; production verification; documentation/migration evidence; user acceptance/delivery state; and an end-to-end feature audit with no unresolved applicable connectivity gaps.

`CODE EXISTS != FEATURE COMPLETE`. `READY_FOR_QA`, `QA_PASS`, `INTEGRATED`, `RELEASED`, and `CUSTOMER_READY` are not synonyms for DONE.

For product functionality, a Worker may not manually choose DONE. `scripts/feature_delivery_audit.py` must derive a state compatible with DONE from the canonical Feature Delivery Matrix, Screen Inventory, and Screen Action Matrix. `IMPLEMENTED_NOT_CONNECTED`, `BACKEND_ONLY`, `UI_ONLY`, `UNREACHABLE_SCREEN`, `MISSING_UI_BINDING`, `PERSISTENCE_GAP`, `FALSE_SUCCESS_RISK`, fake-data paths, or absence from the official build block DONE unless explicitly not applicable or covered by an approved policy exception.

Target invariant: `FALSE_DONE_FEATURES = 0`.

A human-facing handoff cannot support DONE if it violates `EXECUTION_OUTPUT_DISCIPLINE_POLICY`: unsupported DONE, missing exact-head evidence, unresolved contradictory final state, or authoritative QA based on stale/unverified artifact provenance blocks completion.
