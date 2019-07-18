# -* - coding:utf-8 -*-


import unittest
import datetime
from parameterized import parameterized
from xignite_search.income.income_statement import IncomeStatement


class TestIncomeStatement(unittest.TestCase):

    @parameterized.expand([
        (2020, 1, False),
        (2019, 7, False),
        (2019, 6, False),
        (2019, 5, True),
        (2018, 1, True),
    ])
    def test_is_after(self, year, month, expect):
        # ---- given ----
        SUT = IncomeStatement(2019, 6, 123, 456)

        # ---- when ----
        date = datetime.date(year, month, 1)
        got = SUT.is_after(date)

        # ---- then ----
        self.assertEqual(expect, got)
