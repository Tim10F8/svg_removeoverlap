import pytest
from pathlib import Path
from lxml import etree # For parsing output XML

from svg_removeoverlap.remover import RemoveOverlapsSVG

FIXTURE_DIR = Path(__file__).parent / "fixtures"

@pytest.mark.parametrize(
    "input_svg_name, keep_white_setting, cairo_setting, picofy_setting",
    [
        ("simple_overlap.svg", False, False, False),
        ("no_overlap.svg", False, False, False),
        ("with_white.svg", False, False, False), # white should be removed
        ("with_white.svg", True, False, False),  # white should be kept
        # TODO: Could add cases for cairo=True if cairo is reliably available in test env
        # ("simple_overlap.svg", False, True, False),
    ]
)
def test_svg_processing_integration(tmp_path, input_svg_name, keep_white_setting, cairo_setting, picofy_setting):
    input_svg_path = FIXTURE_DIR / input_svg_name
    output_svg_path = tmp_path / f"output_{input_svg_name}"

    remover = RemoveOverlapsSVG(
        cairo=cairo_setting,
        picofy=picofy_setting,
        keep_white=keep_white_setting,
        verbose=True # Enable verbose for more log output during tests if needed
    )

    remover.load_svg(input_svg_path)
    # The remove() method calls remove_overlaps_pico() internally
    remover.remove(sequential=False) # Test with non-sequential for now
    remover.save_svg(output_svg_path)

    assert output_svg_path.exists()
    assert output_svg_path.stat().st_size > 0 # Check file is not empty

    # Try to parse the output SVG to ensure it's valid XML and has an <svg> root
    try:
        output_tree = etree.parse(str(output_svg_path))
        output_root = output_tree.getroot()
        assert output_root.tag == "{http://www.w3.org/2000/svg}svg", "Output is not a valid SVG file"
    except etree.XMLSyntaxError as e:
        pytest.fail(f"Output SVG file is not well-formed XML: {e}\nContent:\n{output_svg_path.read_text()}")

    # Specific assertions based on input and settings
    # These are examples and might need refinement
    output_content = output_svg_path.read_text().lower()
    if input_svg_name == "simple_overlap.svg":
        # After union, there should ideally be a single path if all shapes are combined.
        # This depends heavily on picosvg's output.
        # A simpler check might be that "red" and "blue" fills are gone if not preserved by some logic.
        # For now, we mainly check it produces a valid SVG.
        pass
    elif input_svg_name == "with_white.svg":
        if keep_white_setting:
            assert 'fill="white"' in output_content or 'fill="#ffffff"' in output_content # Check white is present
        else:
            assert 'fill="white"' not in output_content and 'fill="#ffffff"' not in output_content # Check white is absent

    # More specific assertions could be:
    # - Counting number of <path> elements (e.g., expect 1 after union of overlapping shapes)
    # - Checking for the absence/presence of certain fill colors in the final output.
    # - Verifying viewbox consistency.
    # These would require more knowledge of the expected output from picosvg.

def test_svg_processing_integration_sequential(tmp_path):
    input_svg_path = FIXTURE_DIR / "simple_overlap.svg"
    output_svg_path = tmp_path / "output_simple_overlap_sequential.svg"

    remover = RemoveOverlapsSVG(
        cairo=False, # Keep cairo off for predictability unless testing cairo specifically
        picofy=False,
        keep_white=False,
        verbose=True
    )
    remover.load_svg(input_svg_path)
    remover.remove(sequential=True) # Test with sequential=True
    remover.save_svg(output_svg_path)

    assert output_svg_path.exists()
    assert output_svg_path.stat().st_size > 0
    try:
        output_tree = etree.parse(str(output_svg_path))
        output_root = output_tree.getroot()
        assert output_root.tag == "{http://www.w3.org/2000/svg}svg"
    except etree.XMLSyntaxError as e:
        pytest.fail(f"Output SVG (sequential) is not well-formed XML: {e}")

def test_svg_processing_integration_malformed_svg_error(tmp_path):
    input_svg_path = FIXTURE_DIR / "malformed.svg" # The malformed SVG fixture

    remover = RemoveOverlapsSVG(cairo=False, picofy=False, verbose=True)

    with pytest.raises(Exception) as excinfo: # Catch a broad exception, could be SVGProcessingError or picosvg error
        # The exact point of failure could be load_svg (if parsing is immediate) or remove
        remover.load_svg(input_svg_path) # picosvg parsing happens in _prep_pico called by remove, or _parse_svg
        remover.remove()                 # or directly if cairo/picofy are false.

    # Check if the exception is one of the expected types from picosvg or our wrapper
    from svg_removeoverlap.remover import SVGProcessingError
    from picosvg.svg import SVGParseError # Assuming picosvg.svg.SVGParseError is the one

    assert isinstance(excinfo.value, (SVGProcessingError, SVGParseError, ValueError)), \
        f"Expected SVGProcessingError or picosvg.svg.SVGParseError, got {type(excinfo.value)}"

    # Check that the error message indicates a parsing or path construction problem
    error_message = str(excinfo.value).lower()
    assert "picosvg failed to parse" in error_message or \
           "failed to construct path data" in error_message or \
           "error converting new shape commands" in error_message or \
           "invalid pathdata" in error_message # More generic for path issues

# TODO: Add integration tests for error conditions (e.g., malformed input SVG that passes initial load but fails in picosvg).
#       This might require creating specific malformed SVG fixture files. (Partially done)
#       Example: an SVG that is XML-valid but has problematic path data for picosvg.
# remover.remove(sequential=True)
# assert ...
