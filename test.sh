SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"

export PYTHONPATH=$PYTHONPATH.
"$SCRIPT_DIR/.venv/bin/python3.13" "$SCRIPT_DIR/tests/test_etl.py"
