#!/usr/bin/env python3
"""
Usage: bump_version.py [major|minor|patch]
E.g.:
    ./bump_version.py patch
"""

import re
import sys
from pathlib import Path

if len(sys.argv) != 2 or sys.argv[1] not in ("major", "minor", "patch"):
    print(__doc__)
    sys.exit(1)

bump_type = sys.argv[1]

# Files to update
FILES = [
    Path("config/default.yaml"),
    Path("pyproject.toml"),
    Path("README.md"),
]

# Regex to find version strings like 1.2.3
VERSION_RE = re.compile(r"(\d+)\.(\d+)\.(\d+)")

def bump(v: str) -> str:
    major, minor, patch = map(int, v.split("."))
    if bump_type == "major":
        major += 1; minor = 0; patch = 0
    elif bump_type == "minor":
        minor += 1; patch = 0
    else:
        patch += 1
    return f"{major}.{minor}.{patch}"

# Read current version from the first file
text = FILES[0].read_text()
m = VERSION_RE.search(text)
if not m:
    print("Could not find version in", FILES[0])
    sys.exit(1)

old_version = m.group(0)
new_version = bump(old_version)
print(f"Bumping version: {old_version} → {new_version}")

# Apply to all files
for f in FILES:
    content = f.read_text()
    updated = VERSION_RE.sub(new_version, content)
    f.write_text(updated)
    print(f"  Updated {f}")

print("Done!")
