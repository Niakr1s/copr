#!/usr/bin/env bash

declare -A downloads=(
  ["$HOME/rpmbuild/SOURCES/llama-cpp-cmpfix-0.6.0.tar.gz"]="https://github.com/Niakr1s/llama.cpp/archive/refs/tags/v0.6.0.tar.gz"
  ["$HOME/rpmbuild/SOURCES/joystickwake-1.0.0.tar.gz"]="https://codeberg.org/forestix/joystickwake/archive/v1.0.tar.gz"
  ["$HOME/rpmbuild/SOURCES/nvidia-pstated-1.0.9.tar.gz"]="https://github.com/sasha0552/nvidia-pstated/archive/refs/tags/v1.0.9.tar.gz"
)

for path in "${!downloads[@]}"; do
  url="${downloads[$path]}"
  if [[ ! -e "$path" ]]; then
    wget -O "$path" "$url"
  fi
done
