"""
Transaction table utilities

"""

from pdfminer.pdfparser import PDFParser
from pdfminer.layout import LTLine, LTRect
from .pages import all_txt_elms


def top(elms):
    "return the tx table header box bottom line y-coordinate value"
    boxes = [i for i in elms if isinstance(i, LTRect)]
    assert len(boxes) == 1
    box = boxes[0]
    return box.y0

def bottom(elms):
    "return the y-coordinate of the tx table bottom horizontal line"

    elms = list(elms)
    # for the summary page, use "YHTEENVETO" text top as the bottom limit
    summary = [e for e in all_txt_elms(elms) if e.get_text().strip()=="YHTEENVETOTIEDOT"]
    if len(summary) == 1:
        return summary[0].y1

    # for other pages, use the bottom horizontal line
    else:
        lines = [e for e in elms if isinstance(e, LTLine) and e.y0==e.y1]
        assert len(lines) == 1
        return lines[0].y0

def left(elms):
    "return the x-coordinate value of the leftmost vertical table line"
    coords = [e.x0 for e in elms if isinstance(e, LTLine) and e.x0==e.x1]
    return min(coords)

def right(elms):
    "return the x-coordinate value of the rightmost vertical table line"
    coords = [e.x0 for e in elms if isinstance(e, LTLine) and e.x0==e.x1]
    return max(coords)

def constraints(elms):
    "return a dictionary with all the constraint values"

    return {
        "top": top(elms),
        "bottom": bottom(elms),
        "left": left(elms),
        "right": right(elms)
    }
