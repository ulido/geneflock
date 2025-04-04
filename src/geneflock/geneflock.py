import pathlib
from geffa.geffa import GffFile, SequenceRegion, GeneNode

class Gene:
    def __init__(self, genenode: GeneNode):
        self.genenode = genenode

    @property
    def extent(self):
        return self.genenode.end - self.genenode.start + 1
    
    @property
    def id(self):
        return self.genenode.attributes["ID"].replace(".", "_")

    @property
    def direction(self):
        if self.genenode.strand == '+':
            return "left-right"
        elif self.genenode.strand == '-':
            return "right-left"
        raise ValueError("GeneNode has no strand!")

    def render(self):
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
    def __init__(self, seqreg: SequenceRegion):
        self.seqreg = seqreg

    @property
    def id(self):
        return self.seqreg.name.replace(".", "_")

    @property
    def extent(self):
        return self.seqreg.end - self.seqreg.start + 1
    
    def render(self, offset=0):
        s = f'<g transform="translate(0 {offset})" id="{self.id}">'
        s += f'<text y="0.2" transform="scale(10000, 1)" class="chromosome-name">{self.seqreg.name}</text>'
        for gene in (feature for feature in self.seqreg.node_registry.values() if feature.type == "gene"):
            s += Gene(gene).render()
        s += f'<path d="M 0,0.5 h {self.extent}" class="chromosome"/></g>'
        return s

class Genome:
    def __init__(self, gfffile: str | pathlib.Path | GffFile, filter_chromosomes=lambda c: c.extent > 100000):
        if not isinstance(gfffile, GffFile):
            gfffile = GffFile(gfffile)
        self.gfffile = gfffile

        self.chromosomes = [Chromosome(seqreg) for seqreg in self.gfffile.sequence_regions.values() if len(seqreg.node_registry) > 0]
        self.chromosomes = [chromosome for chromosome in self.chromosomes if filter_chromosomes(chromosome)]

    @property
    def height(self):
        return len(self.chromosomes)
    
    @property
    def width(self):
        return max([chromosome.extent for chromosome in self.chromosomes])
    
    def style(self):
        return """
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
                fill: red;
            }

            .right-left {
                fill: blue;
            }

            .chromosome-name {
                font-size: 0.25px;
                font-family: sans-serif;
            }
"""
    
    def render(self):
        s = f'<svg viewBox="0 0 {self.width} {self.height}" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg" height="{self.height * 100}" width="{self.width / 100}">'
        s += f"<style>{self.style()}</style>"
        s += '<rect height="100%" width="100%" class="background"/>'
        for offset, chromosome in enumerate(self.chromosomes):
            s += chromosome.render(offset)
        s += "</svg>"
        return s
