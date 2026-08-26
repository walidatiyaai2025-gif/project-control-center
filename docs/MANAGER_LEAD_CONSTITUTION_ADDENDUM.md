# Manager / Lead Constitution Addendum

This addendum records the constitutional hardening that makes the Project Control Center the mandatory management entrypoint before implementation work is dispatched.

Authoritative rules live in root `AGENTS.md`, `policies/GOVERNANCE_LAWS.md`, `policies/CENTRAL_ORCHESTRATION_POLICY.md`, and `policies/PROJECT_FAMILY_ROUTING_POLICY.md`.

A Manager/Lead must resolve project/client/variant identity, live repository state, task identity, canonical continuation branch, change boundary, and required validation before issuing a PCC Routing Packet to an implementation Worker.

Ambiguous routing is a write blocker. Product-family CORE changes require cross-variant validation; VARIANT changes must stay isolated. Manager/Lead responsibility continues through QA, integration, release/deployment when required, and final evidence reconciliation.
