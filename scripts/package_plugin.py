#!/usr/bin/env python3
"""Build and verify the OpenAI directory ZIP without developer or private files."""

import argparse
import json
import re
import struct
import sys
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

from package_skills import NAMES, ROOT, skill_bytes, verify_archive


def package_entries():
    manifest = json.loads((ROOT / "plugin.json").read_text())
    mcp = json.loads((ROOT / "mcp.json").read_text())
    interface = manifest["extensions"]["com.openai"]["interface"]
    version = manifest["version"]
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        raise ValueError("version must have three numeric components")
    if manifest["name"] != "byair" or manifest["license"] != "MIT":
        raise ValueError("unexpected plugin identity or license")
    for name, limit in (("displayName", 30), ("shortDescription", 30), ("longDescription", 4000)):
        if not 1 <= len(interface[name]) <= limit:
            raise ValueError(f"{name} must contain 1..{limit} characters")
    prompts = interface.get("defaultPrompt", [])
    if len(prompts) > 3 or any(len(prompt) > 128 for prompt in prompts):
        raise ValueError("starter prompt limits exceeded")
    expected_mcp = {"byair": {"type": "streamable-http", "url": "https://api.byairapp.com/mcp"}}
    if mcp["mcpServers"] != expected_mcp:
        raise ValueError("MCP configuration must use the public production OAuth endpoint")
    cases = manifest["extensions"]["com.openai"]["review"]["test_cases"]
    if len(cases["positive"]) != 5 or len(cases["negative"]) != 3:
        raise ValueError("review requires five positive and three negative cases")
    paths = [Path(name) for name in ("plugin.json", "mcp.json", "README.md", "LICENSE")]
    for field in ("logo", "composerIcon"):
        value = interface[field]
        if not value.startswith("./assets/") or ".." in Path(value).parts:
            raise ValueError(f"{field} must reference a bundled asset")
        paths.append(Path(value))
    discovered = {p.name for p in (ROOT / "skills").iterdir() if p.is_dir()}
    if discovered != set(NAMES):
        raise ValueError("skill folders differ from the declared byAir skills")
    for name in NAMES:
        skill_bytes(name)
        dependency = ROOT / "skills" / name / "agents" / "openai.yaml"
        if not dependency.is_file():
            raise ValueError(f"{name}: missing OpenAI MCP dependency")
        paths.extend(p.relative_to(ROOT) for p in (ROOT / "skills" / name).rglob("*") if p.is_file())
    entries = {}
    for relative in sorted(set(paths)):
        path = ROOT / relative
        if path.is_symlink() or not path.is_file() or not path.resolve().is_relative_to(ROOT):
            raise ValueError(f"invalid package file: {relative}")
        content = path.read_bytes()
        if len(content) > 5 * 1024 * 1024:
            raise ValueError(f"package file too large: {relative}")
        if path.suffix in (".json", ".md", ".yaml"):
            text = content.decode("utf-8")
            if re.search(r"api_key=|-----BEGIN .*PRIVATE KEY-----|\bBearer [A-Za-z0-9_.-]+", text):
                raise ValueError(f"credential-like material in public package: {relative}")
        entries[relative.as_posix()] = content
    icon = entries[Path(interface["logo"]).as_posix()]
    if not icon.startswith(b"\x89PNG\r\n\x1a\n"):
        raise ValueError("expected PNG logo")
    width, height = struct.unpack(">II", icon[16:24])
    if width != height or not 48 <= width <= 4096:
        raise ValueError("logo must be square and 48..4096 pixels")
    return version, entries


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify an existing ZIP against source")
    args = parser.parse_args()
    version, entries = package_entries()
    output = ROOT / "dist" / f"byair-openai-{version}.zip"
    if not args.check:
        output.parent.mkdir(exist_ok=True)
        with ZipFile(output, "w", compression=ZIP_DEFLATED) as archive:
            for name, content in entries.items():
                info = ZipInfo(name, date_time=(2026, 10, 7, 0, 0, 0))
                info.compress_type = ZIP_DEFLATED
                info.create_system = 3
                info.external_attr = 0o100644 << 16
                archive.writestr(info, content)
    verify_archive(output, entries)
    print(f"Verified {output.relative_to(ROOT)}: {len(entries)} files")
    print("Local package checks only; portal validation and review execution are separate.")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError) as error:
        print(f"Packaging failed: {error}", file=sys.stderr)
        sys.exit(1)
