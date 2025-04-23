#!/usr/bin/env bash
# -----------------------------------------------------------------------------
# Create (or refresh) a local Python virtual‑environment that mirrors the exact
# package versions Bazel assembles via rules_python.
# -----------------------------------------------------------------------------
#
# Usage (from repo root):
#   ./scripts/setup_venv.sh
#   source .venv/bin/activate
# -----------------------------------------------------------------------------

set -euo pipefail

LOCK_FILE="requirements_lock.txt"
VENV_DIR=".venv"

if [[ ! -f "${LOCK_FILE}" ]]; then
  echo "[!] ${LOCK_FILE} not found—cannot continue." >&2
  exit 1
fi

if [[ ! -d "${VENV_DIR}" ]]; then
  echo "[+] Creating Python virtual‑environment at ${VENV_DIR}"
  python -m venv "${VENV_DIR}"
fi

# shellcheck disable=SC1090
source "${VENV_DIR}/bin/activate"

echo "[+] Installing dependencies from ${LOCK_FILE}"
python -m pip install --upgrade pip wheel >/dev/null
pip install -r "${LOCK_FILE}" >/dev/null

echo "[✓] .venv ready – activate with: source ${VENV_DIR}/bin/activate"