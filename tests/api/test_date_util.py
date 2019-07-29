# -*- coding:utf-8 -*-

import unittest
from xignite_search.api import date_util
import datetime


class TestDateUtil(unittest.TestCase):

    def test_calculate_last_open_date(self):
        # ---- given ----
        closed_days = [
            datetime.date(year=2019, month=7, day=15),  # Sea Day, Monday
        ]
        today = datetime.date(year=2019, month=7, day=16)

        # ---- when ----
        got = date_util.calc_last_open_date(today, closed_days)

        # ---- then ----
        self.assertEqual(got, datetime.date(year=2019, month=7, day=12))  # last Friday
