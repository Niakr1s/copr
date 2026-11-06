#!/usr/bin/env bash

# This tool builds a src.rpm packages

SPECS_DIR="$HOME/rpmbuild/SPECS"

build() {
  local spec="$1"

  echo "Building: $spec"
  spectool -g -R "$spec"
  rpmbuild -bs "$spec"
}

buildall() {
  for spec in "$SPECS_DIR"/*.spec; do
    build "$spec"
  done
}

SPEC="$1"

if [[ -z "$SPEC" ]]; then
  buildall
else
  if [[ "$SPEC" != *".spec" ]]; then
    SPEC="$SPEC.spec"
  fi
  build "$SPECS_DIR/$SPEC"
fi
