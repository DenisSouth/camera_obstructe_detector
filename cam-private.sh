#!/usr/bin/env bash
# Use when camera should always be covered (privacy/tape-over policy).
# Alerts if camera gets uncovered. Skips silently if camera is in use.
CAMERA="${1:-0}"
THRESHOLD="${2:-0.2}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PYTHON="$SCRIPT_DIR/.venv/bin/python"
[ ! -f "$PYTHON" ] && PYTHON=python3

fuser "/dev/video${CAMERA}" > /dev/null 2>&1 && exit 0

"$PYTHON" "$SCRIPT_DIR/detector.py" -c "$CAMERA" -t "$THRESHOLD"
code=$?
[ $code -eq 0 ] && notify-send -u critical "Camera Exposed" "Camera ${CAMERA} is uncovered"
