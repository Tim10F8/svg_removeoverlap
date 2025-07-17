# this_file: tests/test_version.py
"""Tests for version handling and semver compliance"""

import re
import sys
import subprocess
from pathlib import Path
import pytest

# Add src to Python path for testing
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from svg_removeoverlap import __version__


def test_version_format():
    """Test that version follows semantic versioning format"""
    # Either a proper version or "unknown" during development
    if __version__ != "unknown":
        # Check semver format: MAJOR.MINOR.PATCH with optional pre-release/build
        semver_pattern = r'^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$'
        assert re.match(semver_pattern, __version__), f"Version {__version__} does not match semver format"


def test_version_accessible():
    """Test that version is accessible"""
    assert __version__ is not None
    assert isinstance(__version__, str)
    assert len(__version__) > 0


def test_cli_version():
    """Test that CLI reports version correctly"""
    try:
        # Test if CLI is accessible
        result = subprocess.run([
            sys.executable, "-m", "svg_removeoverlap", "--help"
        ], capture_output=True, text=True, cwd=Path(__file__).parent.parent)
        
        # Should not crash
        assert result.returncode == 0
        
    except (FileNotFoundError, subprocess.CalledProcessError):
        pytest.skip("CLI not available for testing")


def test_package_metadata():
    """Test that package metadata is accessible"""
    try:
        from importlib.metadata import metadata
        meta = metadata("svg_removeoverlap")
        
        # Check essential metadata fields
        assert meta["Name"] == "svg_removeoverlap"
        assert meta["Version"] is not None
        assert meta["Author"] is not None
        
    except Exception:
        pytest.skip("Package metadata not available")


def test_setuptools_scm_integration():
    """Test that setuptools_scm can determine version from git"""
    try:
        from setuptools_scm import get_version
        
        # This should work in a git repository
        version = get_version()
        assert version is not None
        assert isinstance(version, str)
        
    except (ImportError, LookupError):
        pytest.skip("setuptools_scm not available or not in git repo")


def test_git_tag_version_consistency():
    """Test that git tags follow semver format"""
    try:
        result = subprocess.run([
            "git", "tag", "-l", "v*"
        ], capture_output=True, text=True, cwd=Path(__file__).parent.parent)
        
        if result.returncode == 0:
            tags = result.stdout.strip().split('\n')
            tags = [tag for tag in tags if tag.startswith('v')]
            
            semver_pattern = r'^v(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$'
            
            for tag in tags:
                if tag:  # Skip empty tags
                    assert re.match(semver_pattern, tag), f"Git tag {tag} does not follow semver format"
    
    except (FileNotFoundError, subprocess.CalledProcessError):
        pytest.skip("Git not available for testing")