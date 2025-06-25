# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased] - YYYY-MM-DD

### Added
- Created `PLAN.md` to outline project enhancement strategy.
- Created `TODO.md` to track specific tasks for project improvement and updated it progressively.
- Created root `CHANGELOG.md` and `CONTRIBUTING.md`.
- `lxml-stubs` as a testing dependency for improved type checking.
- `codespell` pre-commit hook to check for typos.
- New test fixtures: `malformed.svg`, `complex_clippath.svg`, `empty_shapes.svg`.
- Unit tests for `_rebuild_svg_from_shape` method in `remover.py`.
- Unit tests for `remove_overlaps_pico` sequential mode and for cases with no shapes after filtering.
- Unit tests for `_protect_clipPaths` with complex SVG structures.
- Unit tests for `get_css_fill` with malformed CSS.
- CLI tests for `--sequential` option and for error reporting with malformed SVGs.
- Integration tests for sequential mode and error handling with malformed SVGs.

### Changed
- **Core Logic (`src/svg_removeoverlap/remover.py`):**
    - Refactored `remove_overlaps_pico`: extracted SVG reconstruction to `_rebuild_svg_from_shape`.
    - Enhanced `_protect_clipPaths` to correctly handle various graphical elements within a `<clipPath>`.
    - Made `skip_svg_fills` matching case-insensitive.
    - Improved error handling in `get_css_fill` for `tinycss2.ast.ParseError`.
    - `remove_overlaps_pico` now correctly handles cases where no shapes remain after filtering.
- **CLI (`src/svg_removeoverlap/__main__.py`):**
    - Implemented robust error handling: catches specific exceptions, prints user-friendly messages to `stderr`, and exits with status 1.
    - Added a success message upon completion.
- **Build & QA:**
    - Updated `setup.cfg`: added `Changelog` URL to `project_urls`.
    - Updated `.pre-commit-config.yaml`: enabled `codespell` and configured `mypy` with `lxml-stubs`.
- **Tests:**
    - Updated existing unit tests for `remove_overlaps_pico` to align with refactoring.
    - Improved detail in some CLI and integration test assertions.

### Fixed
- Redundant `lxml.etree` import in `src/svg_removeoverlap/remover.py`.
- Potential `KeyError` if `xmlns` was not in original SVG root attributes during rebuild (now explicitly sets `xmlns`).
- `test_cli_input_file_not_found` to expect custom error message instead of full traceback.

### Removed
- N/A
