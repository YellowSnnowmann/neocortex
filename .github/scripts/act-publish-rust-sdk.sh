#!/usr/bin/env bash
# Run the Publish Rust SDK workflow locally with act (https://github.com/nektos/act).
# Requires: act, jq; .github/scripts/secrets.json with CARGO_REGISTRY_TOKEN.
# act expects secrets in KEY=value format; this script converts secrets.json to that.
#
# Usage:
#   ./act-publish-rust-sdk.sh              # simulate workflow_dispatch (manual trigger)
#   ./act-publish-rust-sdk.sh release       # simulate release published

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
SECRETS_JSON="$SCRIPT_DIR/secrets.json"
WORKFLOW=".github/workflows/publish-rust-sdk.yml"

if [[ ! -f "$SECRETS_JSON" ]]; then
  echo "Missing $SECRETS_JSON (see secrets.json.example or add CARGO_REGISTRY_TOKEN)." >&2
  exit 1
fi

if ! command -v jq &>/dev/null; then
  echo "jq is required to convert secrets.json to act's .env format. Install jq (e.g. brew install jq)." >&2
  exit 1
fi

# act expects KEY=value per line, not JSON
SECRETS_FILE=$(mktemp)
trap 'rm -f "$SECRETS_FILE"' EXIT
jq -r 'to_entries | map("\(.key)=\(.value)") | .[]' "$SECRETS_JSON" > "$SECRETS_FILE"

cd "$REPO_ROOT"

EVENT="${1:-workflow_dispatch}"
if [[ "$EVENT" == "release" ]]; then
  act release \
    -W "$WORKFLOW" \
    --secret-file "$SECRETS_FILE" \
    -e "$SCRIPT_DIR/release-event.json"
else
  act workflow_dispatch \
    -W "$WORKFLOW" \
    --secret-file "$SECRETS_FILE"
fi
