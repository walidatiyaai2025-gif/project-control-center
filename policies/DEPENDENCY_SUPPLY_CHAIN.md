# Dependency and Supply-Chain Controls

Dependency changes must be intentional, reviewable, and traceable. Prefer lockfiles/pinned resolution where supported. CI should surface vulnerable, deprecated, unmaintained, or unexpectedly transitive dependencies according to project risk.

Do not bypass signature/checksum/provenance controls to make a build pass. Major runtime/build dependency upgrades require compatibility evidence and rollback awareness.
