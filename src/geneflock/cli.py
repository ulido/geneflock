"""cli.py

Command line interface for geneflock.
"""
import argparse
import pathlib

from .geneflock import Genome
from .genehighlight import HighlightIDListGenome


def cli():
    """Command line interface."""
    parser = argparse.ArgumentParser(
        description=(
            "Read a genome GFF file and produce an SVG file with each chromosome rendered as a line "
            "and colored boxes representing the genes."
        )
    )
    parser.add_argument("GFF_file", type=pathlib.Path, help="The path to the GFF file.")
    parser.add_argument("output_file", type=pathlib.Path, help="The path to the generated SVG file")
    parser.add_argument("--highlight-genes-file", type=pathlib.Path,
                        help="The path to a file containing a list of gene IDs to highlight"
                        " (one per line).")
    parser.add_argument("--forward-color", type=str, default="red",
                        help="Color of forward-strand genes.")
    parser.add_argument("--reverse-color", type=str, default="blue",
                        help="Color of reverse-strand genes.")
    parser.add_argument("--highlight-color", type=str, default="green",
                        help="Color of highlighted genes.")

    args = parser.parse_args()
    gff_file: pathlib.Path = args.GFF_file
    output_file: pathlib.Path = args.output_file

    colors = {
        "forward_color": args.forward_color,
        "reverse_color": args.reverse_color,
    }

    genome: Genome
    if args.highlight_genes_file is None:
        genome = Genome(gff_file, **colors)
    else:
        list_file_path: pathlib.Path = args.highlight_genes_file
        with list_file_path.open(mode="r") as list_file:
            highlight_ids = [entry.strip() for entry in list_file]
        colors["highlight_color"] = args.highlight_color
        genome = HighlightIDListGenome(highlight_ids, gff_file, **colors)

    with output_file.open(mode="w") as output:
        output.write(genome.render())
