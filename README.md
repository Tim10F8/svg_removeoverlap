
# svg_removeoverlap

`svg_removeoverlap` is a command-line tool and Python library designed to simplify SVG (Scalable Vector Graphics) files by merging overlapping shapes into a single, unified shape. This process effectively removes any visual overlaps, leading to cleaner and often more optimized SVG output.

## Part 1: Accessible Overview

### What the Tool Does

This tool processes SVG files to identify and eliminate areas where different shapes or paths overlap. It takes multiple vector shapes and unions them into a single path, resulting in a simplified graphic where no shapes cover each other. This is particularly useful for complex SVGs that might have been generated from various sources, converted from other formats, or edited extensively.

It can be used in two ways:
1.  As a **Command-Line Interface (CLI)** tool for quick processing of SVG files directly from your terminal.
2.  As a **Python library** that you can integrate into your own Python scripts and applications for more programmatic control over SVG processing.

### Who It's For

`svg_removeoverlap` is beneficial for:

*   **Graphic Designers:** Who need to clean up SVGs for print, web, or further editing in design software.
*   **Web Developers:** Looking to optimize SVGs for faster loading times and better rendering performance on websites.
*   **Iconographers and UI/UX Designers:** Who create or manage icon sets and need consistent, optimized vector assets.
*   **Engineers and Hobbyists:** Working with SVGs for CNC machining, laser cutting, or other applications where clean vector paths are crucial.
*   Anyone who needs to simplify complex SVGs or prepare them for specific renderers or applications that might struggle with overlapping paths or complex SVG structures.

### Why It's Useful

*   **Reduced File Size:** Merging shapes can lead to simpler path data and potentially smaller file sizes, especially for complex graphics.
*   **Cleaner Rendering:** Eliminates visual artifacts that can sometimes occur when overlapping shapes are rendered, particularly with semi-transparent fills or strokes.
*   **Improved Compatibility:** Some older or simpler SVG renderers, cutting machines, or software might handle simplified SVGs better.
*   **Easier Further Processing:** Simplified SVGs are often easier to manipulate, edit, or convert to other formats.
*   **Preparation for Specific Operations:** For tasks like creating font glyphs from SVGs or certain types of animation, non-overlapping shapes can be a prerequisite.

### How to Install It

**1. Install the Package:**

You can install `svg_removeoverlap` directly from its GitHub repository using pip:

```bash
python3 -m pip install --upgrade git+https://github.com/twardoch/svg_removeoverlap
```

**2. Install External Dependencies:**

`svg_removeoverlap` relies on external libraries (primarily for the optional CairoSVG preprocessing step). You'll need to install these system dependencies:

*   **Cairo:** A 2D graphics library.
*   **libffi:** A foreign function interface library.
*   **pkg-config:** A helper tool used to compile and link against libraries.

Here's how to install them on common operating systems:

**On macOS (using [Homebrew](https://brew.sh/)):**

```bash
brew install cairo libffi pkg-config
```

**On Windows:**

*   With [vcpkg](https://github.com/microsoft/vcpkg):
    ```bash
    vcpkg install cairo:x64-windows
    vcpkg install libffi:x64-windows
    vcpkg install pkg-config:x64-windows
    ```
*   With [Chocolatey](https://chocolatey.org/install):
    ```bash
    choco install cairo
    choco install pkgconfiglite
    ```

**On Ubuntu/Debian-based Linux:**

```bash
sudo apt-get install libcairo2-dev libffi-dev pkg-config
```

### How to Use It

#### Command-Line Interface (CLI)

The basic syntax for the CLI tool is:

```bash
svg_removeoverlap input.svg output.svg [OPTIONS]
```

**Example:**

```bash
svg_removeoverlap my_complex_graphic.svg simplified_graphic.svg
```

To see all available options and their descriptions, use the `--help` flag:

```bash
svg_removeoverlap --help
```

This will output:
```
INFO: Showing help with the command 'svg_removeoverlap -- --help'.

NAME
    svg_removeoverlap - Removes overlapping shapes in an SVG file and saves the result to a new SVG file.

SYNOPSIS
    svg_removeoverlap INPUT_SVG OUTPUT_SVG <flags>

DESCRIPTION
    Removes overlapping shapes in an SVG file and saves the result to a new SVG file.

POSITIONAL ARGUMENTS
    INPUT_SVG
        Type: Union
        Input SVG file path.
    OUTPUT_SVG
        Type: Union
        Output SVG file path.

FLAGS
    -s, --sequential=SEQUENTIAL
        Type: bool
        Default: False
        If True, process shapes sequentially instead of all at once. Defaults to False.
    -k, --keep_white=KEEP_WHITE
        Type: bool
        Default: False
        If True, keep white shapes. Defaults to False.
    -c, --cairo=CAIRO
        Type: bool
        Default: True
        If True, use cairo to convert input SVG. Defaults to True.
    -p, --picofy=PICOFY
        Type: bool
        Default: False (Note: CLI help shows True, but class default is False. The class default is more representative for library use)
        If True, use picosvg to simplify input SVG. Defaults to False.
    -v, --verbose=VERBOSE
        Type: bool
        Default: False
        If True, display detailed logging information. Defaults to False.

NOTES
    You can also use flags syntax for POSITIONAL ARGUMENTS
```

#### Programmatic Usage (Python Library)

You can integrate `svg_removeoverlap` into your Python projects. Here's a basic example:

```python
from pathlib import Path
from svg_removeoverlap.remover import RemoveOverlapsSVG, SVGProcessingError

input_path = Path("path/to/your/input.svg")
output_path = Path("path/to/your/output.svg")

# Instantiate the remover
# Key parameters for RemoveOverlapsSVG:
# - cairo (bool): If True (default), use CairoSVG to preprocess the SVG. This can help normalize
#                 the SVG for better processing by picosvg.
# - picofy (bool): If True (default is False), use picosvg's topicosvg() method to further
#                  simplify and canonicalize the SVG structure.
# - keep_white (bool): If True (default is False), shapes filled with white will also be
#                      processed. Otherwise, they are typically skipped.
# - verbose (bool): If True, enables detailed logging, including progress bars for some operations.
remover = RemoveOverlapsSVG(cairo=True, picofy=False, keep_white=False, verbose=True)

try:
    # Load the SVG file
    remover.load_svg(input_path)

    # Remove overlaps
    # - sequential (bool): If True, shapes are unioned one by one. If False (default),
    #                      all shapes are unioned in a single operation. Sequential can
    #                      sometimes be more stable for very complex SVGs but might be slower.
    remover.remove(sequential=False)

    # Save the processed SVG
    remover.save_svg(output_path)
    print(f"Processed SVG saved to {output_path}")

except FileNotFoundError:
    print(f"Error: Input file {input_path} not found.")
except SVGProcessingError as e:
    print(f"An error occurred during SVG processing: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

```

## Part 2: Technical Details

### How the Code Works (High-Level Workflow)

The `svg_removeoverlap` tool processes SVGs through the following main steps:

1.  **Load SVG File:** The input SVG file is read into memory.
2.  **Optional: Preprocess with CairoSVG (`cairo=True`):**
    *   If the `cairo` option is enabled (default), the loaded SVG content is first processed by `cairosvg`.
    *   `cairosvg.surface.SVGSurface.convert()` is used to convert the input SVG. This step helps to normalize various SVG features, resolve CSS, and convert text or complex shapes into paths, making the SVG structure more consistent and amenable to `picosvg`.
3.  **Protect `clipPath` Elements:**
    *   The SVG (potentially Cairo-processed) is parsed using `lxml`.
    *   It iterates through all `<clipPath>` elements. For any graphical child elements within a `<clipPath>` (like `<path>`, `<rect>`, etc.), their `fill` attribute is explicitly set to `transparent`.
    *   This is crucial because `clipPath` contents are masks and should not be treated as visual filled shapes during the unioning process. Without this, parts of a clip path might be merged into the main graphic.
4.  **Parse with `picosvg`:**
    *   The (potentially modified) SVG string is parsed into a `picosvg.svg.SVG` object. This object represents the SVG structure in a way that `picosvg` can manipulate.
5.  **Optional: Simplify with `picosvg.topicosvg()` (`picofy=True`):**
    *   If the `picofy` option is enabled, the `picoSVG.topicosvg()` method is called. This converts the SVG into a simpler, more canonical `picosvg` representation, which can further help in standardizing path data and structure before unioning.
6.  **Filter Shapes:**
    *   The tool iterates through all shapes (paths) within the `picosvg` object.
    *   The `fill` attribute of each shape is determined (checking both direct `fill` attributes and `style` attributes using `tinycss2`).
    *   Shapes are filtered based on their fill values. By default, shapes with common white fill values (e.g., "white", "#ffffff", "rgb(255,255,255)") and transparent fills ("none", "transparent") are skipped. This behavior can be changed with the `keep_white=True` option,_which will include white shapes in the unioning process.
7.  **Remove Overlaps using `picosvg.svg_pathops.union()`:**
    *   The core of the overlap removal is performed by `picosvg.svg_pathops.union()`. This function takes a list of path command sequences and computes their geometric union.
    *   **Sequential Mode (`sequential=True`):** If enabled, shapes are unioned iteratively. The first shape becomes the base. Then, the second shape is unioned with this base. The result of that union then becomes the new base, and the third shape is unioned with it, and so on. This can sometimes be more robust or yield different results for highly complex SVGs compared to an all-at-once union, but may be slower.
    *   **Simultaneous Mode (`sequential=False`, default):** All filtered shapes are provided to the `union()` function in a single call. This is generally faster.
8.  **Rebuild SVG:**
    *   After the union operation, the result is a single sequence of path commands representing the final merged shape.
    *   A new SVG structure is created. The original SVG's root attributes (like `viewBox`, `width`, `height`, `xmlns`) are preserved.
    *   A new `<path>` element is created within this new SVG, and its `d` attribute is set to the path data obtained from the unioned shape commands. This path is typically given a black fill by default in the rebuilt SVG by `picosvg` if not specified otherwise.
9.  **Save Resulting SVG:** The newly constructed SVG content, containing the single merged path, is written to the specified output file.

### Core Libraries and Their Roles

*   **`picosvg`**: This is the primary library for the core SVG manipulation tasks:
    *   Parsing SVG files into an internal object model (`picosvg.svg.SVG.fromstring`).
    *   Converting SVG shapes into path command sequences (`shape.as_cmd_seq()`).
    *   Performing the geometric union of paths (`picosvg.svg_pathops.union`). This relies on the `skia-pathops` library.
    *   Generating the output SVG string from its internal representation (`picosvg.SVG.tostring`).
    *   Optionally simplifying/canonicalizing SVG structure (`topicosvg()`).
*   **`lxml`**: Used for robust XML and SVG tree manipulation. Its main role here is in the `_protect_clipPaths` method to find and modify `clipPath` elements before they are processed by `picosvg`.
*   **`tinycss2`**: A lightweight CSS parser used by the `get_css_fill()` helper function to parse `style` attributes on SVG elements and extract the `fill` color value. This is important because fill colors can be defined via CSS styles rather than direct XML attributes.
*   **`cairosvg`**: An optional but often crucial preprocessing library. It can convert a wide variety of SVG features (including text, strokes, and complex structures) into a simpler set of paths that `picosvg` can more reliably process. It acts as a normalization layer.
*   **`python-fire`**: Used to quickly and easily create the command-line interface from the `remove_overlaps` function in `__main__.py`. It handles argument parsing and help message generation.
*   **`skia-pathops`** (via `picosvg`): While not a direct dependency of `svg_removeoverlap`, `picosvg` uses `skia-pathops` (Python bindings for Skia's path operations module) under the hood to perform the actual boolean operations on paths (like union).
*   **`skia-python`** (in alternative scripts): The scripts `remover_cairo_skia.py` and `remover_skia.py` exist in the repository as alternative implementations or experiments. These use the `skia-python` library directly for path operations, bypassing `picosvg` for the union step. However, the main CLI tool and `RemoveOverlapsSVG` class do **not** use these scripts or `skia-python` directly, relying instead on `picosvg`'s interface to path operations.

### Key Modules and Classes

*   **`src/svg_removeoverlap/remover.py`**: This is the heart of the library.
    *   **`RemoveOverlapsSVG` class**:
        *   `__init__(self, cairo, picofy, keep_white, skip_svg_fills, verbose)`: Initializes options. `skip_svg_fills` defines which fill colors cause a shape to be ignored (unless `keep_white` is true for white fills).
        *   `load_svg(self, input_path)`: Reads the SVG file. If `self.cairo` is true, it calls `_prep_svg_cairo()`.
        *   `_protect_clipPaths(self, svg_bytes)`: Modifies `clipPath` children to have transparent fill using `lxml`.
        *   `_prep_svg_cairo(self)`: Converts SVG content using `cairosvg.surface.SVGSurface.convert()` and then calls `_protect_clipPaths`.
        *   `_parse_svg(self)`: Parses the `self.svg_content` string into `self.pico` (a `picosvg.svg.SVG` instance).
        *   `_picofy_svg(self)`: If `self.picofy` is true, calls `self.pico.topicosvg()` to simplify the SVG structure.
        *   `_prep_pico(self)`: Calls `_parse_svg()` and then `_picofy_svg()`.
        *   `_filter_pico_shapes(self)`: Iterates through shapes in `self.pico`, checks their fill (using `get_css_fill`), and returns a list of shapes that are not skipped.
        *   `remove_overlaps_pico(self, sequential=False)`: Orchestrates the overlap removal. It calls `_prep_pico()`, then `_filter_pico_shapes()`. It then uses `picosvg.svg_pathops.union()` on the filtered shapes (either sequentially or all at once). Finally, it calls `_rebuild_svg_from_shape()` to generate the new SVG content.
        *   `_rebuild_svg_from_shape(self, unioned_shape_commands)`: Creates a new `picosvg.svg.SVG` object, adds the `unioned_shape_commands` as a new path, and updates `self.svg_content`.
        *   `remove(self, sequential=False)`: Public alias for `remove_overlaps_pico`.
        *   `save_svg(self, output_path)`: Writes `self.svg_content` to the specified output file.
    *   **`get_css_fill(style: str) -> str`**: Helper function that uses `tinycss2` to parse a CSS style string (e.g., from a `style` attribute) and return the value of the `fill` property if present.

*   **`src/svg_removeoverlap/__main__.py`**: Provides the command-line interface.
    *   **`remove_overlaps(...)` function**: This is the main function exposed to the CLI by `python-fire`. It instantiates `RemoveOverlapsSVG` with parameters derived from CLI arguments, calls its `load_svg`, `remove`, and `save_svg` methods, and includes basic error handling.
    *   **`cli()` function**: Configures and runs `fire.Fire(remove_overlaps)` to make the `remove_overlaps` function available as a CLI command.

### Error Handling

The tool implements error handling to manage potential issues during processing:
*   **`SVGProcessingError`**: A custom exception class defined in `remover.py` (though used from `__main__.py`). It's raised for errors specific to the SVG processing logic, such as failures in CairoSVG conversion, picosvg parsing, or path unioning.
*   **Standard Python Exceptions**:
    *   `FileNotFoundError`: If the input SVG file does not exist.
    *   `NotADirectoryError`: If the input path is a directory instead of a file.
    *   `ValueError`: For invalid input values or if picosvg/cairosvg raise it during parsing/conversion.
    *   Generic `Exception`: A catch-all for any other unexpected errors, with traceback logged if `verbose` is enabled.
Logging (`logging` module) is used to provide information about the processing steps and errors, especially when `verbose` mode is active. Errors are typically printed to `sys.stderr`, and the CLI tool will exit with a non-zero status code upon failure.

### Coding and Contributing Rules

This project welcomes contributions. If you're interested in contributing, please follow these guidelines, largely derived from `CONTRIBUTING.md`:

*   **Reporting Bugs & Suggesting Enhancements:**
    *   Use the GitHub Issues section of the project repository.
    *   For bugs, provide detailed steps to reproduce, expected vs. actual behavior, OS/Python versions, and if possible, a sample SVG.
    *   For enhancements, clearly describe the suggestion and its benefits.

*   **Code Contributions:**
    1.  **Fork & Clone:** Fork the repository on GitHub and clone your fork locally.
    2.  **Branch:** Create a new branch for your feature or bugfix (e.g., `feature/your-feature-name` or `bugfix/issue-123`).
    3.  **Development Environment:**
        *   Use a virtual environment (`python3 -m venv .venv`).
        *   Install dependencies: `pip install -e .[testing]`.
        *   Install pre-commit hooks: `pip install pre-commit` (if needed) and `pre-commit install`.
    4.  **Make Changes:**
        *   Write clean, readable, and well-commented code.
        *   **Code Style:** This project uses **Black** for code formatting and **Flake8** for linting. These are enforced by pre-commit hooks, so ensure they pass before committing.
        *   **Type Hints:** Type hints are encouraged for clarity and static analysis.
    5.  **Testing:**
        *   Tests are written using **pytest**.
        *   Add tests for any new functionality or bug fixes.
        *   Ensure all tests pass by running `pytest` in the project root.
    6.  **Commit & Push:** Make clear, descriptive commit messages. Push your branch to your fork.
    7.  **Pull Request (PR):** Open a Pull Request to the main `svg_removeoverlap` repository. Describe your changes and link any relevant issues.

*   **Contributors:** See `AUTHORS.md` for a list of contributors.\n\n## Development and Building\n\n### For Developers\n\nThis project uses a comprehensive build system with git-tag-based semantic versioning:\n\n**Local Development:**\n\n```bash\n# Set up development environment\npython3 -m venv venv\nsource venv/bin/activate  # On Windows: venv\\Scripts\\activate\npip install -e .[testing]\n\n# Run tests\n./scripts/test.sh\n\n# Full build with tests and packaging\n./scripts/build.sh\n```\n\n**Release Process:**\n\n```bash\n# Create a new release (automatically builds, tests, and tags)\n./scripts/release.sh patch    # 1.0.0 -> 1.0.1\n./scripts/release.sh minor    # 1.0.0 -> 1.1.0\n./scripts/release.sh major    # 1.0.0 -> 2.0.0\n./scripts/release.sh 2.1.0    # Specific version\n```\n\n**Available Scripts:**\n\n- `./scripts/build.sh` - Full build with tests, coverage, and packaging\n- `./scripts/test.sh` - Quick test run\n- `./scripts/release.sh` - Automated release with git tagging\n\n### CI/CD Pipeline\n\nThe project includes a comprehensive GitHub Actions workflow that:\n\n- **Continuous Integration:** Runs tests on Python 3.8-3.12 across Ubuntu, macOS, and Windows\n- **Code Quality:** Enforces formatting, linting, and type checking\n- **Automated Releases:** Creates releases on git tags with:\n  - PyPI package distribution\n  - Multi-platform standalone binaries\n  - GitHub releases with artifacts\n\n### Build System Features\n\n- **Semantic Versioning:** Git tag-based versioning with `setuptools_scm`\n- **Multi-platform Binaries:** PyInstaller-based standalone executables\n- **Comprehensive Testing:** Unit tests, integration tests, and coverage reporting\n- **Code Quality:** Pre-commit hooks with Black, Flake8, and mypy\n- **Documentation:** Sphinx-based documentation with automatic API docs\n\n### Testing\n\nThe test suite includes:\n\n- Unit tests for core functionality\n- Integration tests with sample SVG files\n- CLI interface tests\n- Build system and packaging tests\n- Version and semver compliance tests\n\nRun the full test suite with:\n\n```bash\n# Quick test\npython -m pytest tests/\n\n# With coverage\npython -m pytest tests/ --cov=svg_removeoverlap --cov-report=html\n\n# Using tox (tests across Python versions)\ntox\n```

## License

`svg_removeoverlap` is licensed under the Apache 2.0 License. See the [LICENSE.txt](./LICENSE.txt) file for details.
Copyright (c) 2023 Adam Twardoch.