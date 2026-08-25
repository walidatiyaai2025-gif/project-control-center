# Execution Output Discipline & No-Narration Policy

POLICY_ID: EXECUTION_OUTPUT_DISCIPLINE_POLICY
POLICY_VERSION: 1.0.0
CONTROL_PLANE_VERSION: v1.4.0
SILENT_EXECUTION_BY_DEFAULT: TRUE

## Fundamental law
Operational roles execute first and report verified state only:

`READ -> INVESTIGATE -> EXECUTE -> VALIDATE -> RECONCILE EVIDENCE -> REPORT`

Investigation diaries, sequential hypotheses, raw tool-operation commentary, premature conclusions, speculative findings, temporary contradictions and private reasoning are not user-facing delivery output.

## Covered roles
This policy is mandatory for Implementation Worker, Continuation Worker, QA Worker, CI Investigator, Visual QA Worker, Integration Lead, Release Lead, Recovery Worker, Drift Auditor and Fleet Controller. Delivery / Control Lead may publish project-wide synthesized state, but must not publish the investigation process.

## Human output contract
Normal user-facing operational output is limited to:
- final verified result;
- genuine blocker;
- required user/admin action;
- structured handoff;
- requested evidence;
- next action.

Machine/audit channels may retain request logs, API responses, diagnostic traces, intermediate findings and reconciliation detail. Human delivery must contain verified state, evidence-backed conclusion, blocker and next action.

## Prohibited intermediate output
Do not emit routine narration such as `I will check`, `I am reviewing`, `I found the first`, `next I will`, `it seems`, `probably`, `maybe`, or `I suspect` when execution can continue automatically. Do not expose chain-of-thought, scratchpad analysis or temporary hypotheses as project state.

## No-premature-finding law
Raw signals are not conclusions. `mergeable=false`, a screenshot, a failed step, an old workflow run, or a stale branch status must be reconciled against its domain, exact source identity and current evidence before user delivery. Contradictory signals must resolve to `RESOLVED_STATE` or `UNRESOLVED_BLOCKER`; the discovery process is not streamed.

## Exact-head evidence gate
Before authoritative CI, QA, integration or release conclusions, establish as applicable: repository, branch, HEAD SHA, base SHA, PR, workflow run, artifact source SHA, screenshot source SHA and build/version identity. Evidence from different source identities must not be presented as one coherent result.

## Artifact provenance gate
Screenshots, APKs, ZIPs, reports, goldens and QA artifacts must track where applicable:
- ARTIFACT_ID;
- SOURCE_SHA;
- WORKFLOW_RUN;
- GENERATED_AT;
- TARGET.

If provenance cannot prove the artifact belongs to the candidate under evaluation, classify it `STALE_OR_UNVERIFIED_ARTIFACT`. A screenshot may not override exact-head application state without provenance. Use `ARTIFACT_DELTA_REQUIRES_PROVENANCE` until exact-head evidence is established.

## Visual QA provenance
Authoritative Visual QA requires `REFERENCE_SOURCE`, `REFERENCE_VERSION`, `REFERENCE_SHA` when applicable, `CANDIDATE_SOURCE_SHA`, `CANDIDATE_ARTIFACT`, `ARTIFACT_GENERATED_AT`, and `PROVENANCE_VERIFIED`. PASS/FAIL is not authoritative when `PROVENANCE_VERIFIED=false`; it must remain preliminary/non-authoritative.

## Output confidence
Every final conclusion is classified as exactly one of `VERIFIED`, `PARTIALLY_VERIFIED`, `BLOCKED`, or `UNKNOWN`. UNKNOWN must not be translated into confident prose.

## Contradiction gate
Before delivery, reject unresolved combinations such as CI GREEN + CI FAILED for the same exact source, QA PASS with failed gates, authoritative QA with unknown artifact provenance, or MERGEABLE + NOT_MERGEABLE without domain resolution. Stale evidence may not be described as current.

## Genuine blocker exception
Immediate output is allowed only when execution cannot safely continue. A blocker handoff must include TASK/scope, exact head or explicit UNKNOWN, blocker, why execution cannot continue, required action and next action. No investigative narration is added.

## User-requested live progress exception
When the operator explicitly requests live progress, concise milestone updates are allowed. Multi-paragraph reasoning narratives remain prohibited.

## Structured role contracts
### Implementation / Continuation Worker
`TASK`, `STATUS`, `HEAD`, `CHANGED`, `VALIDATION`, `NEXT_ACTION`.

### QA Worker
`QA_RESULT`, `EXACT_HEAD`, `BUILD_VERSION`, `ACCEPTANCE_GATES`, `FAILED_GATES`, `EVIDENCE`.

### CI Investigator
`EXACT_HEAD`, `WORKFLOW`, `JOB`, `STEP`, `TEST`, `ROOT_CAUSE`, `CLASSIFICATION`, `OWNER`.

### Visual QA
`EXACT_HEAD`, `REFERENCE_SOURCE`, `REFERENCE_VERSION`, `REFERENCE_SHA`, `CANDIDATE_SOURCE_SHA`, `CANDIDATE_ARTIFACT`, `ARTIFACT_GENERATED_AT`, `PROVENANCE_VERIFIED`, `DELTA`, `CLASSIFICATION`, `QA_RESULT`.

### Integration Lead
`INTEGRATION_HEAD`, `CANDIDATE`, `MERGE_STATE`, `CI`, `QA`, `BLOCKERS`, `RESULT`.

### Release Lead
`VERSION`, `SOURCE_SHA`, `BUILD_ID`, `QA`, `RELEASE_STATE`, `PRODUCTION_STATE`, `ROLLBACK`.

Each contract is machine-checkable through the matching schema and `scripts/output_discipline.py`.

## Worker prompt requirement
Every managed operational Worker prompt must include:

```text
OUTPUT MODE: SILENT EXECUTION
Do not narrate investigation.
Do not send intermediate hypotheses.
Execute available actions directly.
Return only final verified handoff or a genuine blocker requiring external input.
```

## Enforcement
Structured handoff schemas are primary enforcement. Keyword/narration detection is secondary. Unsupported DONE, missing exact HEAD for authoritative exact-head workflows, unproven artifact provenance, speculative authoritative QA, mismatched artifact SHA, stale screenshot conclusions and unresolved contradictory states are rejected.

## Policy integration
This policy is incorporated by reference into Task Lifecycle/Worker governance, CI/QA/Visual QA, Integration/Release, Recovery, User Acceptance/Delivery, Definition of Done and all managed operational prompt templates.

## Final state law
Human operational delivery should contain `RESULT`, `EVIDENCE`, `BLOCKER`, `NEXT ACTION` — not what the Worker thought while investigating.
