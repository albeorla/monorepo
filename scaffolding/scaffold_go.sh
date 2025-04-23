#!/usr/bin/env bash
set -euo pipefail
NAME=$1
DIR="go/${NAME}"
mkdir -p "${DIR}"
cat > "${DIR}/main.go" <<EOF
package main
import "fmt"
func main() {
    fmt.Println("Hello from ${NAME}")
}
EOF
cat > "${DIR}/BUILD.bazel" <<EOF
load("@io_bazel_rules_go//go:def.bzl", "go_binary")
go_binary(
    name = "${NAME}",
    srcs = ["main.go"],
    importpath = "example.com/${NAME}",
)
EOF
echo "Created Go module ${NAME}"
