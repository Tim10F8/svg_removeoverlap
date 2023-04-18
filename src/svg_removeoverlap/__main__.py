#!/usr/bin/env python3
from pathlib import Path
from typing import Union

import fire

from .remover import RemoveOverlapsSVG


def remove_overlaps(
    input_svg: Union[str, Path],
    output_svg: Union[str, Path],
    sequential: bool = False,
    keep_white: bool = False,
    cairo: bool = True,
    picofy: bool = True,
    verbose: bool = False,
) -> None:
    """
    Removes overlapping shapes in an SVG file and saves the result to a new SVG file.

    Args:
        input_svg (Union[str, Path]): Input SVG file path.
        output_svg (Union[str, Path]): Output SVG file path.
        sequential (bool, optional): If True, process shapes sequentially instead of all at once. Defaults to False.
        keep_white (bool, optional): If True, keep white shapes. Defaults to False.
        cairo (bool, optional): If True, use cairo to convert input SVG. Defaults to True.
        picofy (bool, optional): If True, use picosvg to simplify input SVG. Defaults to True.
        verbose (bool, optional): If True, display detailed logging information. Defaults to False.
    """
    remover = RemoveOverlapsSVG(
        cairo=cairo, picofy=picofy, keep_white=keep_white, verbose=verbose
    )
    remover.load_svg(Path(input_svg))
    remover.remove(sequential=sequential)
    remover.save_svg(Path(output_svg))

def cli():
    fire.core.Display = lambda lines, out: print(*lines, file=out)
    fire.Fire(remove_overlaps)

if __name__ == "__main__":
    cli()
    