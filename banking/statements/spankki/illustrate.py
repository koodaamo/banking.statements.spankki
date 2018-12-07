"""

Some utility functions to illustrate parsed structures using matplotlib, useful mostly
for debugging and testing.

The functions expect a matplotlib Axes object, and the plot coordinate system should be
already set up. Like this:

>>> import matplotlib.pyplot as plt
>>> ax = plt.gca()
>>> plt.ylim(0, 700)
>>> plt.xlim(0, 600)

"""

from statistics import mean
from pdfminer.layout import LTLine, LTRect
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle

from .txids import txid_elms, txcolbox
from .tables import left, right
from .rows import rowcoordinates


def prepare_rendering():
    import matplotlib.pyplot as plt
    plt.rcParams["figure.figsize"] = (7.5*1.4, 6*1.4)
    plt.ylim(0, 750)
    plt.xlim(0, 600)
    ax = plt.gca()
    return (plt, ax)


def render_table(elms, ax):
    "draw the tx table"

    # Draw all the lines we find
    lines = [i for i in elms if isinstance(i, LTLine)]
    for i, l in enumerate(lines):
        dl = Line2D((l.x0, l.x1), (l.y0,l.y1))
        ax.add_line(dl)

    # Draw all the rectangle boxes
    boxes = [i for i in elms if isinstance(i, LTRect)]
    for i, b in enumerate(boxes):
        ax.add_patch(Rectangle((b.x0, b.y0), b.width, b.height, fill=None, alpha=1))


    # Highlight the tx column
    box = txcolbox(elms)
    #ax.add_patch(Rectangle((box["x0"], box["y0"]), box["width"], box["height"], fill="#EEEEEE", alpha=0.05))

    # Indicate vertical area occupied bu the transaction column text contents
    l, r = left(elms), right(elms)
    txelms = txid_elms(elms)
    ordered = sorted(txid_elms(elms), key=lambda e: e.y1, reverse=True)
    txcolx = mean((box["x0"], box["x1"]))

    for elm in ordered:
        height = elm.y1-elm.y0
        lbl = elm.get_text().strip()
        ax.add_patch(Rectangle((l, elm.y0),r-l, height, facecolor="#999999", alpha=0.1))
        ax.text(txcolx-5, elm.y0, lbl, fontsize=10)

    # Draw the row areas from which we extract transaction textual data
    bg = "#FF0000"
    hatch = "/"
    for rowtop, rowbottom in rowcoordinates(elms):
        height = rowtop - rowbottom
        ax.add_patch(Rectangle((l, rowbottom),r-l, height, hatch=hatch, facecolor=bg, edgecolor="#00FF00", alpha=0.05))
        bg = "#FF0000" if bg=="#0000FF" else "#0000FF"
        hatch = "/" if hatch=="\\" else "\\"
