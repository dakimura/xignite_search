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
    m.remove_data_not_found_symbols()
    sorted = m.sort_by_pbr()

    print("symbol,name,PBR,price,NetAsset,share")
    for s in sorted:
        print("{},{},{},{},{},{}".format(s.symbol, s.name, s.pbr, s.price, s.net_asset, s.shares))
