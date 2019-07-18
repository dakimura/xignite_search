#!/usr/bin/python
# -*- coding:utf-8 -*-

from xignite_search.api.client import XigniteAPIClient
from xignite_search.config import config
from xignite_search.income.main import searchCompanies_PositiveIncome
from xignite_search.pbr.main import make_pbr_ranking

import logging


def get_symbols(api_client, exchanges):
    symbols = []
    for exchange in exchanges:
        s = api_client.list_symbols(exchange)
        symbols.extend(s)

    return symbols


def run():
    # init the Xignite API client
    client = XigniteAPIClient(config.xignite_base_url, config.api_token, config.closed_days)

    # list up the target symbols
    symbols = get_symbols(client, config.exchanges)

    # # output symbols which has positive net/operating income for n consecutive years
    # searchCompanies_PositiveIncome(client, symbols, config.target_period_in_year,
    #                                config.output_net_income, config.output_operating_income)

    # make PBR ranking
    make_pbr_ranking(client, symbols)


if __name__ == "__main__":
    logging.basicConfig(
        format='[%(asctime)s - %(name)s - %(levelname)s] %(message)s',
        level=config.log_level)

    run()
