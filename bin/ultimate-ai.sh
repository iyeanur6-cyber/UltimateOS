#!/usr/bin/env bash
# UltimateOS Hardware Copilot Key Dispatcher (.sh)

MODE="${1:-gemini}"

case "$MODE" in
  gemini)  URL="https://gemini.google.com/app" ;;
  chatgpt) URL="https://chatgpt.com/" ;;
  claude)  URL="https://claude.ai/new" ;;
  *)       URL="https://gemini.google.com/app" ;;
esac

if command -v brave-browser >/dev/null 2>&1; then
  nohup brave-browser --new-tab "$URL" >/dev/null 2>&1 &
else
  nohup xdg-open "$URL" >/dev/null 2>&1 &
fi
