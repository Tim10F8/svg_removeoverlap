
# svg_removeoverlap

CLI tool & Python lib to remove overlap in SVG

## Installation

```bash
python3 -m pip install --upgrade git+https://github.com/twardoch/svg_removeoverlap
```

You also need to install external dependencies. On macOS: 

```bash
brew install cairo skia
```

## Usage

```bash
svg_removeoverlap input.svg output.svg
```

```
$ svg_removeoverlap --help
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
        Default: False
        If True, use picosvg to simplify input SVG. Defaults to False.
    -v, --verbose=VERBOSE
        Type: bool
        Default: False
        If True, display detailed logging information. Defaults to False.

NOTES
    You can also use flags syntax for POSITIONAL ARGUMENTS
```

## Description

This tool is a Python module for removing overlaps from SVG files. The module consists of several Python files, namely `__init__.py`, `__main__.py`, and `remover.py`.

The `__init__.py` file imports necessary libraries and defines the package name and version. The `__main__.py` file is the entry point of the tool, and it defines a function `remove_overlaps` that takes input SVG and outputs a new SVG file with overlaps removed. The `remover.py` file contains the core functionality of the tool, which includes loading and parsing SVG files, filtering shapes, and removing overlaps.

To use this tool, you need to have Python 3.8 or later installed on your system. Then you can install the package using pip and run the `remove_overlaps` function from the command line. You need to specify the input SVG file path and output SVG file path as arguments to the function. You can also provide additional optional arguments, such as `sequential`, `keep_white`, `cairo`, `picofy`, and `verbose`, to modify the behavior of the tool.

## License

- Copyright (c) 2023 Adam Twardoch
- Licensed under the [Apache 2.0](./LICENSE.txt) license.