from pdfminer.layout import LTTextBoxHorizontal

from .columns import columncoordinates
from .util import within
from .tables import top, bottom

def txid_elms(elms):
    "return tx id text box elements from column 4"

    t, b = top(elms), bottom(elms)
    l, r = columncoordinates(elms)[3]
    txtelms = (elm for elm in elms if isinstance(elm, LTTextBoxHorizontal))
    for telm in txtelms:
        if within(telm, top=t, bottom=b, left=l, right=r):
            yield telm


def txcolbox(elms):
    "return coordinates and dimensions for the tx id columnn 4"

    # get top & bottom and left & right
    t, b = top(elms), bottom(elms)
    l, r = columncoordinates(elms)[3]

    # calculate width and height
    w = r - l
    h = t - b

    # TODO remove assertions at some point when matured or have tests

    assert w > 0
    assert h > 0
    assert l > 0
    assert r > 0

    return {
        "x0": l,
        "y0": b,
        "x1": r,
        "y1": t,
        "width": w,
        "height": h
    }
