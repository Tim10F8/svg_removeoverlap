
# svg_removeoverlap

CLI tool & Python lib to remove overlap in SVG. 

This Python script is designed to remove overlapping shapes in an SVG (Scalable Vector Graphics) file using the picosvg library. It provides several options to control the removal process, such as using CairoSVG for SVG conversion, converting SVG to picosvg, keeping white fill shapes, and skipping specific fill values.

## Installation

```bash
python3 -m pip install --upgrade git+https://github.com/twardoch/svg_removeoverlap
```

You also need to install external dependencies. 

### On macOS

With [Homebrew](https://brew.sh/)

```bash
brew install cairo libffi pkg-config
```

### On Windows 

With [vcpkg](https://github.com/microsoft/vcpkg):

```
vcpkg install cairo:x64-windows
vcpkg install libffi:x64-windows
vcpkg install pkg-config:x64-windows
```

With [Chocolatey](https://chocolatey.org/install):

```
choco install cairo
choco install pkgconfiglite
```

### On Ubuntu

```bash
sudo apt-get install libcairo2-dev libffi-dev pkg-config
```


## Usage in CLI

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

## Usage in Python

```python
from svg_removeoverlap.remover import RemoveOverlapsSVG
remover = RemoveOverlapsSVG(cairo=True, picofy=False, keep_white=False, verbose=True)
remover.load_svg(input_path)
remover.remove(sequential=False)
remover.save_svg(output_path)
```

## License

- Copyright (c) 2023 Adam Twardoch
- Licensed under the [Apache 2.0](./LICENSE.txt) license.