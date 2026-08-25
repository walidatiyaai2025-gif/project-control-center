# Rollback, Production Verification and Incident Management

Every release with meaningful production risk defines rollback or forward-fix before deployment. Production verification validates deployed artifact/source/version identity and critical smoke checks.

Every release rollback record includes `PREVIOUS_KNOWN_GOOD_VERSION` and `PREVIOUS_KNOWN_GOOD_SHA` when a prior good release exists. Rollback deploys that real immutable prior identity; it never rebuilds changed source under an old version number or moves an immutable release tag.

Incidents receive incident ID, severity, start/detection times, affected project/version/release/SHA, containment, evidence, owner, current state, resolution and follow-up tasks. Incident fixes still require canonical Task IDs; emergency handling shortens lead time, not traceability or version immutability.
