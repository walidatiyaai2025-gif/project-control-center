# Portfolio Dashboard

Read-only projection of canonical portfolio and orchestration state.

Shows portfolio totals plus project health, progress, production version/SHA, development/target version/SHA, next release candidate, latest user-review candidate, P0, blocked, QA, stale, waiting-for-user, policy/version drift, last sync, maturity and control-plane version.

`build_portfolio.py` merges the project registry with observed orchestration metadata and generates `portfolio/status/index.json`. The dashboard never invents missing versions or SHAs.
