import datetime
import logging
import os

# Log Level
log_level = logging.DEBUG

# Base URL of Xignite API without trailing '/'
xignite_base_url = "https://api.marketdata-cloud.quick-co.jp"

# API Token for Xignite API
api_token = os.environ['XIGNITE_API_TOKEN']

# target exchanges to analyze. XTKS=Tokyo Stock Exchange, XJAS=JASDAQ
exchanges = ["XTKS", "XJAS"]
# exchanges = ["XJAS"]

# ----- get symbols which have positive net/operating incomes for n
# consecutive years
# How many years of net income & operating income this module analyzes
target_period_in_year = 5

# filepaths of the output csv
output_net_income = "/tmp/output/positive_net_income.csv"
output_operating_income = "/tmp/output/positive_operating_income.csv"

# ----- make PBR(Price Book-value Ratio) ranking ---------------------------
number_of_issued_shares_csv = "/tmp/xignite_search/config/security_code_and_number_of_shares2.csv"

# filepath of the output csv
output_pbr_ranking = "/tmp/output/pbr_ranking.csv"

# days that the market is closed
closed_days = [
    datetime.date(year=2019, month=1, day=1),
    datetime.date(year=2019, month=1, day=2),
    datetime.date(year=2019, month=1, day=3),
    datetime.date(year=2019, month=1, day=4),
    datetime.date(year=2019, month=2, day=11),
    datetime.date(year=2019, month=3, day=21),
    datetime.date(year=2019, month=4, day=29),
    datetime.date(year=2019, month=4, day=30),
    datetime.date(year=2019, month=5, day=1),
    datetime.date(year=2019, month=5, day=2),
    datetime.date(year=2019, month=5, day=3),
    datetime.date(year=2019, month=5, day=4),
    datetime.date(year=2019, month=5, day=5),
    datetime.date(year=2019, month=5, day=6),
    datetime.date(year=2019, month=7, day=15),
    datetime.date(year=2019, month=8, day=11),
    datetime.date(year=2019, month=8, day=12),
    datetime.date(year=2019, month=9, day=16),
    datetime.date(year=2019, month=9, day=23),
    datetime.date(year=2019, month=10, day=14),
    datetime.date(year=2019, month=10, day=22),
    datetime.date(year=2019, month=11, day=3),
    datetime.date(year=2019, month=11, day=4),
    datetime.date(year=2019, month=11, day=23),
    datetime.date(year=2019, month=12, day=31),
    datetime.date(year=2020, month=1, day=1),
    datetime.date(year=2020, month=1, day=2),
    datetime.date(year=2020, month=1, day=3),
    datetime.date(year=2020, month=1, day=13),
    datetime.date(year=2020, month=2, day=11),
    datetime.date(year=2020, month=2, day=23),
    datetime.date(year=2020, month=2, day=24),
    datetime.date(year=2020, month=3, day=20),
    datetime.date(year=2020, month=4, day=29),
    datetime.date(year=2020, month=5, day=3),
    datetime.date(year=2020, month=5, day=4),
    datetime.date(year=2020, month=5, day=5),
    datetime.date(year=2020, month=5, day=6),
    datetime.date(year=2020, month=7, day=23),
    datetime.date(year=2020, month=7, day=24),
    datetime.date(year=2020, month=8, day=10),
]
