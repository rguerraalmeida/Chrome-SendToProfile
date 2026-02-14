#!/usr/bin/env bash
set -euo pipefail

RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m'

warn() { printf "${YELLOW}WARN${NC}: %s\n" "$1"; }
fail() { printf "${RED}FAIL${NC}: %s\n" "$1"; exit 1; }
ok() { printf "${GREEN}OK${NC}: %s\n" "$1"; }

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  fail "Not inside a git repository."
fi

branch="$(git branch --show-current)"
if [[ -z "$branch" ]]; then
  fail "Detached HEAD. Checkout a branch before creating a PR."
fi
ok "Current branch: $branch"

if ! git remote get-url origin >/dev/null 2>&1; then
  fail "No origin remote configured. Add one with: git remote add origin <repo-url>"
fi
ok "Origin remote configured."

if [[ -n "$(git status --porcelain)" ]]; then
  warn "Working tree has uncommitted changes. Commit before opening a PR."
else
  ok "Working tree clean."
fi

if git rev-parse --verify --quiet "origin/$branch" >/dev/null 2>&1; then
  ahead_count="$(git rev-list --count "origin/$branch..$branch" 2>/dev/null || echo 0)"
  if [[ "$ahead_count" -gt 0 ]]; then
    warn "Branch is ahead of origin/$branch by $ahead_count commit(s). Push first: git push -u origin $branch"
  else
    ok "Branch is pushed to origin/$branch."
  fi
else
  warn "Remote branch origin/$branch not found. First push: git push -u origin $branch"
fi

if command -v gh >/dev/null 2>&1; then
  if gh auth status >/dev/null 2>&1; then
    ok "GitHub CLI auth is ready."
  else
    warn "gh is installed but not authenticated. Run: gh auth login"
  fi
else
  warn "gh CLI not installed. Install GitHub CLI or create PR in the web UI."
fi

printf "\nPreflight complete. If warnings are resolved, create PR with:\n"
printf "  gh pr create --fill\n"
