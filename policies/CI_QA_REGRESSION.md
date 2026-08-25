# CI, QA and Regression Policy

CI status is bound to an immutable commit SHA. A green result from another SHA is not evidence.

QA must record scope, environment, exact SHA/build identity, executed checks, failures, and disposition. Regression scope is risk-based and must include affected integration paths, localization/responsiveness where applicable, data/error/loading states, and previously fixed critical defects.

Tests must not be weakened merely to turn CI green. Flaky or obsolete tests must be classified and repaired or explicitly quarantined under the flaky-test policy.
