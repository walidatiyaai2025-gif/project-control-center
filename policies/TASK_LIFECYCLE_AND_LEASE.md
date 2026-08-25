# Task Lifecycle and Worker Lease

Allowed states:

`AVAILABLE`, `READY`, `CLAIMED`, `IN_PROGRESS`, `BLOCKED`, `STALE`, `RECLAIMABLE`, `READY_FOR_REVIEW`, `READY_FOR_QA`, `QA_PASS`, `INTEGRATED`, `RELEASED`, `DONE`.

Worker ownership is a temporary lease. Canonical Task identity and canonical Task branch are persistent.

If a Worker disappears or stops: keep the same TASK ID; keep the same canonical branch; discover and record latest pushed SHA; transfer the worker lease; continue from existing evidence. Creating a duplicate implementation branch merely because a Worker stopped is prohibited.

A task becomes `STALE` only by policy-defined inactivity/evidence criteria. `RECLAIMABLE` means ownership may be transferred after branch/SHA/PR reconciliation.

For product-function Tasks, state promotion is constrained by the Feature Delivery Matrix. Workers report Task/Feature/Screen IDs, backend/API/UI/navigation/binding/persistence/QA/customer-visibility status, target version, current head and next gap. A Worker is forbidden from returning an unqualified `DONE`. Product Tasks cannot reach DONE while their feature audit derives an integration-gap state or `FALSE_DONE_FEATURE`.

## Worker and recovery output
Implementation, continuation and recovery Workers use `SILENT_EXECUTION_BY_DEFAULT=TRUE` under `EXECUTION_OUTPUT_DISCIPLINE_POLICY`. They execute available actions without investigation narration and return only a structured final handoff or a genuine blocker requiring external input. Reclaimed evidence must be reconciled to the exact current head before it is reported as current.
