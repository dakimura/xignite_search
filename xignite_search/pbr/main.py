#!/usr/bin/python
# -*- coding:utf-8 -*-

import logging
from xignite_search.config import config
from xignite_search.pbr.symbol import SecurityManager


def make_pbr_ranking(api_client, symbols):
    m = SecurityManager(api_client=api_client, symbols=symbols)

    m.fetch_shares(config.number_of_issued_shares_csv)
    m.fetch_net_assets()
    m.fetch_price()
    m.compute_pbr()
    m.remove_no_pbr_symbols()
    sorted = m.sort_by_pbr()

    for security in sorted:
        print(vars(security))
