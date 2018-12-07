# -*- encoding: utf-8 -*-
import sys
import csv
import decimal
from importlib import import_module
from io import StringIO

from ofxstatement.plugin import Plugin, PluginNotRegistered
from .parser import SPStatementParser, SIGNATURES

class SPPlugin(Plugin):
    "Suomen S-Pankki / Finnish S-Pankki"

    def get_parser(self, pdfpath):
        f = open(fin, "r", encoding='iso-8859-1')
        signature = f.readline().strip()
        f.seek(0)
        if signature in SIGNATURES:
            parser = SPCsvStatementParser(f)
            parser.statement.account_id = self.settings['account']
            parser.statement.currency = self.settings['currency']
            parser.statement.bank_id = self.settings.get('bank', 'S-Pankki')
            return parser

        # no plugin with matching signature was found
        raise Exception("No suitable S-Pankki parser found for this statement file.")
