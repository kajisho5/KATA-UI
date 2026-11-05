#!/usr/bin/env bash
# Inspect by default; install only with an explicit remote/setup opt-in.
set -u
trap 'status=$?; if [ "$status" -ne 0 ]; then printf "Setup warning: stopped with status %s; session may continue.\n" "$status"; fi; exit 0' EXIT
ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd) || exit 0
cd "$ROOT" || exit 0
STATE="$ROOT/.agent"
INSTALL=false
if [ "${CLAUDE_CODE_REMOTE:-}" = true ] || [ "${AGENT_SETUP:-}" = 1 ]; then INSTALL=true; fi
printf 'Agent setup: %s\nInstall opt-in: %s\n' "$ROOT" "$INSTALL"
PYTHON=python3
if [ -x "$STATE/venv/bin/python" ]; then PYTHON="$STATE/venv/bin/python"; fi
PYTHON_OK=false
if command -v python3 >/dev/null 2>&1 && python3 -c 'import sys;sys.exit(sys.version_info < (3,11))'; then
  PYTHON_OK=true
else
  printf 'Setup warning: python3 >=3.11 is required; install the runtime outside this helper.\n'
fi
NODE_OK=false
if command -v node >/dev/null 2>&1 && node -e 'process.exit(Number(process.versions.node.split(".")[0]) < 20 ? 1 : 0)'; then
  NODE_OK=true
else
  printf 'Setup warning: Node >=20 is required; install the runtime outside this helper.\n'
fi
if "$INSTALL"; then
  if "$PYTHON_OK"; then
    if ! "$PYTHON" -c 'import playwright.sync_api; import PIL' >/dev/null 2>&1; then
      if [ ! -x "$STATE/venv/bin/python" ]; then
        if ! python3 -m venv "$STATE/venv"; then printf 'Setup warning: venv creation failed; python3-venv may be missing.\n'; fi
      fi
      if [ -x "$STATE/venv/bin/python" ]; then
        PYTHON="$STATE/venv/bin/python"
        if ! "$PYTHON" -m pip install --disable-pip-version-check --cache-dir "$STATE/pip-cache" -r tools/agent-requirements.txt; then
          printf 'Setup warning: Python dependency install failed (network or package access); browser checks may be unavailable.\n'
        fi
      fi
    else
      printf 'Python browser/image dependencies already available.\n'
    fi
    CHROMIUM_AVAILABLE=false
    if command -v chromium >/dev/null 2>&1 || command -v chromium-browser >/dev/null 2>&1; then
      CHROMIUM_AVAILABLE=true
    elif "$PYTHON" -c 'from pathlib import Path;from playwright.sync_api import sync_playwright
with sync_playwright() as p: assert Path(p.chromium.executable_path).is_file()' >/dev/null 2>&1; then
      CHROMIUM_AVAILABLE=true
    fi
    if ! "$CHROMIUM_AVAILABLE"; then
      if [ "$(id -u)" -eq 0 ]; then
        if ! "$PYTHON" -m playwright install --with-deps chromium; then printf 'Setup warning: Chromium/system dependency installation failed.\n'; fi
      else
        if ! "$PYTHON" -m playwright install chromium; then printf 'Setup warning: Chromium installation failed; system libraries may require an administrator.\n'; fi
      fi
    else
      printf 'Chromium already available.\n'
    fi
  fi
  if "$NODE_OK" && command -v npm >/dev/null 2>&1; then
    if ! npm --cache "$STATE/npm-cache" install --prefix cli --ignore-scripts --no-package-lock --no-audit --no-fund; then
      printf 'Setup warning: CLI npm dependency installation failed.\n'
    fi
  else
    printf 'Setup warning: CLI dependency install skipped; Node >=20 and npm are required.\n'
  fi
else
  printf 'Inspection only. Set CLAUDE_CODE_REMOTE=true or AGENT_SETUP=1 to install.\n'
fi
printf '\nAvailable tools\n'
for tool in python3 node npm git gh chromium chromium-browser; do
  if command -v "$tool" >/dev/null 2>&1; then
    printf '%s: %s\n' "$tool" "$(command -v "$tool")"
  else printf '%s: unavailable\n' "$tool"; fi
done
if command -v python3 >/dev/null 2>&1; then "$PYTHON" --version; fi
if command -v node >/dev/null 2>&1; then node --version; fi
if "$PYTHON" -c 'import playwright.sync_api;import PIL' >/dev/null 2>&1; then
  "$PYTHON" -c 'import importlib.metadata as m;print("Playwright: "+m.version("playwright"));print("Pillow: "+m.version("Pillow"))'
else printf 'Playwright/Pillow: unavailable; browser/image verification must be reported as unverified.\n'; fi
if [ -x "$STATE/venv/bin/python" ]; then printf 'Before manual commands: source .agent/venv/bin/activate\n'; fi
if [ ! -x /usr/bin/chromium ]; then printf 'Setup warning: some existing regression scripts require /usr/bin/chromium; a managed browser alone does not satisfy those hard-coded paths.\n'; fi
if command -v node >/dev/null 2>&1; then
  node -e 'const p=require("./cli/package.json");console.log("CLI test command: "+(p.scripts?.test || "unavailable in this checkout; PR #25 is required"))'
fi
printf 'Agent setup completed; no merge, publish, deprecate or PR/issue closure was performed.\n'
exit 0
