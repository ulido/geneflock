"""genehightlight.py

Extends geneflock.py to allow highlighting of individual genes.
"""

from .geneflock import Genome


class HighlightIDListGenome(Genome):
    """Subclass of Genome, allowing one to specify a list of highlighted genes."""
    def __init__(self, idlist: list[str], *args, highlightcolor: str = "green", **kwargs):
        self.idlist = idlist
        self.highlightcolor = highlightcolor
        super().__init__(*args, **kwargs)

    def style(self):
        styles = super().style()

        highlightlist = ','.join(["#" + entry.replace(".", "_")
                                 for entry in self.idlist])
        styles += highlightlist + f"{{ fill: {self.highlightcolor}; }}"
        return styles
