# -*- coding:utf-8 -*-

from typing import List

from xignite_search.config import config
from xignite_search.pbr.symbol import SecurityManager, Security


def make_pbr_ranking(api_client, symbols, output_csv_filepath: str):
    m = SecurityManager(api_client=api_client, symbols=symbols)

    m.fetch_shares(config.number_of_issued_shares_csv)
    m.fetch_net_assets()
    m.fetch_price()
    m.compute_pbr()
    m.remove_data_not_found_symbols()
    sorted = m.sort_by_pbr()
    output_to_csv(output_csv_filepath, sorted)


def output_to_csv(filepath, sorted_securities: List[Security]):
    with open(filepath, "w") as f:
        f.write("symbol,name,pbr,price,net_asset,share\n")
        for s in sorted_securities:
            f.write("{},\"{}\",{},{},{},{}\n".format(s.symbol, s.name, s.pbr, s.price, s.net_asset, s.shares))
