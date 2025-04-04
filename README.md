# geneflock

Renders a genome, one line per chromosome with the genes represented as colored boxes and output as an SVG file. Can be used from the command line or as an extensible python module.

## Installation

Install using `pip`
```
pip install git+https://github.com/ulido/geneflock
```

## Usage
```
usage: geneflock [-h] [--highlight-genes-file HIGHLIGHT_GENES_FILE] [--forward-color FORWARD_COLOR] [--reverse-color REVERSE_COLOR]
                 [--highlight-color HIGHLIGHT_COLOR]
                 GFF_file output_file

Read a genome GFF file and produce an SVG file with each chromosome rendered as a line and colored boxes representing the genes.

positional arguments:
  GFF_file              The path to the GFF file.
  output_file           The path to the generated SVG file

options:
  -h, --help            show this help message and exit
  --highlight-genes-file HIGHLIGHT_GENES_FILE
                        The path to a file containing a list of gene IDs to highlight (one per line).
  --forward-color FORWARD_COLOR
                        Color of forward-strand genes.
  --reverse-color REVERSE_COLOR
                        Color of reverse-strand genes.
  --highlight-color HIGHLIGHT_COLOR
                        Color of highlighted genes.
```