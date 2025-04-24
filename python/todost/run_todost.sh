#!/usr/bin/env bash
# ----------------------------------------------------------------------------
# Helper script to run todost with proper environment variables
# ----------------------------------------------------------------------------

set -euo pipefail

# Directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${SCRIPT_DIR}"

# Default to running with Python
USE_CONTAINER=false

# Parse command line arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    -c|--container)
      USE_CONTAINER=true
      shift
      ;;
    *)
      # Unknown option
      echo "Unknown option: $1"
      echo "Usage: $0 [-c|--container]"
      exit 1
      ;;
  esac
done

# Load environment variables from .env file if it exists
ENV_FILE="${SCRIPT_DIR}/.env"
if [[ -f "${ENV_FILE}" ]]; then
  echo "[+] Loading environment from ${ENV_FILE}"
  # shellcheck disable=SC1090
  set -a
  source "${ENV_FILE}"
  set +a
  
  # Debug
  echo "[DEBUG] TODOIST_API_TOKEN is set to: ${TODOIST_API_TOKEN:0:4}..."
else
  echo "[!] No .env file found. Please create one based on .env.example"
  echo "    cp .env.example .env"
  echo "    Then edit .env to add your Todoist API token"
  exit 1
fi

# Check if Todoist API token is set
if [[ -z "${TODOIST_API_TOKEN:-}" ]]; then
  echo "[!] TODOIST_API_TOKEN environment variable is not set"
  echo "    Please set it in your .env file"
  exit 1
fi

# Set default output file if not specified
TODOST_OUTPUT_FILE="${TODOST_OUTPUT_FILE:-todoist_gtd_para.json}"

if [[ "$USE_CONTAINER" == "true" ]]; then
  echo "[+] Running todost exporter in container with output to ${TODOST_OUTPUT_FILE}"
  
  # Check if Docker is available
  if ! command -v docker &> /dev/null; then
    echo "[!] Docker is not installed or not in PATH"
    exit 1
  fi
  
  # Run using Docker
  docker run --rm \
    -e TODOIST_API_TOKEN="${TODOIST_API_TOKEN}" \
    -e TODOST_OUTPUT_FILE="/data/${TODOST_OUTPUT_FILE}" \
    -e LOG_LEVEL="${LOG_LEVEL:-INFO}" \
    -v "${SCRIPT_DIR}:/data" \
    ghcr.io/albeorla/todost:latest
  
  echo "[✓] Export completed successfully to ${TODOST_OUTPUT_FILE}"
else
  echo "[+] Running todost exporter with output to ${TODOST_OUTPUT_FILE}"

  # Try to use Python directly if in a virtual environment
  if [[ -n "${VIRTUAL_ENV:-}" ]]; then
    echo "[+] Running with Python in virtual environment"
    TODOIST_API_TOKEN="${TODOIST_API_TOKEN}" python todost.py --outfile="${TODOST_OUTPUT_FILE}"
  else
    # Create and activate a temporary virtual environment if not already in one
    echo "[+] Setting up a temporary virtual environment"
    TEMP_VENV="${SCRIPT_DIR}/.temp_venv"
    
    # Check if Python 3 is available
    if command -v python3 &> /dev/null; then
      PYTHON_CMD="python3"
    else
      PYTHON_CMD="python"
    fi
    
    # Create a temporary virtual environment if it doesn't exist
    if [[ ! -d "${TEMP_VENV}" ]]; then
      ${PYTHON_CMD} -m venv "${TEMP_VENV}"
    fi
    
    # Activate the virtual environment
    # shellcheck disable=SC1090
    source "${TEMP_VENV}/bin/activate"
    
    # Install required dependencies
    echo "[+] Installing required dependencies"
    pip install httpx pydantic pyyaml typer --quiet
    
    # Run the tool
    echo "[+] Running todost with Python"
    TODOIST_API_TOKEN="${TODOIST_API_TOKEN}" python todost.py --outfile="${TODOST_OUTPUT_FILE}"
    
    # Deactivate the virtual environment
    deactivate
    
    echo "[+] Cleaned up temporary environment"
  fi

  echo "[✓] Export completed successfully to ${TODOST_OUTPUT_FILE}"
fi