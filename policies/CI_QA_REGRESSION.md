# CI, QA and Regression Policy

CI status is bound to an immutable commit SHA. A green result from another SHA is not evidence.

QA must record scope, environment, exact SHA/build identity, executed checks, failures, and disposition. Regression scope is risk-based and includes affected integration paths, localization/responsiveness where applicable, data/loading/empty/error/retry states, and previously fixed critical defects.

For customer-facing functionality QA must verify actual end-to-end connectivity, not isolated component success: reachable screen; visible/enabled action; correct authorization; production service/API path; authoritative data flow; server-confirmed mutation; persistence; authoritative reload/reconciliation; truthful failure handling; and presence in the official candidate when required.

A screen, service, endpoint, button, or unit test passing in isolation cannot establish `END_TO_END_VERIFIED` or `QA_VERIFIED`. Mock/fake/local-only data must be flagged when real authoritative data is required.

Tests must not be weakened merely to turn CI green. Flaky or obsolete tests must be classified and repaired or explicitly quarantined under the flaky-test policy.
