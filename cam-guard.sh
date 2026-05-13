#!/usr/bin/env bash
# Use when camera should always be clear (e.g. security cam, always-on feed).
# Alerts if camera gets covered. Skips silently if camera is in use.
CAMERA="${1:-0}"
THRESHOLD="${2:-0.2}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PYTHON="$SCRIPT_DIR/.venv/bin/python"
[ ! -f "$PYTHON" ] && PYTHON=python3

fuser "/dev/video${CAMERA}" > /dev/null 2>&1 && exit 0

"$PYTHON" "$SCRIPT_DIR/detector.py" -c "$CAMERA" -t "$THRESHOLD"
code=$?
[ $code -eq 2 ] && notify-send -u critical "Camera Covered" "Camera ${CAMERA} may be obstructed"
