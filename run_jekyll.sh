#!/usr/bin/env bash
set -euo pipefail 2>/dev/null || set -eu

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cd "$ROOT_DIR"

require_cmd() {
  command -v "$1" >/dev/null 2>&1
}

gem_user_bin() {
  ruby -e 'print Gem.user_dir' 2>/dev/null || true
}

install_deps() {
  if ! require_cmd sudo; then
    echo "sudo not found. Please install dependencies manually." >&2
    exit 1
  fi

  sudo apt update
  sudo apt install -y jekyll ruby-full build-essential zlib1g-dev
}

ensure_gems() {
  # Ensure user-installed gems are on PATH
  GEM_USER_DIR="$(gem_user_bin)"
  if [ -n "${GEM_USER_DIR}" ]; then
    export PATH="${GEM_USER_DIR}/bin:$PATH"
  fi

  # Needed for the TOC plugin in _config.yml
  if ! gem list -i jekyll-toc >/dev/null 2>&1; then
    gem install --user-install jekyll-toc
  fi

  if ! gem list -i jekyll-theme-minimal >/dev/null 2>&1; then
    gem install --user-install jekyll-theme-minimal
  fi

  if ! gem list -i jekyll-relative-links >/dev/null 2>&1; then
    gem install --user-install jekyll-relative-links
  fi
}

if ! require_cmd jekyll; then
  install_deps
fi

ensure_gems

# Ensure user-installed gems are on PATH (for jekyll-toc, etc.)
GEM_USER_DIR="$(gem_user_bin)"
if [ -n "${GEM_USER_DIR}" ]; then
  export PATH="${GEM_USER_DIR}/bin:$PATH"
fi

echo "Local preview: http://localhost:4000/"
jekyll serve --livereload --baseurl "" --destination ".jekyll/_site" --source .
