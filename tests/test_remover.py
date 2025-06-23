from unittest import mock
import pytest

from svg_removeoverlap.remover import get_css_fill, SVGProcessingError, RemoveOverlapsSVG
from pathlib import Path


# Tests for get_css_fill
@pytest.mark.parametrize(
    "style_str, expected_fill",
    [
        ("fill:#ff0000;", "#ff0000"),
        ("fill: red; stroke: blue;", "red"),
        ("font-size: 12px; fill:rgb(0,255,0);", "rgb(0,255,0)"),
        ("fill: hsl(120, 100%, 50%);", "hsl(120,100%,50%)"), # Test case with space in hsl
        ("fill:none;", "none"),
        ("stroke: black;", ""), # No fill
        ("", ""), # Empty string
        ("fill: ;", ""), # Fill with no value
        ("fill: red; fill: blue;", "red"), # First one wins as per current implementation logic
        ("fill:#FF0000;", "#ff0000"), # Case insensitivity for hex
        ("fill: RGB(0,255,0);", "rgb(0,255,0)"), # Case insensitivity for rgb
        ("fill: HSL(120,100%,50%);", "hsl(120,100%,50%)"), # Case insensitivity for hsl
        # Malformed but tinycss2 might recover or ignore
        ("fill: red stroke: blue", "red"), # Missing semicolon
        ("fill : yellow", "yellow"), # Space around colon
    ],
)
def test_get_css_fill(style_str, expected_fill):
    assert get_css_fill(style_str) == expected_fill

# Placeholder for tests for RemoveOverlapsSVG class
class TestRemoveOverlapsSVG:
    def test_dummy(self): # Dummy test to make sure the class can be instantiated
        remover = RemoveOverlapsSVG(cairo=False) # Disable cairo for basic instantiation test
        assert remover is not None

    @pytest.fixture
    def remover_no_cairo(self):
        return RemoveOverlapsSVG(cairo=False, picofy=False)

    def test_load_svg_empty_path(self, remover_no_cairo):
        with pytest.raises(ValueError, match="The input path cannot be empty."):
            remover_no_cairo.load_svg(None)
        with pytest.raises(ValueError, match="The input path cannot be empty."):
            remover_no_cairo.load_svg("")

    def test_load_svg_file_not_found(self, remover_no_cairo):
        with pytest.raises(FileNotFoundError, match="The input path non_existent_file.svg does not exist."):
            remover_no_cairo.load_svg(Path("non_existent_file.svg"))

    @mock.patch("pathlib.Path.is_file", return_value=False)
    @mock.patch("pathlib.Path.exists", return_value=True)
    def test_load_svg_path_is_not_a_file(self, mock_exists, mock_is_file, remover_no_cairo):
        with pytest.raises(NotADirectoryError, match="The input path path_is_a_dir is not a file."): # Corrected error type
            remover_no_cairo.load_svg(Path("path_is_a_dir"))

    @mock.patch("builtins.open", new_callable=mock.mock_open, read_data="<svg></svg>")
    @mock.patch("pathlib.Path.is_file", return_value=True)
    @mock.patch("pathlib.Path.exists", return_value=True)
    def test_load_svg_successful(self, mock_exists, mock_is_file, mock_file_open, remover_no_cairo):
        remover_no_cairo.load_svg(Path("dummy.svg"))
        assert remover_no_cairo.svg_content == "<svg></svg>"
        mock_file_open.assert_called_once_with(Path("dummy.svg"), "r")

    # Basic test for _protect_clipPaths - more detailed tests would require actual SVG content
    def test_protect_clip_paths_simple(self, remover_no_cairo):
        svg_bytes = b'<svg><clipPath id="cp1"><path d="M0,0 L10,0 L10,10 L0,10Z" fill="red"/></clipPath></svg>'
        protected_svg_str = remover_no_cairo._protect_clipPaths(svg_bytes)
        assert 'fill="transparent"' in protected_svg_str
        assert 'fill="red"' not in protected_svg_str # Ensure original fill is replaced

    def test_protect_clip_paths_malformed_xml(self, remover_no_cairo):
        svg_bytes = b'<svg><clipPath id="cp1"><path d="M0,0 L10,0 L10,10 L0,10Z" fill="red"</clipPath></svg>' # Missing quote in fill
        with pytest.raises(SVGProcessingError, match="Invalid XML structure in SVG for clipPath processing"):
            remover_no_cairo._protect_clipPaths(svg_bytes)

    # Placeholder for _prep_svg_cairo tests (requires mocking CairoSVG)
    @mock.patch("svg_removeoverlap.remover.SVGSurface")
    def test_prep_svg_cairo_called_if_enabled(self, mock_svg_surface_class, tmp_path):
        # Mock SVGSurface.convert to avoid actual CairoSVG dependency and complex return
        mock_svg_surface_class.convert.return_value = b"<svg_cairo_output></svg_cairo_output>"

        remover_with_cairo = RemoveOverlapsSVG(cairo=True)
        # Need to set svg_content before _prep_svg_cairo is called internally by load_svg
        remover_with_cairo.svg_content = "<svg_initial></svg_initial>"

        # Create a dummy file to load
        dummy_svg_path = tmp_path / "dummy_cairo.svg"
        dummy_svg_path.write_text("<svg_initial></svg_initial>")

        remover_with_cairo.load_svg(dummy_svg_path) # This will call _prep_svg_cairo

        mock_svg_surface_class.convert.assert_called_once()
        # Check that svg_content was modified by the mocked _protect_clipPaths (called by _prep_svg_cairo)
        # This is an indirect check that _prep_svg_cairo's flow was entered
        assert remover_with_cairo.svg_content != "<svg_initial></svg_initial>"
        assert "<svg_cairo_output>" in remover_with_cairo.svg_content # More direct check after _protect_clipPaths

    @mock.patch("svg_removeoverlap.remover.SVGSurface")
    def test_prep_svg_cairo_handles_conversion_error(self, mock_svg_surface_class):
        mock_svg_surface_class.convert.side_effect = ValueError("Cairo conversion failed")

        remover = RemoveOverlapsSVG(cairo=True)
        remover.svg_content = "<svg></svg>" # Set content to trigger conversion
        with pytest.raises(SVGProcessingError, match="CairoSVG failed to convert SVG"):
            remover._prep_svg_cairo() # Call directly for this test

    # More tests will be added here for:
    # - _parse_svg, _picofy_svg, _prep_pico (mocking picosvg)
    @mock.patch("svg_removeoverlap.remover.picosvg.svg.SVG")
    def test_parse_svg_successful(self, mock_picosvg_svg_class, remover_no_cairo):
        mock_svg_instance = mock.MagicMock()
        mock_picosvg_svg_class.fromstring.return_value = mock_svg_instance
        remover_no_cairo.svg_content = "<svg></svg>"

        remover_no_cairo._parse_svg()

        mock_picosvg_svg_class.fromstring.assert_called_once_with("<svg></svg>")
        assert remover_no_cairo.pico == mock_svg_instance

    @mock.patch("svg_removeoverlap.remover.picosvg.svg.SVG")
    def test_parse_svg_handles_parse_error(self, mock_picosvg_svg_class, remover_no_cairo):
        # Need to import picosvg.svg directly here to reference SVGParseError for the side_effect
        from picosvg.svg import SVGParseError
        mock_picosvg_svg_class.fromstring.side_effect = SVGParseError("Picosvg parsing failed")
        remover_no_cairo.svg_content = "<svg_malformed></svg_malformed>"

        with pytest.raises(SVGProcessingError, match="Picosvg failed to parse SVG content"):
            remover_no_cairo._parse_svg()

    @mock.patch("svg_removeoverlap.remover.picosvg.svg.SVG") # Mock the class used by _parse_svg
    def test_picofy_svg_when_enabled(self, mock_picosvg_svg_class_for_parse, remover_no_cairo):
        # Setup for _parse_svg to run without error
        mock_parsed_svg_instance = mock.MagicMock()
        mock_picofied_svg_instance = mock.MagicMock()
        mock_parsed_svg_instance.topicosvg.return_value = mock_picofied_svg_instance
        mock_picofied_svg_instance.tostring.return_value = "<picofied_svg/>"
        mock_picosvg_svg_class_for_parse.fromstring.return_value = mock_parsed_svg_instance

        remover_no_cairo.svg_content = "<svg_content_for_picofy>"
        remover_no_cairo.picofy = True # Enable picofy

        remover_no_cairo._prep_pico() # This calls _parse_svg then _picofy_svg

        mock_parsed_svg_instance.topicosvg.assert_called_once()
        mock_picofied_svg_instance.tostring.assert_called_once_with(pretty_print=False)
        assert remover_no_cairo.pico == mock_picofied_svg_instance
        assert remover_no_cairo.svg_content == "<picofied_svg/>"

    @mock.patch("svg_removeoverlap.remover.picosvg.svg.SVG")
    def test_picofy_svg_handles_error(self, mock_picosvg_svg_class_for_parse, remover_no_cairo):
        mock_parsed_svg_instance = mock.MagicMock()
        mock_parsed_svg_instance.topicosvg.side_effect = Exception("Picofy failed")
        mock_picosvg_svg_class_for_parse.fromstring.return_value = mock_parsed_svg_instance

        remover_no_cairo.svg_content = "<svg_content_for_picofy>"
        remover_no_cairo.picofy = True

        with pytest.raises(SVGProcessingError, match="Failed during picosvg simplification"):
            remover_no_cairo._prep_pico()

    def test_prep_pico_calls_parse_and_picofy(self, remover_no_cairo):
        remover_no_cairo.svg_content = "<svg></svg>"
        remover_no_cairo.picofy = True # Ensure _picofy_svg is also called

        with mock.patch.object(remover_no_cairo, '_parse_svg') as mock_parse, \
             mock.patch.object(remover_no_cairo, '_picofy_svg') as mock_picofy:

            remover_no_cairo._prep_pico()

            mock_parse.assert_called_once()
            mock_picofy.assert_called_once()

    def test_filter_pico_shapes(self, remover_no_cairo):
        # Mock shapes
        shape1 = mock.MagicMock(style="fill:red;", fill="") # Red
        shape2 = mock.MagicMock(style="fill:white;", fill="") # White
        shape3 = mock.MagicMock(style="", fill="blue") # Blue
        shape4 = mock.MagicMock(style="fill:#FFFFFF;", fill="") # White (hex)
        shape5 = mock.MagicMock(style="fill:transparent;", fill="") # Transparent
        shape6 = mock.MagicMock(style="fill:none", fill="") # None
        shape7 = mock.MagicMock(style="fill:rgb(0,0,0)", fill="") # Black

        all_shapes = [shape1, shape2, shape3, shape4, shape5, shape6, shape7]

        # Mock remover.pico.shapes()
        remover_no_cairo.pico = mock.MagicMock()
        remover_no_cairo.pico.shapes.return_value = all_shapes

        # Test 1: keep_white = False (default)
        remover_no_cairo.keep_white = False
        # Default skip_svg_fills includes "white", "#ffffff", "transparent", "none", etc.
        filtered_shapes = remover_no_cairo._filter_pico_shapes()
        assert shape1 in filtered_shapes # red
        assert shape2 not in filtered_shapes # white
        assert shape3 in filtered_shapes # blue
        assert shape4 not in filtered_shapes # #FFFFFF
        assert shape5 not in filtered_shapes # transparent
        assert shape6 not in filtered_shapes # none
        assert shape7 in filtered_shapes # black
        assert len(filtered_shapes) == 3

        # Test 2: keep_white = True
        remover_no_cairo.keep_white = True
        filtered_shapes_keep_white = remover_no_cairo._filter_pico_shapes()
        # Should keep white, but still skip "transparent" and "none" based on default skip_svg_fills
        assert shape1 in filtered_shapes_keep_white
        assert shape2 in filtered_shapes_keep_white # white is kept
        assert shape3 in filtered_shapes_keep_white
        assert shape4 in filtered_shapes_keep_white # #FFFFFF is kept
        assert shape5 not in filtered_shapes_keep_white # transparent is still skipped
        assert shape6 not in filtered_shapes_keep_white # none is still skipped
        assert shape7 in filtered_shapes_keep_white
        assert len(filtered_shapes_keep_white) == 5

        # Test 3: Custom skip_svg_fills
        remover_no_cairo.keep_white = False # Reset
        remover_no_cairo.skip_svg_fills = ["red", "blue"] # Custom skip
        filtered_shapes_custom_skip = remover_no_cairo._filter_pico_shapes()
        assert shape1 not in filtered_shapes_custom_skip # red is skipped
        assert shape2 in filtered_shapes_custom_skip # white is kept (not in custom skip)
        assert shape3 not in filtered_shapes_custom_skip # blue is skipped
        assert shape4 in filtered_shapes_custom_skip # #FFFFFF is kept
        assert shape5 in filtered_shapes_custom_skip # transparent is kept
        assert shape6 in filtered_shapes_custom_skip # none is kept
        assert shape7 in filtered_shapes_custom_skip # black is kept
        assert len(filtered_shapes_custom_skip) == 5

    @mock.patch("svg_removeoverlap.remover.picosvg.svg_pathops.union")
    @mock.patch("svg_removeoverlap.remover.picosvg.svg.SVGPath")
    @mock.patch("svg_removeoverlap.remover.etree") # To mock etree.Element and SubElement
    def test_remove_overlaps_pico_non_sequential(self, mock_etree, mock_svgpath_class, mock_union, remover_no_cairo):
        # Setup remover instance
        remover_no_cairo.svg_content = "<svg viewBox='0 0 100 100'><path d='dummy'/></svg>" # Needs some content to parse

        # Mock _prep_pico to set up a mock pico object
        mock_pico_instance = mock.MagicMock()
        mock_pico_instance.svg_root.attrib = {'viewBox': '0 0 100 100', 'xmlns': 'http://www.w3.org/2000/svg'}
        mock_pico_instance.view_box = (0, 0, 100, 100)

        # Mock _filter_pico_shapes to return some mock shapes
        shape1 = mock.MagicMock(name="shape1")
        shape2 = mock.MagicMock(name="shape2")
        mock_filtered_shapes = [shape1, shape2]

        with mock.patch.object(remover_no_cairo, '_prep_pico', autospec=True) as mock_prep_pico_method, \
             mock.patch.object(remover_no_cairo, '_filter_pico_shapes', return_value=mock_filtered_shapes) as mock_filter_shapes_method:
            # Ensure self.pico is set by the mocked _prep_pico
            def side_effect_prep_pico():
                remover_no_cairo.pico = mock_pico_instance
            mock_prep_pico_method.side_effect = side_effect_prep_pico

            # Mock return value of picosvg.svg_pathops.union
            mock_unioned_shape_commands = [('M', (0,0))] # Dummy commands
            mock_union.return_value = mock_unioned_shape_commands

            # Mock SVGPath.from_commands().d
            mock_svgpath_instance = mock.MagicMock()
            mock_svgpath_instance.d = "M0,0 Z" # Dummy d string
            mock_svgpath_class.from_commands.return_value = mock_svgpath_instance

            # Mock etree Elements
            mock_new_root_element = mock.MagicMock(name="new_root_svg_element")
            mock_etree.Element.return_value = mock_new_root_element
            mock_path_el = mock.MagicMock(name="new_path_element")
            mock_etree.SubElement.return_value = mock_path_el

            # Mock the SVG class constructor used for new_svg
            with mock.patch("svg_removeoverlap.remover.picosvg.svg.SVG") as mock_final_svg_constructor:
                mock_final_svg_instance = mock.MagicMock(name="final_svg_object")
                mock_final_svg_instance.tostring.return_value = "<svg_final_output/>"
                mock_final_svg_constructor.return_value = mock_final_svg_instance

                # Call the method under test
                remover_no_cairo.remove_overlaps_pico(sequential=False)

                mock_prep_pico_method.assert_called_once()
                mock_filter_shapes_method.assert_called_once()

                # Check union call
                mock_union.assert_called_once_with(mock_filtered_shapes, ["nonzero", "nonzero"])
                mock_svgpath_class.from_commands.assert_called_once_with(mock_unioned_shape_commands)

                # Check etree usage
                mock_etree.Element.assert_called_once_with("svg")
                assert mock_new_root_element.set.call_count == 2 # viewBox, xmlns
                mock_new_root_element.set.assert_any_call('viewBox', '0 0 100 100')
                mock_new_root_element.set.assert_any_call('xmlns', 'http://www.w3.org/2000/svg')

                mock_etree.SubElement.assert_called_once_with(mock_new_root_element, "path")
                mock_path_el.set.assert_called_once_with("d", "M0,0 Z")

                # Check final SVG object creation and output
                mock_final_svg_constructor.assert_called_once_with(mock_new_root_element)
                assert mock_final_svg_instance.view_box == (0,0,100,100)
                assert remover_no_cairo.svg_content == "<svg_final_output/>"
                assert remover_no_cairo.pico == mock_final_svg_instance

    # TODO: Add test for sequential=True mode in remove_overlaps_pico
    # This will involve similar mocking but checking that union is called multiple times in a loop.

    # - Different options (sequential, keep_white) are partially covered by _filter_pico_shapes
    #   and can be further tested via integration tests.
    pass
