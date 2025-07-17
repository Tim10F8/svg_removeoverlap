#!/bin/bash
# this_file: scripts/test.sh
# Quick test script

set -e

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

# Colors for output
GREEN='\033[0;32m'
NC='\033[0m' # No Color

print_step() {
    echo -e "${GREEN}▶ $1${NC}"
}

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    print_step "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies if not present
if ! python -c "import pytest" 2>/dev/null; then
    print_step "Installing test dependencies..."
    pip install -e .[testing]
fi

# Run tests
print_step "Running tests..."
python -m pytest tests/ -v "$@"