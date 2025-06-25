#!/usr/bin/env python3
import skia
from fire import Fire


def remove_overlaps(input_file, output_file):
    # Load input SVG
    stream = skia.FILEStream(input_file)
    svgdom = skia.SVGDOM.MakeFromStream(stream)

    # Get the SVG root container
    root_container = svgdom.root()

    # Iterate through all children and extract Skia paths
    skia_paths = []
    for i in range(root_container.children()):
        svg_node = root_container.getChild(i)
        if isinstance(svg_node, skia.SVGPath):
            skia_paths.append(svg_node.getPath())

    # Perform PathOps union operation
    builder = skia.PathOpBuilder()
    for path in skia_paths:
        builder.add(path, skia.PathOp.kUnion)
    result_path = builder.resolve()

    # Save the resulting path to output SVG
    width, height = 800, 600
    stream = skia.FILEWStream(output_file)
    canvas = skia.SVGCanvas.Make((width, height), stream)
    paint = skia.Paint()
    paint.setColor(skia.ColorBLACK)
    paint.setStyle(skia.Paint.kStroke_Style)
    paint.setStrokeWidth(1)
    canvas.drawPath(result_path, paint)
    del canvas
    stream.flush()


if __name__ == "__main__":
    Fire(remove_overlaps)
