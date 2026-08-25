# Portfolio Dashboard

`index.html` is a read-only portfolio view. It renders `portfolio/status/index.json` when served from the repository/site layout. `build_portfolio.py` derives the summary from `portfolio/projects.yml` and canonical status records without accepting Worker percentage estimates.

The GitHub workflow builds and uploads a dashboard artifact. Publishing through GitHub Pages is intentionally not assumed; Pages can be enabled later without changing the data contract.
