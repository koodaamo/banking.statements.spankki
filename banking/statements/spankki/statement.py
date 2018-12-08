"""
Statement-level utilities
"""

from datetime import date

from .pages import all_txt_elms
from .util import within


def stmt_date(elms):
    "return the statement date in ISO 8601 format (YYYY-MM-DD)"
    for elm in all_txt_elms(elms):
        if within(elm, left=530, right=567, top=778, bottom=766):
            ds = elm.get_text().strip()
            ds = ds.split('.')
            ds.reverse()
            return date.fromisoformat('-'.join(ds))

def stmt_iban(elms):
    "return the statement account IBAN"
    for elm in all_txt_elms(elms):
        if within(elm, left=402, right=482, top=736, bottom=724):
            return elm.get_text().strip()
