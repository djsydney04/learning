#!/usr/bin/env bash
# Educational completion check. Run with: bash scripts/check.sh <target>
set -euo pipefail
cd "$(dirname "$0")/.."

target="${1:-examples}"
case "$target" in
  examples|solutions|all|01|02|03|04|05) ;;
  *) printf 'Usage: bash scripts/check.sh [examples|01|02|03|04|05|solutions|all]\n' >&2; exit 2 ;;
esac

if ! command -v lake >/dev/null 2>&1; then
  printf 'Lake was not found. Follow lessons/00_SETUP.md, then reopen your terminal.\n' >&2
  exit 127
fi

lake build
check_file() {
  printf '\nChecking %s\n' "$1"
  lake env lean -DwarningAsError=true "$1"
}

# Check source directly as well, so cached builds cannot hide warnings.
check_file Course/Models.lean
check_file Course/Examples.lean

case "$target" in
  examples) ;;
  solutions)
    for file in solutions/*.lean; do check_file "$file"; done
    ;;
  all)
    for file in exercises/*.lean; do check_file "$file"; done
    ;;
  *)
    for file in exercises/"${target}"_*.lean; do check_file "$file"; done
    ;;
esac

printf '\nPASS: %s (Lean reported no errors or warnings).\n' "$target"
