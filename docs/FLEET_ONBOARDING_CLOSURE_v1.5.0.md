# PCC v1.5.0 — Fleet Onboarding Closure

## Mission
Make the Project Control Center fleet-generic and machine-verifiable before adding the remaining repositories.

## Closure delivered
- removed single-pilot assumptions from central self-audit and CI document validation;
- added `scripts/fleet_readiness.py` with explicit `READINESS_PERCENT` and `ONBOARDING_READY` outputs;
- added multi-project onboarding acceptance tests, including duplicate-repository, unsafe write-mode and non-allowlisted-path rejection;
- aligned onboarding templates to the current control-plane version and complete fleet enrollment metadata;
- integrated readiness validation into Control Plane Validation, live Fleet Control artifacts and the published dashboard projection;
- preserved the rule that OBSERVE/WARN policy drift is expected pre-promotion and does not falsely make the control plane itself “not ready” to enroll more repositories;
- preserved separate per-project promotion gates for CANARY/ENFORCE, including explicit write authorization, resolved lineage, break-glass checks, allow-listed managed paths and write-capable runtime authentication.

## 100% definition
For the `FLEET_ONBOARDING` readiness profile, `READINESS_PERCENT=100` and `ONBOARDING_READY=true` require all static readiness checks to pass. When a full live fleet report is provided, every registered project must also have successful live collection, discovery complete, baseline locked and read-only reconciliation complete.

This 100% value means **ready to add more projects safely**. It deliberately does not claim that every project is ready for autonomous writes or production release.

## External administration
PCC main branch protection and first-time GitHub Pages enablement can require repository-administration authority not available to the workflow token. Those states must be reported truthfully and never converted to a false PASS. They do not mutate target repositories and do not invalidate the fleet-onboarding software acceptance profile.
