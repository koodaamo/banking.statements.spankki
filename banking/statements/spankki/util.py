"""

Misc. utilities

"""

def within(elm, left=None, right=None, top=None, bottom=None):
    if left and right and (elm.x0 < left or elm.x1 > right):
        return False
    if top and bottom and (elm.y0 < bottom or elm.y1 > top):
        return False
    return True
