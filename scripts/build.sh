#!/bin/bash
# this_file: scripts/build.sh
# Local build and test script

set -e

echo "🔧 Building svg_removeoverlap..."
echo "================================"

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_step() {
    echo -e "${GREEN}▶ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

# Check Python version
print_step "Checking Python version..."
python3 --version

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    print_step "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
print_step "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
print_step "Upgrading pip..."
python -m pip install --upgrade pip

# Install build dependencies
print_step "Installing build dependencies..."
pip install build wheel twine tox

# Install package in development mode
print_step "Installing package in development mode..."
pip install -e .[testing]

# Run code quality checks
print_step "Running pre-commit hooks..."
pip install pre-commit
pre-commit run --all-files || print_warning "Pre-commit checks failed"

# Run tests
print_step "Running tests..."
python -m pytest tests/ -v --cov=svg_removeoverlap --cov-report=term-missing --cov-report=html

# Check mypy
print_step "Running mypy type checking..."
python -m mypy src/svg_removeoverlap/ || print_warning "Type checking issues found"

# Build distribution packages
print_step "Building distribution packages..."
python -m build

# Check distribution packages
print_step "Checking distribution packages..."
twine check dist/*

# Generate coverage report
print_step "Generating coverage report..."
coverage html
echo "Coverage report generated at: htmlcov/index.html"

echo ""
echo -e "${GREEN}✅ Build completed successfully!${NC}"
echo ""
echo "Distribution files:"
ls -la dist/
echo ""
echo "Next steps:"
echo "  • Review test coverage: htmlcov/index.html"
echo "  • Run release script: ./scripts/release.sh"
echo "  • Create git tag: git tag v1.0.0"