#!/usr/bin/env bash

echo "========================================"
echo "git-ai-commit installation started"
echo "========================================"

echo
echo "[1/7] Setting BIN_DIR..."
BIN_DIR="$HOME/.local/bin"
echo "BIN_DIR=$BIN_DIR"

echo
echo "[2/7] Creating BIN_DIR..."
mkdir -p "$BIN_DIR"
echo "BIN_DIR created: $BIN_DIR"

echo
echo "[3/7] Detecting PROJECT_DIR..."
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "PROJECT_DIR=$PROJECT_DIR"

echo
echo "[4/7] Copying launcher..."
echo "Source:      $PROJECT_DIR/launcher/git-ai-commit"
echo "Destination: $BIN_DIR/git-ai-commit"

cp "$PROJECT_DIR/launcher/git-ai-commit" "$BIN_DIR/git-ai-commit"

echo "Launcher copied successfully"

echo
echo "[5/7] Making launcher executable..."
chmod +x "$BIN_DIR/git-ai-commit"
echo "Launcher is executable"

echo
echo "[6/7] Setting INSTALL_DIR..."
INSTALL_DIR="$HOME/git-ai-commit"
echo "INSTALL_DIR=$INSTALL_DIR"

echo
echo "[7/7] Creating INSTALL_DIR and copying scripts..."
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
