SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"

"$SCRIPT_DIR/.venv/bin/python3.13" "$SCRIPT_DIR/scripts/etl.py"
