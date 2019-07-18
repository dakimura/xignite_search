# -*- coding: utf-8 -*-

import datetime


class IncomeStatement:

    def __init__(self,
                 fiscal_period_end_year: int, fiscal_period_end_month: int,
                 net_income: int, operating_income: int):
        # ex. 2018
        self.fiscal_period_end_year = fiscal_period_end_year
        # ex. 3
        self.fiscal_period_end_month = fiscal_period_end_month
        # --- results (, not forecast) ---
        self.net_income = net_income
        self.operating_income = operating_income
        # --------------------------------

    def is_after(self, date: datetime.date):
        """
        :param date:
        :return: true if the end of the period of the income statement is after the date
        """
        if date.year < self.fiscal_period_end_year:
            return True

        if date.year == self.fiscal_period_end_year:
            return date.month < self.fiscal_period_end_month

        # date.year > self.fiscal_period_end_year
        return False
