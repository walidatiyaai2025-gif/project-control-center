# User Acceptance and Delivery Gateway

Only the DELIVERY / CONTROL LEAD may publish authoritative overall project status to the user. Individual Workers report Task-local state only.

Authoritative delivery references `CANONICAL_INTEGRATION_SHA`, `PRODUCTION_SHA`, `LATEST_RELEASE` and current product version identity where applicable. It states complete/incomplete, blocked/waiting work and distinguishes verified facts from pending acceptance.

A user-review build must identify PROJECT, PRODUCT_VERSION, BUILD_ID, SOURCE_SHA, CI_STATUS, QA_STATUS, WHAT_CHANGED and WHAT_TO_VERIFY. It must originate from an approved immutable source state and obey `IMMUTABLE_PRODUCT_VERSION_POLICY.md`.

Anonymous authoritative builds such as `latest.apk`, `final.zip`, `new.exe`, or an arbitrary Worker-branch build are forbidden. Competing Worker summaries are non-authoritative.
