#!/usr/bin/env bash

echo "========================================"
echo "git-ai-commit installation started"
echo "========================================"

echo
echo "[1/9] Setting BIN_DIR..."
BIN_DIR="$HOME/.local/bin"
echo "BIN_DIR=$BIN_DIR"

echo
echo "[2/9] Creating BIN_DIR..."
mkdir -p "$BIN_DIR"
echo "BIN_DIR created: $BIN_DIR"

echo
echo "[3/9] Detecting PROJECT_DIR..."
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "PROJECT_DIR=$PROJECT_DIR"

echo
echo "[4/9] Copying launcher..."
echo "Source:      $PROJECT_DIR/launcher/git-ai-commit"
echo "Destination: $BIN_DIR/git-ai-commit"

cp "$PROJECT_DIR/launcher/git-ai-commit" "$BIN_DIR/git-ai-commit"

echo "Launcher copied successfully"

echo
echo "[5/9] Making launcher executable..."
chmod +x "$BIN_DIR/git-ai-commit"
echo "Launcher is executable"

echo
echo "[6/9] Setting INSTALL_DIR..."
INSTALL_DIR="$HOME/git-ai-commit"
echo "INSTALL_DIR=$INSTALL_DIR"

echo
echo "[7/9] Creating INSTALL_DIR and copying scripts..."
mkdir -p "$INSTALL_DIR"

echo "Source:      $PROJECT_DIR/scripts/"
echo "Destination: $INSTALL_DIR/"

cp -r "$PROJECT_DIR/scripts/." "$INSTALL_DIR/"

echo "Scripts copied successfully"

echo
echo "========================================"
echo "Installation completed successfully"
echo "========================================"
echo
echo "Launcher:"
echo "  $BIN_DIR/git-ai-commit"
echo
echo "Application:"
echo "  $INSTALL_DIR"
echo
echo
echo "[8/9] Checking Python..."
PYTHON=$(which python)

if [ -z "$PYTHON" ]; then
    echo "Python не найден"
    exit 1
fi

echo "Python found: $PYTHON"
"$PYTHON" --version

echo
echo "[9/9] Installing Python dependencies..."

REQUIREMENTS_FILE="$PROJECT_DIR/requirements.txt"

if [ ! -f "$REQUIREMENTS_FILE" ]; then
    echo "ERROR: requirements.txt not found: $REQUIREMENTS_FILE"
    exit 1
fi

echo "Installing dependencies from:"
echo "  $REQUIREMENTS_FILE"

"$PYTHON" -m pip install -r "$REQUIREMENTS_FILE"

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install Python dependencies"
    exit 1
fi

echo "Python dependencies installed successfully"
