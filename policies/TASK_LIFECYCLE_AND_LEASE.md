# Task Lifecycle and Worker Lease

Allowed states:

`AVAILABLE`, `READY`, `CLAIMED`, `IN_PROGRESS`, `BLOCKED`, `STALE`, `RECLAIMABLE`, `READY_FOR_REVIEW`, `READY_FOR_QA`, `QA_PASS`, `INTEGRATED`, `RELEASED`, `DONE`.

Worker ownership is a temporary lease. Canonical Task identity and canonical Task branch are persistent.

If a Worker disappears or stops:

- keep the same TASK ID;
- keep the same canonical branch;
- discover and record the latest pushed SHA;
- transfer the worker lease;
- continue from existing evidence.

Creating a duplicate implementation branch merely because a Worker stopped is prohibited. A replacement branch is last resort and requires documented evidence that the canonical branch cannot safely be continued.

A task becomes `STALE` only by policy-defined inactivity/evidence criteria, not personal judgment. `RECLAIMABLE` means ownership may be transferred after branch/SHA/PR reconciliation.
