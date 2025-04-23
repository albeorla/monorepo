#!/usr/bin/env bash
set -euo pipefail
NAME=$1
DIR="rust/${NAME}"
cargo new --bin "${DIR}"
cat > "${DIR}/BUILD.bazel" <<EOF
load("@rules_rust//rust:rust.bzl", "rust_binary")
rust_binary(
    name = "${NAME}",
    srcs = ["src/main.rs"],
    edition = "2021",
)
EOF
echo "Created Rust module ${NAME}"
