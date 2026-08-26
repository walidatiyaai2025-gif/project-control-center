# Emergency Production Incident & Temporary Mitigation Policy

POLICY_ID: EMERGENCY_PRODUCTION_INCIDENT_POLICY
POLICY_VERSION: 1.0.0
APPLIES_TO: All PCC-managed projects and product-family variants

## 1. Purpose

Production incidents sometimes require a narrow tactical mitigation before a complete root-cause correction can be safely designed and released. PCC permits that emergency path, but a temporary production fix MUST NOT disappear from project memory or be treated as permanent completion.

The governing invariant is:

`PRODUCTION INCIDENT -> SERVICE RESTORATION -> INCIDENT RECORD -> PERMANENT FIX TASK -> REGRESSION PROTECTION -> FUTURE RELEASE ACCOUNTING -> PERMANENT CLOSURE`

`SERVICE RESTORED != INCIDENT DONE` when the deployed correction is temporary.

## 2. Emergency activation

The emergency path is activated when the owner explicitly marks the request as a production emergency, including phrases such as:

- `مشكلة طارئة`
- `production emergency`
- `emergency hotfix`
- `P0 production incident`

It may also be activated from verified live production evidence showing material outage, security exposure, data-integrity risk, broken authentication/access, critical payment/transaction failure, or equivalent severe regression.

The Manager/Lead MUST still fetch live PCC and target-repository state and resolve the project/variant boundary. Emergency status does not authorize guessing the repository or client variant.

## 3. Stabilization-first rule

Restoring safe production service has priority over normal backlog sequencing.

A Manager/Lead may route a narrow emergency mitigation immediately when:

- the production target and affected boundary are verified;
- the mitigation is limited to the incident;
- unrelated refactoring or feature work is excluded;
- current production base SHA/version is recorded;
- rollback/recovery remains possible where technically applicable.

Governance recording MUST NOT unnecessarily delay a safe service-restoration action. However, before authoritative final closure, the incident record and permanent-fix tracking required by this policy must exist.

## 4. Canonical incident identity

Every production emergency receives one canonical `INCIDENT_ID` and one machine-readable incident record.

Recommended identity:

`INC-<PROJECT_ID>-<YYYY>-<NNNN>`

The target repository MUST persist the incident under:

`.pcc/incidents/<INCIDENT_ID>.json`

before the emergency work can be reported as fully reconciled.

The incident record is durable project memory. It travels with the repository and must remain understandable to a replacement Manager/Lead without chat history.

## 5. Temporary mitigation state

If the deployed production correction is tactical, partial, configuration-based, compatibility-oriented, rollback-oriented, time-boxed, or otherwise not the intended final architecture, it is a `TEMPORARY_MITIGATION`.

The highest valid completion state after such a deployment is:

`SERVICE_RESTORED_TEMPORARY`

or, once permanent work is registered:

`TRACKED_FOR_PERMANENT_FIX`.

A temporary mitigation MUST NOT by itself produce `DONE`, `CLOSED`, `PERMANENTLY_RESOLVED`, or equivalent final language.

## 6. Permanent-fix debt is mandatory

When `PERMANENT_FIX_REQUIRED=true`, the incident MUST have:

- a canonical permanent-fix Task ID;
- a target project/variant scope;
- a permanent-fix target version or explicit `NEXT_RELEASE` target when the project has no established semantic version yet;
- root-cause investigation state;
- required regression-test plan;
- carry-forward state for future releases.

The permanent-fix task is not optional cleanup. It is a first-class delivery obligation created by the emergency incident.

If the permanent fix can safely be completed in the same emergency task, the incident may transition directly through permanent validation without leaving open debt.

## 7. Future-release accounting

Every unresolved temporary mitigation MUST be surfaced during each later release decision for the affected project/variant until permanently resolved.

A future release MUST NOT silently omit, overwrite, revert, or forget the mitigation/debt.

For every affected release, the Release Lead must establish one of:

1. the permanent fix is included and validated; or
2. the temporary mitigation remains intentionally compatible and the permanent-fix task is still scheduled; or
3. the owner explicitly approves deferral to a named later target version/release.

Deferral does not close the incident. It only updates the target version and preserves the open obligation.

## 8. Regression protection

A production incident that reached users or production traffic requires regression protection unless technically impossible.

`REGRESSION_TEST_REQUIRED=true` is the default for temporary production mitigations.

Permanent closure requires evidence that reproduces the failure mode at the appropriate level and proves the corrected behavior, for example:

- automated unit/integration/E2E regression test;
- deployment verification test;
- migration/data-integrity verification;
- exact production-path verification where automation is not feasible.

If automation is technically impossible, the incident record must state why and preserve repeatable manual verification evidence.

## 9. Product-family / variant behavior

For `PRODUCT_FAMILY` repositories:

- a variant-only production incident remains isolated to the routed variant unless live evidence proves a shared root cause;
- if root cause is shared, the permanent fix must be reclassified to `CORE` and validated across all affected active variants;
- a tactical patch in one client variant must not silently become shared behavior;
- future-release accounting is performed for every affected variant.

## 10. Required traceability

A reconciled emergency incident records, at minimum:

- `INCIDENT_ID`
- `PROJECT_ID`
- repository and scope/variant
- severity
- production base SHA and affected version when known
- detection timestamp
- temporary mitigation Task ID / branch / SHA when used
- deployment/service-restoration evidence
- root-cause state and summary
- `PERMANENT_FIX_REQUIRED`
- permanent-fix Task ID and target version when required
- regression-test requirement/evidence
- carry-forward state
- release-gate state
- permanent-fix SHA when resolved

## 11. Closure gate

An incident may enter `CLOSED` only when all required permanent work is complete.

For an incident that used a temporary mitigation, `CLOSED` requires:

- root cause confirmed;
- permanent-fix task completed;
- permanent-fix SHA recorded;
- required regression evidence recorded;
- release gate cleared;
- no unresolved carry-forward obligation.

A restored service with open permanent-fix debt remains open and visible.

## 12. Prohibited emergency shortcuts

Emergency status does not authorize:

- force-pushing or discarding unique work;
- bypassing project/variant routing;
- inventing production lineage;
- weakening authentication, authorization, transport security, or data-integrity controls without explicit owner-approved risk handling;
- merging unrelated features/refactors into the hotfix;
- deleting the incident record after service restoration;
- marking temporary mitigation as final completion.

## 13. Replacement Manager / Lead law

A replacement Manager/Lead MUST be able to inspect the target repository `.pcc/incidents/` records plus PCC tasks/releases and immediately identify:

- which production incidents used temporary fixes;
- what exact SHA restored service;
- which permanent fixes remain outstanding;
- which future release/version must account for each unresolved incident.

No conversational memory is required or authoritative.
