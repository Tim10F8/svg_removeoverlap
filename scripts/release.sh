#!/bin/bash
# this_file: scripts/release.sh
# Release script for git-tag-based semver releases

set -e

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_step() {
    echo -e "${GREEN}▶ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
    exit 1
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

show_usage() {
    echo "Usage: $0 [major|minor|patch|VERSION]"
    echo ""
    echo "Examples:"
    echo "  $0 patch    # Increment patch version (e.g., 1.0.0 -> 1.0.1)"
    echo "  $0 minor    # Increment minor version (e.g., 1.0.0 -> 1.1.0)"
    echo "  $0 major    # Increment major version (e.g., 1.0.0 -> 2.0.0)"
    echo "  $0 1.2.3    # Set specific version"
    echo ""
    echo "This script will:"
    echo "  1. Run full build and test suite"
    echo "  2. Create and push a git tag"
    echo "  3. GitHub Actions will build and release automatically"
    exit 1
}

validate_version() {
    local version=$1
    if [[ ! $version =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
        print_error "Invalid version format: $version. Expected: X.Y.Z"
    fi
}

get_current_version() {
    # Get current version from git tags
    local current_version=$(git tag -l 'v*' | grep -E '^v[0-9]+\.[0-9]+\.[0-9]+$' | sort -V | tail -1)
    if [[ -z "$current_version" ]]; then
        echo "0.0.0"
    else
        echo "${current_version#v}"
    fi
}

increment_version() {
    local version=$1
    local increment_type=$2
    
    IFS='.' read -r -a version_parts <<< "$version"
    local major=${version_parts[0]}
    local minor=${version_parts[1]}
    local patch=${version_parts[2]}
    
    case $increment_type in
        major)
            major=$((major + 1))
            minor=0
            patch=0
            ;;
        minor)
            minor=$((minor + 1))
            patch=0
            ;;
        patch)
            patch=$((patch + 1))
            ;;
        *)
            print_error "Invalid increment type: $increment_type"
            ;;
    esac
    
    echo "${major}.${minor}.${patch}"
}

# Parse command line arguments
if [[ $# -eq 0 ]]; then
    show_usage
fi

VERSION_INPUT=$1

# Check if we're in a git repository
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    print_error "Not inside a git repository"
fi

# Check if working directory is clean
if [[ -n $(git status --porcelain) ]]; then
    print_error "Working directory is not clean. Please commit or stash changes first."
fi

# Get current version
current_version=$(get_current_version)
print_info "Current version: $current_version"

# Determine new version
if [[ $VERSION_INPUT =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    new_version=$VERSION_INPUT
    validate_version "$new_version"
elif [[ $VERSION_INPUT =~ ^(major|minor|patch)$ ]]; then
    new_version=$(increment_version "$current_version" "$VERSION_INPUT")
else
    print_error "Invalid version specifier: $VERSION_INPUT"
fi

print_info "New version: $new_version"

# Ask for confirmation
echo ""
read -p "Create release v$new_version? (y/N) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    print_info "Release cancelled"
    exit 0
fi

# Run build and tests
print_step "Running build and tests..."
./scripts/build.sh

# Update CHANGELOG.md
print_step "Updating CHANGELOG.md..."
today=$(date +%Y-%m-%d)
sed -i "1s/^/# Changelog\n\n## [v$new_version] - $today\n\n### Added\n- Release v$new_version\n\n/" CHANGELOG.md

# Create git tag
print_step "Creating git tag v$new_version..."
git add CHANGELOG.md
git commit -m "Release v$new_version

🚀 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>" || print_warning "Nothing to commit"

git tag -a "v$new_version" -m "Release v$new_version"

# Push tag to trigger GitHub Actions
print_step "Pushing tag to GitHub..."
git push origin main || print_warning "Failed to push main branch"
git push origin "v$new_version"

echo ""
echo -e "${GREEN}✅ Release v$new_version created successfully!${NC}"
echo ""
echo "GitHub Actions will now:"
echo "  • Run tests on multiple platforms"
echo "  • Build distribution packages"
echo "  • Create GitHub release with artifacts"
echo "  • Publish to PyPI (if configured)"
echo ""
echo "Monitor the progress at:"
echo "  https://github.com/$(git config --get remote.origin.url | sed 's/.*github.com[:/]//;s/\.git$//')/actions"