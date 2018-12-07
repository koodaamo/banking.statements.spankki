"Page-level utilities"

import io

from pdfminer.pdfdocument import PDFDocument
from pdfminer.converter import PDFPageAggregator
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LAParams
from pdfminer.pdfparser import PDFParser
from pdfminer.layout import LTTextLine, LTTextContainer


resource_manager = PDFResourceManager()
laparams = LAParams()
device = PDFPageAggregator(resource_manager, laparams=laparams)
interpreter = PDFPageInterpreter(resource_manager, device)


def pages(pdfpath):
    "return all pages"
    with open(pdfpath, "rb") as fp:
        data = io.BytesIO(fp.read())
    parser = PDFParser(data)
    document = PDFDocument(parser)
    return PDFPage.create_pages(document)

def elements(page):
    "return all elements on a page"
    interpreter.process_page(page)
    return device.get_result()

def all_txt_elms(elms):
    "walk all text elements on a page"

    # TODO preselect just all the LTText - derived elements

    for elm in elms:
        if isinstance(elm, LTTextLine):
            yield elm
        elif isinstance(elm, LTTextContainer):
            for subelm in elm:
                yield subelm
        elif elm.__class__.__name__.startswith("LTText"):
            raise Exception("unhandled text element: %s" % elm.__class__.__name__)
        else:
            pass


