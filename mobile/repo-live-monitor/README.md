# PCC Repo Live Android

Task: PCC-MOB-001 / Issue #29

A small Android companion for Project Control Center that talks directly to the GitHub REST API.

## Runtime flow

1. On first launch, enter a GitHub personal access token.
2. The token is validated against /user and stored with Android secure storage.
3. The first operational screen loads every repository visible to the token into a project/repository dropdown.
4. Selecting a repository loads a GitHub-Branches-style live dashboard.
5. Branch lists refresh every 15 seconds. Pending checks refresh each cycle; completed branch details receive a periodic full refresh.
6. Pull to refresh forces a full branch/check refresh.

## Branch data shown

- Default, Yours, Active, Stale and All filters.
- Branch search.
- Last commit time.
- Ahead/behind counts versus the default branch.
- Aggregate GitHub check-runs plus commit statuses.
- Open pull request number and direct GitHub link.

Stale means the branch has not received a commit for 90 days.

## Security

No GitHub credential is compiled into the APK or committed to the repository. The user-supplied token is stored using flutter_secure_storage. Disconnect GitHub from the app menu to delete it.

For private repositories, the token must have enough read permission for repository metadata and the endpoints the app displays, including contents/commits, pull requests, and checks/actions where applicable.

## Build

The isolated workflow .github/workflows/pcc-mob-001-android-apk.yml generates a release APK from this source without changing the existing PCC runtime.
