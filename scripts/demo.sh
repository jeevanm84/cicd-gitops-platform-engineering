#!/usr/bin/env bash
set -euo pipefail

repository_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
state_dir="$repository_dir/.local/state"
release_one="$repository_dir/examples/releases/1.0.0.json"
release_two="$repository_dir/examples/releases/1.1.0.json"

"$repository_dir/scripts/clean.sh"

for release in "$release_one" "$release_two"; do
  "$repository_dir/scripts/delivery.py" verify --release "$release"
  "$repository_dir/scripts/delivery.py" promote --release "$release" --environment development --state-dir "$state_dir" >/dev/null
  "$repository_dir/scripts/delivery.py" promote --release "$release" --environment staging --state-dir "$state_dir" >/dev/null
  "$repository_dir/scripts/delivery.py" promote --release "$release" --environment production --state-dir "$state_dir" --approval "change/demo-approved" >/dev/null
done

echo "Two releases promoted through all environments. Production is ready for the rollback lab."
"$repository_dir/scripts/delivery.py" status --state-dir "$state_dir"

