#!/usr/bin/env python3
"""Rewrite manifest.json so Terbium's source URL points at this image build."""
import json
import os
import pathlib
import subprocess
import sys

tag = sys.argv[1]
checksum, filename = subprocess.check_output(
    ["sha256sum", *pathlib.Path("output").glob("*.zip")], text=True
).split()
filename = pathlib.Path(filename).name
size = pathlib.Path("output", filename).stat().st_size
repo = os.environ["GITHUB_REPOSITORY"]
sha = os.environ["GITHUB_SHA"]
published = subprocess.check_output(["date", "-u", "+%Y-%m-%dT%H:%M:%SZ"], text=True).strip()
url = f"https://github.com/{repo}/releases/download/{tag}/{filename}"
path = pathlib.Path("manifest.json")
manifest = json.loads(path.read_text())
manifest["updated_at"] = published
channel = manifest["channels"]["stable"]
channel["latest"] = tag
channel["releases"] = [tag] + [item for item in channel.get("releases", []) if item != tag]
channel["releases"] = channel["releases"][:20]
manifest["releases"][tag] = {
    "version": tag,
    "channel": "stable",
    "released_at": published,
    "summary": "MacThing page, no Spotify daemon.",
    "changelog": f"Built from {sha}.",
    "changelog_url": f"https://github.com/{repo}/releases/tag/{tag}",
    "yanked": None,
    "deprecated": False,
    "download": {"url": url, "size": size, "sha256": checksum},
}
path.write_text(json.dumps(manifest, indent=2) + "\n")
