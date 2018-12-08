"""
Transaction table row utilities

"""

from pdfminer.layout import LTAnno

from .pages import all_txt_elms
from .txids import txid_elms
from .tables import top, bottom

def rowcoordinates(elms):
    ordered = sorted(txid_elms(elms), key=lambda e: e.y1, reverse=True)
    assert ordered[0].y0 < ordered[0].y1
    coords = [e.y1 for e in ordered]
    #coords[0] = top(elms)
    coords.append(bottom(elms))
    return tuple(zip(coords, coords[1:]))


def txtelmrows(elms, under=2, over=2):
    "generate coordinate-bound text element rows (coordinates extended by under and over)"
    txtelms = tuple(all_txt_elms(elms))
    for (upper, lower) in rowcoordinates(elms):
        yield (e for e in txtelms if e.y0 >= lower - under and e.y1 <= upper + over)


def txtrow(rowelemgen):
    rowelems = list(rowelemgen)
    rowelems.sort(key=lambda e: e.x0)
    return [e.get_text().strip() for e in rowelems]


def normalizerow(row):
    "fix row contents"

    size = len(row)

    for i, txt in enumerate(row):
        if "KIRJAUSPÄIVÄ" in txt:
            del row[i]

    # fix short row in case of "system" transactions
    if size == 4 and row[0].endswith("HOK-ELANTO"):
        row.insert(2, "")
        row.insert(2, "")

    # fix special 'continuation' case
    elif size == 7 and row[4]=="* JATKUU *":
        del row[4]

    # normalize start of row into ([0-9]+ A) form
    if "A" not in row[0]:
        row[0] += " A " + row[1]
        del row[1]

    parts = row[0].split()

    # add id
    row[0] = parts.pop(0) + ' ' + parts.pop(0)

    # add payment date
    row.insert(1, parts.pop(0))

    # merge and add vendor
    vendor = ' '.join(parts)
    row.insert(2, vendor)

    # add valuation date and tx type
    parts = row[3].split()
    datev = parts.pop(0)
    txtype = parts[0] if len(parts)==1 else ' '.join(parts)
    del row[3]
    row.insert(3, txtype)
    row.insert(3, datev)

    # merge message
    msgparts = row[5:-2]
    combined = ' '.join(msgparts)
    del row[5:-2]
    row.insert(5, combined)

    return row


def old_normalizerow(row):
    "fix row element count"
    row = list(row)
    row.sort(key=lambda e: e.x0)
    size = len(row)

    txts = [e.get_text().strip() for e in row]

    if size == 6:
        pass

    # fix short row
    elif size == 4 and row[0].get_text().strip().endswith("HOK-ELANTO"):
        row.insert(2, LTAnno(""))
        row.insert(2, LTAnno(""))

    # fix special case
    elif size == 7 and row[4].get_text().strip()=="* JATKUU *":
        del row[4]

    # fix special case (also has TILISIIRTO)
    elif size == 8:
        row0txt = row[0].get_text().strip()
        if not row0txt.endswith(" A"):
            combined = row0txt + " A " + row[1].get_text().strip()
            row.insert(0, LTAnno(combined))
            del row[1:3]

        # merge automatic message elements and move them before the user-given one
        combined = row[3].get_text().strip() + " " + row[4].get_text().strip()
        del row[3:5]
        row.insert(2, LTAnno(combined))

    # merge the two message elements
    combined = row[2].get_text().strip() + " " + row[3].get_text().strip()
    del row[2:4]
    row.insert(2, LTAnno(combined))

    return row


def rowcontents(elms):
    for txtelmrow in txtelmrows(elms):
        yield normalizerow(txtrow(txtelmrow))


def fixedrows(elms):
    _top, _bottom = top(), bottom()
    rowtop = _top +2.4
    bottom = _bottom -1
    rows = 46
    rowheight = (_top - _bottom) / rows
    print(rowheight)
    rowbottom = rowtop - rowheight
    txtelms = list(all_txt_elms(elms))

    while rowbottom > bottom:
        yield [e.get_text().strip() for e in txtelms if e.y0 >= rowbottom-3 and e.y1 <= rowtop+3]
        rowtop = rowbottom
        rowbottom = rowtop - rowheight





