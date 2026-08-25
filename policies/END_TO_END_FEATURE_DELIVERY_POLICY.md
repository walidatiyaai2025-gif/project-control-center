# End-to-End Feature Delivery Policy

Policy ID: `END_TO_END_FEATURE_DELIVERY_POLICY`
Policy version: `1.0.0`
Introduced in: `PCC v1.2.0`

## Fundamental law

`CODE EXISTS != FEATURE COMPLETE`
`SCREEN EXISTS != FEATURE COMPLETE`
`BACKEND READY != CUSTOMER READY`
`IMPLEMENTED != INTEGRATED`
`INTEGRATED != RELEASED`
`RELEASED != USER VERIFIED`

A feature is DONE only when every applicable required delivery dimension passes. Irrelevant dimensions must be explicitly `NOT_APPLICABLE`; they are not silently ignored.

## Canonical records

Managed repositories must maintain canonical Feature Delivery Matrix, Screen Inventory, and Screen Action Matrix records. The schemas and templates in this control plane are authoritative for their shape. Summary states are derived by `scripts/feature_delivery_audit.py`; Workers may not override a failing derived state by writing `DONE`.

## Dimension states

Only: `NOT_APPLICABLE`, `NOT_STARTED`, `IN_PROGRESS`, `IMPLEMENTED`, `CONNECTED`, `VERIFIED`, `FAILED`, `BLOCKED`.

## Feature delivery dimensions

Applicable dimensions cover requirement/business rules, backend/database/API/service/UI implementation, navigation, UI/API binding, data binding, mutations, permissions, validation, loading/empty/error/retry states, persistence/reload, background/notification paths, feature flags, end-to-end verification, QA, customer visibility, release and user acceptance.

## Derived feature states

The audit derives one of: `PLANNED`, `IMPLEMENTATION_STARTED`, `PARTIALLY_IMPLEMENTED`, `BACKEND_ONLY`, `UI_ONLY`, `IMPLEMENTED_NOT_CONNECTED`, `CONNECTED_NOT_VERIFIED`, `END_TO_END_WORKING`, `QA_FAILED`, `QA_VERIFIED`, `CUSTOMER_READY`, `RELEASED`, `USER_ACCEPTED`, `DONE`.

`IMPLEMENTED_NOT_CONNECTED`, `BACKEND_ONLY`, and `UI_ONLY` never count as customer-ready completion unless the delivery type explicitly makes the absent dimension not applicable.

## Screen inventory

Each customer-facing screen records route/reachability, authorization, authoritative data, actions, validation and UX states, responsive/accessibility/RTL/LTR, QA, visibility and release. `VISUAL_COMPLETION` and `FUNCTIONAL_COMPLETION` are separate derived metrics. A visually complete screen may still be functionally incomplete.

A route that exists but has no valid navigation/deep-link path and is not intentionally hidden is classified `UNREACHABLE_SCREEN`.

## Screen action matrix

Every meaningful action records visibility, enablement, permission, handler, backend connection, success/failure paths, persistence, reload verification and QA. A visible button is not a complete action.

State-changing actions must use server-authoritative success. Showing success before required server mutation/persistence/reconciliation creates `FALSE_SUCCESS_RISK`.

## Real data and persistence

Customer-facing functions requiring production data must not be CUSTOMER_READY while using mock, hardcoded, demo, local-only or fake-success paths.

For state-changing features, the applicable acceptance journey is: action -> server commit -> authoritative reconciliation/reload -> result remains present. Failure after reload is `PERSISTENCE_GAP`.

## Official build connectivity

Source presence is tracked separately as `PRESENT_IN_DEVELOPMENT`, `PRESENT_IN_CANDIDATE`, `PRESENT_IN_PRODUCTION`. Customer visibility requires exact feature commits to be present in an official candidate or production build as appropriate. Worker branches do not establish customer visibility.

## Version traceability

Every customer-visible feature records `TARGET_VERSION`, `FIRST_CANDIDATE_VERSION`, and `RELEASED_IN_VERSION`, linked through Task/PR/source/build evidence.

## Defect classifications

Audits may emit: `DEAD_CODE_CANDIDATE`, `UNCONNECTED_FEATURE`, `UNREACHABLE_SCREEN`, `UNUSED_ENDPOINT`, `MISSING_CONSUMER`, `MISSING_UI_BINDING`, `MISSING_NAVIGATION`, `PERSISTENCE_GAP`, `FALSE_SUCCESS_RISK`, `FAKE_DATA_PATH`, `NOT_IN_OFFICIAL_BUILD`, `RELEASE_IDENTITY_GAP`, `FALSE_DONE_FEATURE`.

Static suspicion never authorizes automatic code deletion.

## Customer-ready gate

A feature becomes CUSTOMER_READY only when every applicable pre-release dimension passes, required end-to-end and QA verification pass, customer visibility is verified where applicable, and the exact feature is present in the official candidate/production source identity.

A project becomes READY_FOR_USER only when requested review scope has no unresolved required integration gaps (`IMPLEMENTED_NOT_CONNECTED`, `UI_ONLY`, `BACKEND_ONLY`, `UNREACHABLE_SCREEN`, `MISSING_UI_BINDING`, `PERSISTENCE_GAP`, `FALSE_SUCCESS_RISK`, or equivalent), unless a documented, approved policy exception applies.

Target invariant: `FALSE_DONE_FEATURES = 0`.

## Completion metrics

Expose separately: `CODE_COMPLETION`, `CONNECTIVITY_COMPLETION`, `QA_COMPLETION`, `CUSTOMER_READY_COMPLETION`, `RELEASE_COMPLETION`. Executive completion must favor customer-ready/release evidence over raw code completion.
