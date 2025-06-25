#!/usr/bin/env python3
import re

import skia
import svgpathtools as svg
from cairosvg.surface import SVGSurface
from fire import Fire
from tqdm import tqdm


def to_num(s):
    return float(re.sub(r"[^\d.]", "", s))


def svg2svg(svg_file):
    return SVGSurface.convert(file_obj=svg_file)


def convert_svg_to_skia(svg_path):
    skia_path = skia.Path()

    for segment in svg_path:
        end = segment.end

        if isinstance(segment, svg.Line):
            skia_path.lineTo(end.real, end.imag)
        elif isinstance(segment, svg.QuadraticBezier):
            skia_path.quadTo(
                segment.control.real, segment.control.imag, end.real, end.imag
            )
        elif isinstance(segment, svg.CubicBezier):
            ctrl1, ctrl2 = segment.control1, segment.control2
            skia_path.cubicTo(
                ctrl1.real, ctrl1.imag, ctrl2.real, ctrl2.imag, end.real, end.imag
            )
        elif isinstance(segment, svg.Arc):
            raise NotImplementedError("Arc conversion is not implemented.")
        else:
            raise ValueError(f"Unknown segment type: {type(segment)}")

        if segment != svg_path[-1]:
            skia_path.moveTo(end.real, end.imag)

    return skia_path


def remove_overlaps(input_file, output_file):
    print(f"Reading {input_file}...")
    with open(input_file) as svg_file:
        svg_str = svg2svg(svg_file).decode("utf-8")
    svg_paths, attributes, svg_attributes = svg.svgstr2paths(
        svg_str, return_svg_attributes=True
    )
    skia_paths = []
    for svg_path in tqdm(svg_paths, desc="Converting paths"):
        skia_paths.append(convert_svg_to_skia(svg_path))
    builder = skia.OpBuilder()
    for path in tqdm(skia_paths, desc="Removing overlaps"):
        builder.add(path, skia.kUnion_PathOp)
    result_path = builder.resolve()
    width = to_num(svg_attributes.get("width", "800"))
    height = to_num(svg_attributes.get("height", "600"))
    print(f"Saving {output_file}...")
    stream = skia.FILEWStream(output_file)
    canvas = skia.SVGCanvas.Make((width, height), stream)
    paint = skia.Paint()
    paint.setColor(skia.ColorBLACK)
    canvas.drawPath(result_path, paint)
    del canvas
    stream.flush()


if __name__ == "__main__":
    Fire(remove_overlaps)
