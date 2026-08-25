# Database Migration Safety

Database changes must declare forward migration, compatibility window, backup/recovery posture, rollback or compensating strategy, data-loss risk, locking/downtime risk, deployment ordering, validation queries, and ownership.

Destructive or irreversible changes require explicit review and evidence. Application and schema compatibility must be proven across the intended rollout sequence. Never mark migration work DONE from code merge alone.
