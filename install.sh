#!/usr/bin/env bash

BIN_DIR="$HOME/.local/bin"
mkdir -p "$BIN_DIR"

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cp "$PROJECT_DIR/launcher/git-ai-commit" "$BIN_DIR/git-ai-commit"
chmod +x "$BIN_DIR/git-ai-commit"

INSTALL_DIR="$HOME/git-ai-commit"
mkdir -p "$INSTALL_DIR"
cp -r "$PROJECT_DIR/scripts/." "$INSTALL_DIR/"
