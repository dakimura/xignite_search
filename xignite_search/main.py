#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys
import os
import logging

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from xignite_search.api.client import XigniteAPIClient
from xignite_search.config import config
from xignite_search.income.main import search_companies_positive_income
from xignite_search.pbr.main import make_pbr_ranking
from xignite_search.net_asset.collector import NetAssetCollector


def get_symbols(api_client, exchanges):
    """
    :param api_client:
    :param exchanges:
    :return: an array of symbol strings (ex. ['1301', '1303', '1304'] )
    """
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

    # output symbols which has positive net/operating income for n consecutive years
    search_companies_positive_income(client, symbols, config.target_period_in_year,
                                     config.output_net_income, config.output_operating_income)

    # make PBR ranking
    make_pbr_ranking(client, symbols, output_csv_filepath=config.output_pbr_ranking)

    # collect net asset of all the target symbols and output to a csv file
    collector = NetAssetCollector(client)
    net_assets = collector.get_net_assets(symbols, fiscal_year=config.net_asset_target_year)
    collector.output_to_csv(filepath=config.output_net_assets, net_assets=net_assets)


def get_incomes():
    # init the Xignite API client
    client = XigniteAPIClient(config.xignite_base_url, config.api_token, config.closed_days)

    # list up the target symbols
    symbols = get_symbols(client, config.exchanges)

    # output symbols which has positive net/operating income for n consecutive years
    search_companies_positive_income(client, symbols, config.target_period_in_year,
                                     config.output_net_income, config.output_operating_income)


def get_net_assets():
    # init the Xignite API client
    client = XigniteAPIClient(config.xignite_base_url, config.api_token, config.closed_days)

    # list up the target symbols
    symbols = get_symbols(client, config.exchanges)

    collector = NetAssetCollector(client)
    net_assets = collector.get_net_assets(symbols, fiscal_year=2018)
    collector.output_to_csv(filepath=config.output_net_assets, net_assets=net_assets)


def pbr_ranking():
    # init the Xignite API client
    client = XigniteAPIClient(config.xignite_base_url, config.api_token, config.closed_days)

    # list up the target symbols
    symbols = get_symbols(client, config.exchanges)

    # make PBR ranking
    make_pbr_ranking(client, symbols, output_csv_filepath=config.output_pbr_ranking)


if __name__ == "__main__":
    logging.basicConfig(
        format='[%(asctime)s - %(name)s - %(levelname)s] %(message)s',
        level=config.log_level)

    run()
    # get_incomes()
    # get_net_assets()
    # pbr_ranking()
