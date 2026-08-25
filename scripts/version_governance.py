#!/usr/bin/env python3
import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

SEMVER = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?(?:\+([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?$")
AMBIGUOUS_ARTIFACTS = {"final.zip", "final2.zip", "latest.zip", "final.apk", "final2.apk", "latest.apk", "new.exe", "latest.exe", "final.exe"}


def git(repo: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(repo), *args], text=True, stderr=subprocess.DEVNULL).strip()


def read_version(repo: Path, source: str) -> str:
    p = repo / source
    if not p.is_file():
        raise ValueError(f"canonical version source missing: {source}")
    value = p.read_text(encoding="utf-8").strip()
    if not value:
        raise ValueError("canonical version is empty")
    return value


def expected_tag(pattern: str, version: str, project: str) -> str:
    return pattern.replace("{version}", version).replace("{project}", project)


def expected_artifact_fragment(pattern: str, version: str, project: str) -> str:
    return pattern.replace("{version}", version).replace("{project}", project)


def released_mapping_error(version: str, source_sha: str, mapping: dict) -> str | None:
    old = mapping.get(version)
    if old and old != source_sha:
        return f"VERSION_REUSE: {version} already maps to {old}, attempted {source_sha}"
    return None


def normalize_mapping(doc: dict) -> dict[str, str]:
    if isinstance(doc.get("VERSIONS"), list):
        return {str(v.get("PRODUCT_VERSION")): str(v.get("SOURCE_SHA")) for v in doc["VERSIONS"] if v.get("PRODUCT_VERSION") and v.get("SOURCE_SHA")}
    return {str(k): str(v) for k, v in doc.items() if isinstance(v, str)}


def validate(repo: Path, project: str, source: str, policy: str, source_sha: str | None,
             display_version: str | None, package_version: str | None, endpoint_version: str | None,
             display_required: bool, endpoint_required: bool, artifact_name: str | None,
             artifact_pattern: str, official: bool, release_tag: str | None,
             tag_pattern: str, released_mapping: dict | None, release_notes: Path | None) -> tuple[str, str, list[str]]:
    errors: list[str] = []
    try:
        version = read_version(repo, source)
    except ValueError as exc:
        return "", source_sha or "", [str(exc)]

    if policy == "semantic" and not SEMVER.match(version):
        errors.append(f"INVALID_VERSION_FORMAT: {version}")

    if not source_sha:
        try:
            source_sha = git(repo, "rev-parse", "HEAD")
        except Exception:
            errors.append("SOURCE_SHA unavailable")
            source_sha = ""

    if display_required and not display_version:
        errors.append("VERSION_DISPLAY_REQUIRED but no observed display version was supplied")
    if display_version and display_version != version:
        errors.append(f"VERSION_DRIFT: display={display_version} canonical={version}")
    if package_version and package_version != version:
        errors.append(f"VERSION_DRIFT: package={package_version} canonical={version}")
    if endpoint_required and not endpoint_version:
        errors.append("VERSION_ENDPOINT_REQUIRED but no observed endpoint version was supplied")
    if endpoint_version and endpoint_version != version:
        errors.append(f"VERSION_DRIFT: endpoint={endpoint_version} canonical={version}")

    expected_artifact = expected_artifact_fragment(artifact_pattern, version, project)
    if official:
        if not artifact_name:
            errors.append("OFFICIAL_ARTIFACT_MISSING_NAME")
        else:
            base = Path(artifact_name).name
            if base.lower() in AMBIGUOUS_ARTIFACTS:
                errors.append(f"AMBIGUOUS_OFFICIAL_ARTIFACT_NAME: {base}")
            if version not in base:
                errors.append(f"OFFICIAL_ARTIFACT_MISSING_VERSION: {base} does not contain {version}")
            if expected_artifact and expected_artifact not in base:
                errors.append(f"ARTIFACT_PATTERN_MISMATCH: expected fragment {expected_artifact} in {base}")
        if not release_tag:
            errors.append("OFFICIAL_RELEASE_TAG_REQUIRED")
        if not release_notes or not release_notes.is_file():
            errors.append("OFFICIAL_RELEASE_NOTES_REQUIRED")
        else:
            notes = release_notes.read_text(encoding="utf-8", errors="replace")
            if version not in notes:
                errors.append(f"RELEASE_NOTES_VERSION_MISMATCH: {version} not found")

    tag = expected_tag(tag_pattern, version, project)
    if release_tag and release_tag != tag:
        errors.append(f"TAG_VERSION_MISMATCH: expected {tag}, got {release_tag}")

    try:
        existing = git(repo, "rev-list", "-n", "1", f"refs/tags/{tag}")
    except Exception:
        existing = ""
    if existing and source_sha and existing != source_sha:
        errors.append(f"VERSION_REUSE: tag {tag} already maps to {existing}, attempted {source_sha}")

    if released_mapping is not None and source_sha:
        err = released_mapping_error(version, source_sha, normalize_mapping(released_mapping))
        if err:
            errors.append(err)

    return version, source_sha or "", errors


def digest_file(path: Path | None) -> str | None:
    if not path or not path.is_file():
        return None
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return "sha256:" + h.hexdigest()


def build_manifest(project: str, version: str, source_sha: str, control_plane_version: str,
                   release_tag: str | None, artifact_name: str | None, artifact_path: Path | None,
                   build_id: str | None) -> dict:
    run_no = os.getenv("GITHUB_RUN_NUMBER", "local")
    attempt = os.getenv("GITHUB_RUN_ATTEMPT", "1")
    return {
        "PROJECT_ID": project,
        "PRODUCT_VERSION": version,
        "SOURCE_SHA": source_sha,
        "BUILD_ID": build_id or f"{run_no}.{attempt}",
        "BUILD_TIME": dt.datetime.now(dt.timezone.utc).isoformat(),
        "CONTROL_PLANE_VERSION": control_plane_version,
        "CI_RUN_ID": os.getenv("GITHUB_RUN_ID", "LOCAL"),
        "ARTIFACT_DIGEST": digest_file(artifact_path),
        "RELEASE_TAG": release_tag,
        "ARTIFACT_NAME": artifact_name,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="PCC immutable product version guard")
    ap.add_argument("--repo", default=".")
    ap.add_argument("--project", required=True)
    ap.add_argument("--version-source", default="VERSION")
    ap.add_argument("--version-policy", default="semantic", choices=["semantic", "stack-native", "none-nonproduct"])
    ap.add_argument("--source-sha")
    ap.add_argument("--display-version")
    ap.add_argument("--package-version")
    ap.add_argument("--endpoint-version")
    ap.add_argument("--display-required", action="store_true")
    ap.add_argument("--endpoint-required", action="store_true")
    ap.add_argument("--official", action="store_true")
    ap.add_argument("--artifact-name")
    ap.add_argument("--artifact-path")
    ap.add_argument("--artifact-pattern", default="{project}-{version}")
    ap.add_argument("--release-tag")
    ap.add_argument("--tag-pattern", default="v{version}")
    ap.add_argument("--release-notes")
    ap.add_argument("--released-mapping")
    ap.add_argument("--control-plane-version", default="v1.1.0")
    ap.add_argument("--build-id")
    ap.add_argument("--manifest-out", default="version-manifest.json")
    args = ap.parse_args()

    repo = Path(args.repo).resolve()
    mapping = json.loads(Path(args.released_mapping).read_text(encoding="utf-8")) if args.released_mapping else None
    release_notes = Path(args.release_notes).resolve() if args.release_notes else None

    version, source_sha, errors = validate(
        repo, args.project, args.version_source, args.version_policy, args.source_sha,
        args.display_version or None, args.package_version or None, args.endpoint_version or None,
        args.display_required, args.endpoint_required, args.artifact_name or None,
        args.artifact_pattern, args.official, args.release_tag or None, args.tag_pattern,
        mapping, release_notes,
    )

    if errors:
        for e in errors:
            print("ERROR", e)
        return 1

    manifest = build_manifest(
        args.project, version, source_sha, args.control_plane_version,
        args.release_tag or expected_tag(args.tag_pattern, version, args.project),
        args.artifact_name or None,
        Path(args.artifact_path).resolve() if args.artifact_path else None,
        args.build_id,
    )
    out = Path(args.manifest_out)
    out.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
