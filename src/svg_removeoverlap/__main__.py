#!/usr/bin/env python3
import logging
import sys # For sys.exit and sys.stderr
from pathlib import Path

import fire

from .remover import RemoveOverlapsSVG, SVGProcessingError


def remove_overlaps(
    input_svg: str | Path,
    output_svg: str | Path,
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
    if verbose:
        logging.basicConfig(
            level=logging.INFO, format="%(levelname)s: %(message)s"
        )
    else:
        logging.basicConfig(
            level=logging.WARNING, format="%(levelname)s: %(message)s"
        )

    input_p = Path(input_svg)
    output_p = Path(output_svg)

    try:
        # The verbose flag in RemoveOverlapsSVG is now primarily for tqdm visibility
        remover = RemoveOverlapsSVG(
            cairo=cairo, picofy=picofy, keep_white=keep_white, verbose=verbose
        )
        remover.load_svg(input_p)
        remover.remove(sequential=sequential)
        remover.save_svg(output_p)
        logger.info(f"Successfully processed SVG and saved to {output_p}")
        # For non-verbose, a simple print to stdout might be preferred for success
        if not verbose:
            print(f"Output SVG saved to: {output_p}")

    except SVGProcessingError as e:
        logger.error(f"An error occurred during SVG processing: {e}")
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e: # Catch other value errors that might not be SVGProcessingError
        logger.error(f"Invalid input or value: {e}")
        print(f"Error: Invalid input - {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e: # Catch-all for any other unexpected errors
        logger.error(f"An unexpected error occurred: {e}", exc_info=verbose) # Log traceback if verbose
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)



def cli():
    # Configure Fire to use custom display for help and error messages
    # This ensures that Fire's output (like help text) goes to stdout as expected.
    fire.core.Display = lambda lines, out: print(*lines, file=out)
    fire.Fire(remove_overlaps)


if __name__ == "__main__":
    cli()
