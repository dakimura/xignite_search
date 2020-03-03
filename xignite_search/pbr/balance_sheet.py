# -*- coding:utf-8 -*-


class BalanceSheet:

    def __init__(self, fiscal_period_end_year: int, fiscal_period_end_month: int, net_assets: int, report_type: str,
                 fiscal_year: int):
        # e.g. 2018
        self.fiscal_period_end_year = fiscal_period_end_year
        # e.g. 3
        self.fiscal_period_end_month = fiscal_period_end_month
        self.net_assets = net_assets
        # "Q1", "Q2", "Q3" or "Annual"
        self.report_type = report_type
        # e.g. 2016, 2018
        self.fiscal_year = fiscal_year
        # TODO: self.accounting_standard = accounting_standard
