# -*- coding:utf-8 -*-


class BalanceSheet:

    def __init__(self, fiscal_period_end_year: int, fiscal_period_end_month: int, net_assets: int):
        # ex. 2018
        self.fiscal_period_end_year = fiscal_period_end_year
        # ex. 3
        self.fiscal_period_end_month = fiscal_period_end_month
        self.net_assets = net_assets
        # TODO: self.accounting_standard = accounting_standard
