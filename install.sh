#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV="$SCRIPT_DIR/.venv"
BIN="$HOME/.local/bin"

echo "Creating virtual environment..."
python3 -m venv "$VENV"
"$VENV/bin/pip" install -q -r "$SCRIPT_DIR/requirements.txt"

mkdir -p "$BIN"

cat > "$BIN/cam-guard" << EOF
#!/usr/bin/env bash
exec "$SCRIPT_DIR/cam-guard.sh" "\$@"
EOF

cat > "$BIN/cam-private" << EOF
#!/usr/bin/env bash
exec "$SCRIPT_DIR/cam-private.sh" "\$@"
EOF

chmod +x "$BIN/cam-guard" "$BIN/cam-private"

echo ""
echo "Done. Commands installed to $BIN:"
echo "  cam-guard   [camera] [threshold]  — alert if camera gets covered"
echo "  cam-private [camera] [threshold]  — alert if camera gets uncovered"
echo ""

if [[ ":$PATH:" != *":$BIN:"* ]]; then
    echo "Add to your shell config:"
    echo '  export PATH="$HOME/.local/bin:$PATH"'
fi
