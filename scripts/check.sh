#!/usr/bin/env bash
set -euo pipefail

repository_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repository_dir"

python3 -m compileall -q app delivery scripts tests
python3 -m unittest discover -s tests -v
python3 scripts/check.py
git diff --check

