import pytest
from pathlib import Path
import subprocess
from lxml import etree # For parsing output XML

FIXTURE_DIR = Path(__file__).parent / "fixtures"
MAIN_SCRIPT = ["svg_removeoverlap"] # Assuming it's installed and in PATH or using entry point

def run_cli(args):
    """Helper function to run the CLI command and return result."""
    return subprocess.run(MAIN_SCRIPT + args, capture_output=True, text=True)

def test_cli_help():
    result = run_cli(["--help"])
    assert result.returncode == 0
    assert "svg_removeoverlap" in result.stdout
    assert "INPUT_SVG" in result.stdout
    assert "OUTPUT_SVG" in result.stdout

def test_cli_basic_processing(tmp_path):
    input_svg = FIXTURE_DIR / "simple_overlap.svg"
    output_svg = tmp_path / "cli_output.svg"

    result = run_cli([str(input_svg), str(output_svg)])

    assert result.returncode == 0, f"CLI Error: {result.stderr}"
    assert output_svg.exists()
    assert output_svg.stat().st_size > 0

    try:
        output_tree = etree.parse(str(output_svg))
        output_root = output_tree.getroot()
        assert output_root.tag == "{http://www.w3.org/2000/svg}svg"
    except etree.XMLSyntaxError as e:
        pytest.fail(f"CLI Output SVG is not well-formed XML: {e}\nContent:\n{output_svg.read_text()}")

def test_cli_keep_white(tmp_path):
    input_svg = FIXTURE_DIR / "with_white.svg"
    output_svg = tmp_path / "cli_output_white.svg"

    # Test without keep_white (default: white removed)
    result_no_keep = run_cli([str(input_svg), str(output_svg)])
    assert result_no_keep.returncode == 0, f"CLI Error (no keep_white): {result_no_keep.stderr}"
    assert output_svg.exists()
    content_no_keep = output_svg.read_text().lower()
    assert 'fill="white"' not in content_no_keep and 'fill="#ffffff"' not in content_no_keep

    # Test with keep_white
    output_svg_kept = tmp_path / "cli_output_white_kept.svg"
    result_keep = run_cli([str(input_svg), str(output_svg_kept), "--keep_white"]) # or -k
    assert result_keep.returncode == 0, f"CLI Error (keep_white): {result_keep.stderr}"
    assert output_svg_kept.exists()
    content_kept = output_svg_kept.read_text().lower()
    assert 'fill="white"' in content_kept or 'fill="#ffffff"' in content_kept

def test_cli_verbose_option(tmp_path):
    input_svg = FIXTURE_DIR / "no_overlap.svg"
    output_svg = tmp_path / "cli_output_verbose.svg"

    result = run_cli([str(input_svg), str(output_svg), "--verbose"]) # or -v
    assert result.returncode == 0, f"CLI Error: {result.stderr}"
    assert output_svg.exists()
    # Verbose should produce INFO level logs, which go to stdout for Fire by default
    # if logging is configured as in __main__.py to print to console.
    # The default fire.core.Display prints to stdout.
    # Our __main__ configures logging to print to console.
    assert "INFO: Reading" in result.stdout or "INFO: Saving" in result.stdout # Check for logger output

def test_cli_input_file_not_found(tmp_path):
    non_existent_input = "does_not_exist.svg"
    output_svg = tmp_path / "output.svg"
    result = run_cli([non_existent_input, str(output_svg)])
    assert result.returncode != 0 # Expect an error
    # Fire usually prints the traceback to stderr
    assert "FileNotFoundError" in result.stderr

# TODO: Add CLI test for --sequential option
# TODO: Add CLI test for --cairo and --picofy if reliable way to test their effects via CLI
#       (e.g. if they change output structure significantly or handle specific SVGs differently)
# TODO: Add CLI tests for more complex error conditions if possible from CLI
#       (e.g., providing a malformed SVG that causes SVGProcessingError)
#       This would check if the error is reported reasonably on stderr.
