#!/usr/bin/env bash
set -euo pipefail

echo "==> Installing Python libraries"
pip install --quiet pandas matplotlib seaborn python-telegram-bot python-dotenv

echo "==> Installing Typst (for standardised PDF reports)"
curl -fsSL https://github.com/typst/typst/releases/latest/download/typst-x86_64-unknown-linux-musl.tar.xz -o /tmp/typst.tar.xz
sudo tar -xJf /tmp/typst.tar.xz -C /opt
sudo ln -sf /opt/typst-x86_64-unknown-linux-musl/typst /usr/local/bin/typst
rm /tmp/typst.tar.xz
typst --version

echo "==> Installing Bun (for Claude Code channel plugins)"
if ! command -v unzip >/dev/null 2>&1; then
  sudo apt-get update
  sudo apt-get install -y unzip
fi
curl -fsSL https://bun.sh/install | bash
sudo ln -sf "$HOME/.bun/bin/bun" /usr/local/bin/bun
bun --version

echo "==> Installing Claude Code CLI"
export PATH="$HOME/.local/bin:$HOME/.claude/local:$HOME/.npm-global/bin:$PATH"
if ! command -v claude >/dev/null 2>&1; then
  curl -fsSL https://claude.ai/install.sh | bash
fi

if ! command -v claude >/dev/null 2>&1; then
  CLAUDE_BIN="$(find "$HOME/.claude" "$HOME/.local/bin" -type f -name claude -perm -u+x 2>/dev/null | head -n 1 || true)"
  if [ -n "$CLAUDE_BIN" ]; then
    sudo ln -sf "$CLAUDE_BIN" /usr/local/bin/claude
  fi
fi

if ! command -v claude >/dev/null 2>&1; then
  echo "==> Claude native installer did not expose 'claude' on PATH; trying npm fallback"
  mkdir -p "$HOME/.npm-global"
  npm config set prefix "$HOME/.npm-global"
  npm install -g @anthropic-ai/claude-code
fi

if ! grep -q 'HOME/.local/bin' "$HOME/.bashrc"; then
  echo 'export PATH="$HOME/.local/bin:$HOME/.claude/local:$HOME/.npm-global/bin:$PATH"' >> "$HOME/.bashrc"
fi

claude --version

echo "==> Done. Run 'claude' to start Claude Code, or open any module README to begin."
