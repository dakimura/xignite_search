# -*- coding:utf-8 -*-

from xignite_search.pbr.balance_sheet import BalanceSheet


class BalanceSheetHistory:
    """
    Attributes:
        balance_sheets (list of BalanceSheet): an array of balance sheets
    """

    def __init__(self, symbol: str, name: str, balance_sheets: list):
        self.symbol = symbol
        self.name = name
        self.balance_sheets = balance_sheets
