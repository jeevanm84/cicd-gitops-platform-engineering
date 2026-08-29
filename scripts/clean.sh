#!/usr/bin/env bash
set -euo pipefail

repository_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
target="$repository_dir/.local"

if [[ "$target" != "$repository_dir/.local" || ! "$target" == */cicd-gitops-platform-engineering/.local ]]; then
  echo "Refusing cleanup outside the repository .local directory." >&2
  exit 1
fi

if [[ -d "$target" ]]; then
  rm -rf -- "$target"
  echo "Removed generated local delivery state: $target"
else
  echo "No generated local state exists."
fi

