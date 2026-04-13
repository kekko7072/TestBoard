#!/usr/bin/env bash
set -euo pipefail

# ── Helpers ───────────────────────────────────────────────────────────────────
red()   { echo -e "\033[0;31m$*\033[0m"; }
green() { echo -e "\033[0;32m$*\033[0m"; }
bold()  { echo -e "\033[1m$*\033[0m"; }

# ── Version argument ──────────────────────────────────────────────────────────
if [[ $# -lt 1 ]]; then
  bold "Usage: ./scripts/release.sh <version>"
  echo  "       e.g.  ./scripts/release.sh 1.2.0"
  exit 1
fi

VERSION="$1"

# Strip leading 'v' if provided, then rebuild the tag
VERSION="${VERSION#v}"
TAG="v${VERSION}"

# Validate semver (MAJOR.MINOR.PATCH)
if ! [[ "$VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
  red "Error: version must be in MAJOR.MINOR.PATCH format (e.g. 1.2.0)"
  exit 1
fi

# ── Git checks ────────────────────────────────────────────────────────────────
if ! git rev-parse --git-dir > /dev/null 2>&1; then
  red "Error: not inside a git repository"
  exit 1
fi

# Ensure we are on main
BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [[ "$BRANCH" != "main" ]]; then
  red "Error: releases must be made from main (currently on '$BRANCH')"
  exit 1
fi

# Ensure working tree is clean
if ! git diff --quiet || ! git diff --cached --quiet; then
  red "Error: working tree has uncommitted changes — commit or stash them first"
  exit 1
fi

# Ensure tag does not already exist
if git rev-parse "$TAG" > /dev/null 2>&1; then
  red "Error: tag $TAG already exists"
  exit 1
fi

# Pull latest to avoid out-of-date releases
bold "Pulling latest changes from origin/main..."
git pull --ff-only origin main

# ── Create and push tag ───────────────────────────────────────────────────────
bold "Creating tag $TAG..."
git tag -a "$TAG" -m "Release $TAG"

bold "Pushing tag to origin..."
git push origin "$TAG"

green "Done! Release $TAG triggered."
echo  "Follow the build at: $(git remote get-url origin | sed 's/\.git$//')/actions"
