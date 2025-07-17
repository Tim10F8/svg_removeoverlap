# Quick Start Guide - Git Tag Semver Build System

This guide helps you quickly test the new git-tag-based semantic versioning system.

## Prerequisites

- Python 3.8+ installed
- Git repository initialized
- Basic familiarity with command line

## Quick Test

1. **Clone and set up the project:**
   ```bash
   git clone <repository-url>
   cd svg_removeoverlap
   chmod +x scripts/*.sh
   ```

2. **Run basic tests:**
   ```bash
   ./scripts/test.sh
   ```

3. **Build the project:**
   ```bash
   ./scripts/build.sh
   ```

4. **Test version system:**
   ```bash
   python -m pytest tests/test_version.py -v
   python -m pytest tests/test_build_system.py -v
   ```

## Testing the Release Process

**Important:** Only do this in a test repository or branch!

1. **Create a test tag:**
   ```bash
   git tag v0.1.0
   git push origin v0.1.0
   ```

2. **Test release script (dry run):**
   ```bash
   git tag -d v0.1.0  # Remove test tag
   ./scripts/release.sh patch  # This will create v0.1.1
   ```

3. **Check the results:**
   - Look for updated `CHANGELOG.md`
   - Verify git tag was created: `git tag -l`
   - Check GitHub Actions if pushed to GitHub

## Testing GitHub Actions

1. **Push to trigger CI:**
   ```bash
   git push origin main
   ```

2. **Create a release tag:**
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

3. **Monitor GitHub Actions:**
   - Go to your repository's Actions tab
   - Watch the CI/CD Pipeline run
   - Check for binary artifacts
   - Look for GitHub release creation

## Expected Outputs

### After `./scripts/build.sh`:
- `dist/` directory with wheel and source distributions
- `htmlcov/` directory with coverage report
- All tests passing
- Type checking passing

### After `./scripts/release.sh`:
- New git tag created
- `CHANGELOG.md` updated
- GitHub Actions triggered (if pushed)

### After GitHub Actions (on tag):
- PyPI package published (if `PYPI_TOKEN` set)
- Multi-platform binaries in GitHub releases
- Coverage reports updated

## Troubleshooting

### Common Issues:

1. **Permission denied on scripts:**
   ```bash
   chmod +x scripts/*.sh
   ```

2. **Python dependencies missing:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -e .[testing]
   ```

3. **Tests failing due to missing dependencies:**
   ```bash
   pip install tox
   tox -e py311  # Or your Python version
   ```

4. **Git tag already exists:**
   ```bash
   git tag -d v1.0.0      # Delete local tag
   git push origin :v1.0.0  # Delete remote tag
   ```

## Verification Checklist

- [ ] `./scripts/test.sh` runs successfully
- [ ] `./scripts/build.sh` completes without errors
- [ ] Version tests pass: `python -m pytest tests/test_version.py -v`
- [ ] Build system tests pass: `python -m pytest tests/test_build_system.py -v`
- [ ] Release script creates proper git tags
- [ ] GitHub Actions workflow runs on tag push
- [ ] Binary artifacts are created for multiple platforms
- [ ] PyPI package is published (if configured)

## Next Steps

Once everything is working:

1. **Set up PyPI token** (for automated PyPI releases):
   - Go to GitHub repository settings
   - Add secret: `PYPI_TOKEN` with your PyPI API token

2. **Configure branch protection** (optional):
   - Require PR reviews
   - Require status checks
   - Require branches to be up to date

3. **Start using the system:**
   ```bash
   ./scripts/release.sh minor  # For your first real release
   ```

## Support

If you encounter issues:
1. Check the GitHub Actions logs
2. Review the tox configuration
3. Verify all dependencies are installed
4. Check that git repository is properly configured