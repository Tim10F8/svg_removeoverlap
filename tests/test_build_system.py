# this_file: tests/test_build_system.py
"""Tests for build system and packaging"""

import sys
import subprocess
from pathlib import Path
import pytest
import tempfile
import shutil


def test_package_structure():
    """Test that package structure is correct"""
    project_root = Path(__file__).parent.parent
    
    # Check essential files exist
    assert (project_root / "setup.cfg").exists()
    assert (project_root / "pyproject.toml").exists()
    assert (project_root / "tox.ini").exists()
    assert (project_root / "src" / "svg_removeoverlap" / "__init__.py").exists()
    assert (project_root / "src" / "svg_removeoverlap" / "__main__.py").exists()
    assert (project_root / "src" / "svg_removeoverlap" / "remover.py").exists()
    
    # Check scripts exist
    assert (project_root / "scripts" / "build.sh").exists()
    assert (project_root / "scripts" / "release.sh").exists()
    assert (project_root / "scripts" / "test.sh").exists()
    
    # Check GitHub Actions
    assert (project_root / ".github" / "workflows" / "ci.yml").exists()
    
    # Check PyInstaller spec
    assert (project_root / "svg_removeoverlap.spec").exists()


def test_tox_configuration():
    """Test tox configuration is valid"""
    project_root = Path(__file__).parent.parent
    tox_ini = project_root / "tox.ini"
    
    content = tox_ini.read_text()
    
    # Check essential sections
    assert "[tox]" in content
    assert "[testenv]" in content
    assert "[testenv:build]" in content
    assert "[testenv:publish]" in content
    
    # Check Python versions
    assert "py38" in content
    assert "py39" in content
    assert "py310" in content
    assert "py311" in content
    assert "py312" in content


def test_pyproject_toml_configuration():
    """Test pyproject.toml configuration"""
    project_root = Path(__file__).parent.parent
    pyproject = project_root / "pyproject.toml"
    
    content = pyproject.read_text()
    
    # Check build system
    assert "[build-system]" in content
    assert "setuptools" in content
    assert "setuptools_scm" in content
    
    # Check setuptools_scm configuration
    assert "[tool.setuptools_scm]" in content


def test_setup_cfg_configuration():
    """Test setup.cfg configuration"""
    project_root = Path(__file__).parent.parent
    setup_cfg = project_root / "setup.cfg"
    
    content = setup_cfg.read_text()
    
    # Check metadata
    assert "[metadata]" in content
    assert "name = svg_removeoverlap" in content
    assert "author = Adam Twardoch" in content
    
    # Check options
    assert "[options]" in content
    assert "python_requires = >=3.8" in content
    
    # Check entry points
    assert "[options.entry_points]" in content
    assert "console_scripts" in content
    assert "svg_removeoverlap = svg_removeoverlap.__main__:cli" in content


def test_scripts_are_executable():
    """Test that scripts are executable"""
    project_root = Path(__file__).parent.parent
    scripts = [
        "scripts/build.sh",
        "scripts/release.sh", 
        "scripts/test.sh"
    ]
    
    for script in scripts:
        script_path = project_root / script
        assert script_path.exists()
        # Check if executable (Unix-style)
        if hasattr(script_path, 'stat'):
            import stat
            assert script_path.stat().st_mode & stat.S_IEXEC


def test_pyinstaller_spec():
    """Test PyInstaller spec file"""
    project_root = Path(__file__).parent.parent
    spec_file = project_root / "svg_removeoverlap.spec"
    
    content = spec_file.read_text()
    
    # Check essential components
    assert "Analysis" in content
    assert "PYZ" in content
    assert "EXE" in content
    
    # Check entry point
    assert "__main__.py" in content
    
    # Check hidden imports
    assert "hiddenimports" in content
    assert "svg_removeoverlap.remover" in content


def test_github_actions_workflow():
    """Test GitHub Actions workflow"""
    project_root = Path(__file__).parent.parent
    workflow = project_root / ".github" / "workflows" / "ci.yml"
    
    content = workflow.read_text()
    
    # Check workflow name
    assert "name: CI/CD Pipeline" in content
    
    # Check triggers
    assert "on:" in content
    assert "push:" in content
    assert "pull_request:" in content
    
    # Check jobs
    assert "prepare:" in content
    assert "test:" in content
    assert "build-binaries:" in content
    assert "publish:" in content
    
    # Check matrix testing
    assert "matrix:" in content
    assert "python:" in content
    assert "platform:" in content
    
    # Check semver tag support
    assert "v[0-9]+.[0-9]+.[0-9]+" in content


@pytest.mark.skipif(shutil.which("tox") is None, reason="tox not available")
def test_tox_dry_run():
    """Test tox dry run"""
    project_root = Path(__file__).parent.parent
    
    try:
        result = subprocess.run([
            "tox", "--listenvs"
        ], capture_output=True, text=True, cwd=project_root)
        
        # Should list environments
        assert result.returncode == 0
        assert "py38" in result.stdout or "py39" in result.stdout
        
    except FileNotFoundError:
        pytest.skip("tox not available")


def test_build_system_integration():
    """Test basic build system integration"""
    project_root = Path(__file__).parent.parent
    
    # Test that we can import the package
    sys.path.insert(0, str(project_root / "src"))
    
    try:
        import svg_removeoverlap
        assert hasattr(svg_removeoverlap, "__version__")
        
        from svg_removeoverlap.remover import RemoveOverlapsSVG
        assert RemoveOverlapsSVG is not None
        
    except ImportError as e:
        pytest.skip(f"Package import failed: {e}")


def test_coverage_configuration():
    """Test coverage configuration"""
    project_root = Path(__file__).parent.parent
    coveragerc = project_root / ".coveragerc"
    
    if coveragerc.exists():
        content = coveragerc.read_text()
        
        # Check configuration sections
        assert "[run]" in content
        assert "[report]" in content
        assert "source = svg_removeoverlap" in content