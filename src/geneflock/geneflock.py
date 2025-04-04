"""geneflock.py

Module to render a genome to SVG, each chromosome represented as a line, with
colored boxes representing genes.
"""

import pathlib
from geffa.geffa import GffFile, SequenceRegion, GeneNode


class Gene:
    """Class rendering a single gene."""
    def __init__(self, genenode: GeneNode):
        self.genenode = genenode

    @property
    def extent(self):
        """Length of the gene in basepairs."""
        return self.genenode.end - self.genenode.start + 1

    @property
    def id(self):
        """Unique gene ID, formatted to act as as CSS selector."""
        return self.genenode.attributes["ID"].replace(".", "_")

    @property
    def direction(self):
        """Gene direction (left-right or right-left)"""
        if self.genenode.strand == '+':
            return "left-right"
        elif self.genenode.strand == '-':
            return "right-left"
        raise ValueError("GeneNode has no strand!")

    def render(self):
        """Render the gene as SVG element(s)."""
        d = -1 if self.genenode.strand == "+" else 1
        f = (1-d)*0.5
        return f'''
        <rect
            x="{self.genenode.start-1}"
            y="0.5"
            width="{self.extent}"
            height="0.25"
            transform="matrix(1, 0, 0, {d}, 0, {f})"
            class="gene {self.direction}"
            id="{self.id}"/>'''


class Chromosome:
    """Class rendering a chromosome."""
    def __init__(self, seqreg: SequenceRegion):
        self.seqreg = seqreg

    @property
    def id(self):
        """Unique chromosome ID, formatted to act as as CSS selector."""
        return self.seqreg.name.replace(".", "_")

    @property
    def extent(self):
        """Length of the chromosome in basepairs."""
        return self.seqreg.end - self.seqreg.start + 1

    def render(self, offset=0):
        """Render the chromosome and any genes contained within as SVG elements."""
        s = f'<g transform="translate(0 {offset})" id="{self.id}">'
        s += f'<text y="0.2" transform="scale(10000, 1)" class="chromosome-name">{self.seqreg.name}</text>'
        for gene in (feature for feature in self.seqreg.node_registry.values() if feature.type == "gene"):
            s += Gene(gene).render()
        s += f'<path d="M 0,0.5 h {self.extent}" class="chromosome"/></g>'
        return s


DEFAULT_STYLE = """
.background {
    fill: white;
}

.chromosome {
    stroke: black;
    stroke-width: 0.1px;
    zorder: 100;
}

.gene {
    height: 0.25px;
}

.left-right {
    fill: ##FORWARD_COLOR##;
}

.right-left {
    fill: ##REVERSE_COLOR##;
}

.chromosome-name {
    font-size: 0.25px;
    font-family: sans-serif;
}
"""


class Genome:
    """Class rendering a genome (given as a GFF file) as an SVG drawing."""
    def __init__(
            self,
            gfffile: str | pathlib.Path | GffFile,
            filter_chromosomes=lambda c: c.extent > 100000,
            forward_color: str = "red",
            reverse_color: str = "blue",
    ):
        if not isinstance(gfffile, GffFile):
            gfffile = GffFile(gfffile)
        self.gfffile = gfffile

        self.chromosomes = [Chromosome(seqreg) for seqreg in self.gfffile.sequence_regions.values(
        ) if len(seqreg.node_registry) > 0]
        self.chromosomes = [
            chromosome for chromosome in self.chromosomes if filter_chromosomes(chromosome)]
        
        self.forward_color = forward_color
        self.reverse_color = reverse_color

    @property
    def height(self):
        """The 'height' of the genome (the number of chromosomes contained)."""
        return len(self.chromosomes)

    @property
    def width(self):
        """The 'width' of the genome (the length in basepairs of the longest chromosome)."""
        return max([chromosome.extent for chromosome in self.chromosomes])

    def style(self):
        """CSS styles of the rendered SVG file."""
        return (
            DEFAULT_STYLE
            .replace("##FORWARD_COLOR##", self.forward_color)
            .replace("##REVERSE_COLOR##", self.reverse_color)
        )

    def render(self):
        """Render the genome with all chromosomes contained therein as a SVG file."""
        s = f'''<svg
            viewBox="0 0 {self.width} {self.height}"
            preserveAspectRatio="none"
            xmlns="http://www.w3.org/2000/svg"
            height="{self.height * 100}"
            width="{self.width / 100}">
        '''
        s += f"<style>{self.style()}</style>"
        s += '<rect height="100%" width="100%" class="background"/>'
        for offset, chromosome in enumerate(self.chromosomes):
            s += chromosome.render(offset)
        s += "</svg>"
        return s
