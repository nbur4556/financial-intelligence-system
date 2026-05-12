
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"

"$SCRIPT_DIR/.venv/bin/pip3.13" install -r "$SCRIPT_DIR/requirements.txt"
