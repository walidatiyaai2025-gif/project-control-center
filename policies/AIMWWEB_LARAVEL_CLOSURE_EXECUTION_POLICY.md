# AIMWWeb Laravel Remaining-Parity Closure Execution Policy

Authority: explicit owner constitutional amendment, 2026-10-27  
Project: `AIMWWEB`  
Target variant: `LARAVEL_AIWMWEB`  
Target repository charter: `.pcc/LARAVEL_AIWMWEB_VARIANT_CHARTER.md`

This policy governs the remaining canonical parity-closure work until the Laravel variant reaches 100% terminality in the full canonical operation reconciliation.

## Canonical task and branch law

- Every remaining canonical Task/operation has exactly one persistent Task ID and exactly one canonical implementation branch for its full lifecycle.
- The Manager/Lead creates or reconciles that canonical branch once before dispatch.
- Implementation Workers MUST NOT create a new, alternate, temporary, recovery, replacement, duplicate, or second branch for the same Task.
- A replacement Worker inherits the same Task ID, branch, PR, latest pushed SHA, evidence chain, and unresolved gaps.
- If no canonical branch has been supplied, the Worker returns `BRANCH_REQUIRED`; it does not invent one.

## Duplicate-work race gate

Before implementation writes, the Manager/Lead and Worker must reconcile the canonical Task/operation against:
- live issue state;
- open and recently merged PRs;
- active Worker leases;
- existing task branches;
- pushed commits and exact branch head;
- materially overlapping implementation scope.

Equivalent existing work is continued, never reimplemented. Stale chat state, historical task lists, branch counts, and issue counts are not authoritative.

## Ten-worker closure pool

- Maximum concurrent implementation Workers for this closure program: **10**.
- Keep up to 10 non-overlapping Task leases active whenever at least 10 dependency-safe READY canonical Tasks exist.
- One Worker owns one Task scope at a time.
- Two Workers may not own the same Task ID, operation ID, canonical branch, PR, or materially overlapping surface.
- When a Task is integrated and its canonical branch is retired, the freed slot may take the next READY Task only after a fresh duplicate/ownership race check.
- Parallelism must never be created by duplicating a Task or branch.

## Verified branch retirement

For this program, verified post-merge Task-branch deletion is mandatory task closure, not blind fleet cleanup.

The Integration Lead must verify:
1. the Task PR is merged into the approved integration lineage;
2. the exact canonical branch head is represented by the merge;
3. no unique unmerged commits remain on the canonical Task branch;
4. required CI/evidence is preserved by the merged lineage.

After those checks pass, the canonical Task branch must be deleted promptly.

Blind bulk deletion, deletion of unique unmerged work, deletion based only on branch naming, and force-push cleanup remain prohibited.

## Source of remaining work

The authoritative remaining-work pool is the latest **full canonical parity reconciliation plus live GitHub state**. A task is not created merely because an old issue, branch, or chat entry exists.

## Routing-packet requirements

Every routing packet for this program must include:
- the canonical Task ID;
- canonical operation ID;
- canonical Task branch;
- current Worker lease;
- exact starting SHA;
- duplicate/race-check result;
- approved integration target;
- branch-retirement requirement after verified merge;
- the 10-worker pool constraint.
