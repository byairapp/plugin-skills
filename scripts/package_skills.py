#!/usr/bin/env python3
"""Validate and package the four byAir skills using only the standard library."""

import argparse
import re
import sys
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo


ROOT = Path(__file__).resolve().parents[1]
NAMES = (
    "byair-flight-brief",
    "byair-trip-brief",
    "byair-import-itinerary",
    "byair-flight-history",
)


def skill_bytes(name):
    path = ROOT / "skills" / name / "SKILL.md"
    if path.is_symlink():
        raise ValueError(f"{name}: SKILL.md must be a regular file")
    content = path.read_bytes()
    text = content.decode("utf-8")
    match = re.fullmatch(
        r"---\nname: ([a-z0-9-]+)\ndescription: ([^\n]+)\n---\n\n(.+)",
        text,
        re.DOTALL,
    )
    if not match:
        raise ValueError(f"{name}: expected name/description YAML frontmatter and body")
    declared_name, description, body = match.groups()
    if declared_name != name or len(name) > 64:
        raise ValueError(f"{name}: invalid name or folder mismatch")
    if not 1 <= len(description) <= 200 or any(c in description for c in "<>\r"):
        raise ValueError(f"{name}: description must be 1..200 characters without XML")
    if ": " in description or " #" in description:
        raise ValueError(f"{name}: description needs YAML quoting; adjust validator if used")
    if len(body.splitlines()) >= 500 or not body.strip():
        raise ValueError(f"{name}: body must be nonempty and below 500 lines")
    if re.search(r"\b(?:TODO|FIXME|TBD)\b|\[INSERT", body):
        raise ValueError(f"{name}: unfinished placeholder")
    print(f"Validated {name}: description {len(description)} chars")
    return content


def verify_archive(path, expected):
    with ZipFile(path) as archive:
        if sorted(archive.namelist()) != sorted(expected):
            raise ValueError(f"{path.name}: unexpected archive structure")
        if archive.testzip() is not None:
            raise ValueError(f"{path.name}: corrupt archive")
        for name, content in expected.items():
            if archive.read(name) != content:
                raise ValueError(f"{path.name}: stale content for {name}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify existing archives only")
    args = parser.parse_args()
    skills = {name: skill_bytes(name) for name in NAMES}
    packages = {
        f"{name}.zip": {f"{name}/SKILL.md": content}
        for name, content in skills.items()
    }
    packages["byair-agent-skills.zip"] = {
        f"{name}/SKILL.md": content for name, content in skills.items()
    }
    output = ROOT / "dist"
    if not args.check:
        output.mkdir(exist_ok=True)
    for filename, entries in packages.items():
        path = output / filename
        if not args.check:
            with ZipFile(path, "w", compression=ZIP_DEFLATED) as archive:
                for name, content in sorted(entries.items()):
                    info = ZipInfo(name, date_time=(2026, 10, 7, 0, 0, 0))
                    info.compress_type = ZIP_DEFLATED
                    info.create_system = 3
                    info.external_attr = 0o100644 << 16
                    archive.writestr(info, content)
        verify_archive(path, entries)
        print(f"Verified dist/{filename}")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError) as error:
        print(f"Packaging failed: {error}", file=sys.stderr)
        sys.exit(1)
