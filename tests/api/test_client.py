# -*- coding:utf-8 -*-

import logging
import os
import unittest

import requests
import requests_mock

from xignite_search.api.client import XigniteAPIClient


class TestXigniteAPIClient(unittest.TestCase):
    api_token = "foobar"

    @classmethod
    def setUpClass(self):
        logging.basicConfig(
            format='[%(asctime)s - %(name)s - %(levelname)s] %(message)s',
            level=logging.DEBUG)

    def setUp(self):
        self.session = requests.session()
        self.adapter = requests_mock.Adapter()
        self.session.mount('mock', self.adapter)

    def test_list_symbols(self):
        # ---- given ----
        with open(os.path.dirname(__file__) + "/fixtures/list_symbols.json", "r") as f:
            response = f.read()
        self.adapter.register_uri('GET', 'mock://mock.com/QUICKEquityRealTime.json/ListSymbols', text=response)

        SUT = XigniteAPIClient(base_url="mock://mock.com", api_token="foobar", closed_days=[], session=self.session)
        # ---- when ----
        symbols = SUT.list_symbols("fizzbuzz")

        # ---- then ----
        self.assertEqual(['1301', '1305', '1306', '1308', '1309'], symbols)

    def test_get_income_statement_history(self):
        # ---- given ----
        with open(os.path.dirname(__file__) + "/fixtures/get_income_statement_history.json", "r") as f:
            response = f.read()
        self.adapter.register_uri('POST', 'mock://mock.com/QUICKFinancialStatements.json/GetIncomeStatementHistory',
                                  text=response)
        SUT = XigniteAPIClient(base_url="mock://mock.com", api_token="foobar", closed_days=[], session=self.session)

        # ---- when ----
        income_history = SUT.get_income_statement_history(["6501", "7751"])

        # ---- then ----
        self.assertEqual("6501", income_history[0].symbol)
        self.assertEqual("2019", income_history[0].income_statements[0].fiscal_year)
        self.assertEqual(222546, income_history[0].income_statements[0].net_income)
        self.assertEqual(754976, income_history[0].income_statements[0].operating_income)

    def test_get_balance_sheet_history(self):
        # ---- given ----
        with open(os.path.dirname(__file__) + "/fixtures/get_balance_sheet_history.json", "r") as f:
            response = f.read()
        self.adapter.register_uri('POST', 'mock://mock.com/QUICKFinancialStatements.json/GetBalanceSheetHistory',
                                  text=response)
        SUT = XigniteAPIClient(base_url="mock://mock.com", api_token="foobar", closed_days=[], session=self.session)

        # ---- when ----
        bs_history = SUT.get_balance_sheet_history(["6501", "7751"])

        # ---- then ----
        self.assertEqual("6501", bs_history["6501"].symbol)
        self.assertEqual(2019, bs_history["6501"].balance_sheets[0].fiscal_year)
        self.assertEqual(4414403, bs_history["6501"].balance_sheets[0].net_assets)
