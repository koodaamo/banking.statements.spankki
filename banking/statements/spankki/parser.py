"""
S-Pankki provides PDF downloads containing transaction information. This parser uses
PDFMiner to extract information from the PDFs.
"""

import csv
import types
from io import StringIO

from ofxstatement.parser import StatementParser
from ofxstatement.statement import StatementLine, BankAccount
from . import TRANSACTION_TYPES


class CustomStatementLine(StatementLine):
    "don't print the check number"

    def __str__(self):
        return """
        ID: %s, date: %s, amount: %s, payee: %s
        memo: %s
        """ % (self.id, self.date, self.amount, self.payee, self.memo)


class SPStatementParser(StatementParser):
    "parser for various variations with common field semantics"

    mappings = {
       "date":1, "amount":2, "trntype":4, "payee":5,
       "bank_account_to":6, "refnum":7, "memo":8, "id":9
    }

    date_format = "%d.%m.%Y"

    def __init__(self, fin):
        sin=StringIO()
        for l in fin:
           # Some versions from 2011 have broken CSV...
           sin.write(l.replace("&amp;amp;", "&"))
        sin.seek(0)
        super().__init__(sin)

    def split_records(self):
        return csv.reader(self.fin, delimiter=';', quotechar='"')

    def parse_value(self, value, field):
       if field == "bank_account_to":
          return BankAccount("", value)
       else:
          return super().parse_value(value, field)

    def parse_record(self, line):
        #Free Headerline
        if self.cur_record <= 1:
            return None

        # Change decimalsign from , to .
        line[2] = line[2].replace(',', '.')

        # Set transaction type
        line[4] = TRANSACTION_TYPES[line[4]]

        stmt_line = CustomStatementLine()
        for field, col in self.mappings.items():
            if col >= len(line):
                raise ValueError("Cannot find column %s in line of %s items "
                                 % (col, len(line)))
            rawvalue = line[col]
            value = self.parse_value(rawvalue, field)
            setattr(stmt_line, field, value)
        return stmt_line
