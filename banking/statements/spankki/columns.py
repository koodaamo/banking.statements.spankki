"""
Transaction table column utilities

"""

from pdfminer.layout import LTLine


def columncoordinates(elms):
    "return (left, right) tuples for column x-coordinates"
    coords = [e.x0 for e in elms if isinstance(e, LTLine) and e.x0 == e.x1]
    ordered = sorted(coords)
    return tuple(zip(ordered, ordered[1:]))

