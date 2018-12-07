"""
Transaction table row utilities

"""

from pdfminer.layout import LTTextLine

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


def rowcontents(elms):
    txtelms = list(all_txt_elms(elms))
    for (upper, lower) in rowcoordinates(elms):
        rowelms = [e for e in txtelms if e.y0 >= lower - 3 and e.y1 <= upper + 3]
        rowelms.sort(key=lambda e: e.x0)

        if rowelms[0].get_text().strip().endswith("HOK-ELANTO"):
            assert len(rowelms) == 4
            rowelms.insert(2, LTTextLine(""))

        elif rowelms[4].get_text().strip()=="* JATKUU *":
            del rowelms[4]
            assert len(rowelms) == 6, [e.get_text().strip() for e in rowelms]

        elif "TILISIIRTO" in rowelms[2].get_text().strip():
            assert len(rowelms) == 8, [e.get_text().strip() for e in rowelms]
        else:
            assert len(rowelms) == 6, [e.get_text().strip() for e in rowelms]

        rowtxts = [e.get_text().strip() for e in rowelms]
        rowtxts[-1] = rowtxts[-1].rstrip('-').replace(',', '.')


        if " A" not in rowtxts[0]:
            rowtxts[0] = rowtxts[0] + " A " + rowtxts[1]
            del rowtxts[1]

        # merge message fields

        if "TILISIIRTO" in rowtxts[1]:
            # custom case :(
            rowtxts[2] = ' '.join(rowtxts[2:5])
            del rowtxts[3:5]
            assert len(rowtxts) == 5
        else:
            rowtxts[2] = rowtxts[2] + " " + rowtxts[3]
            del rowtxts[3]

        row = []
        for i, txt in enumerate(rowtxts):
            parts = [p.strip() for p in txt.split()]

            if i==0:
                row.extend((parts[0] + ' ' + parts[1] , parts[2], ' '.join(parts[3:])))
            elif i==1:
                row.extend(parts)
            else:
                row.append(txt)

        yield row


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





