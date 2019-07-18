# -*- coding:utf-8 -*-

from xignite_search.api.client import XigniteAPIClient
from typing import List, Dict


class Security:
    pbr: int

    def __init__(self, symbol: str = None, shares: int = None, net_asset: int = None, price: int = None):
        self.symbol = symbol
        self.shares = shares
        self.net_asset = net_asset
        self.price = price
        self.pbr = None


class SecurityManager:
    securities: Dict[str, Security]

    def __init__(self, api_client: XigniteAPIClient, symbols=None):
        """
        :param api_client:
        :param symbols:
        :type symbols: List[str]
        """
        self.api_client = api_client
        self.securities = {symbol: Security(symbol=symbol) for symbol in symbols}

    def fetch_shares(self, csv_file_path):
        self.create_from_csv(csv_file_path)

    def fetch_net_assets(self):
        # get BalanceSheetHistory data
        all_histories = {}
        for c_symbols in divide_chunks(list(self.securities.keys()), 100):
            histories = self.api_client.get_balance_sheet_history(c_symbols)
            # merge the result into all_histories
            dict.update(all_histories, histories)

        for symbol in self.securities.keys():
            # set the net assets if it is included in the retrieved Balance Sheet Histories
            if symbol in all_histories:
                # net asset unit in the balance sheet history is 1,000,000
                self.securities[symbol].net_asset = all_histories[symbol].balance_sheets[0].net_assets * 1000000

    def fetch_price(self):
        end_of_day_prices = self.api_client.get_end_of_day_prices(self.securities.keys())
        for symbol, security in self.securities.items():
            # set the prices if it is included in the retrieved Quotes
            if symbol in end_of_day_prices:
                security.price = end_of_day_prices[security.symbol]

    def create_from_csv(self, file_path):
        """
        the csv file is like
        ----
        security_code,number_of_shares2
        33230,67446500
        90830,6022414
        38080,9073214
        59280,10305259
        ...
        ----
        the first line is column names,
        and each security code has a trailing 0.
        :param file_path:
        :return: list of securities
        :rtype: list of Security
        """
        securities = []

        with open(file_path, "r") as f:
            # skip the first line (=column names)
            next(f)

            for line in f:
                security_code, num_shares = line.strip("\n").split(",")
                # omit the trailing 0
                symbol = security_code[:-1]
                num_shares = int(num_shares)

                if symbol in self.securities.keys():
                    self.securities[symbol].shares = num_shares

        return securities

    def compute_pbr(self):
        """
        PBR = price / ( net_assets / issued shares )
              株価 / (純資産 / 発行済み株式数)
        :param self:
        :return:
        """
        for symbol in self.securities.keys():
            if self.securities[symbol].net_asset is None:
                continue

            if self.securities[symbol].shares is None:
                continue

            self.securities[symbol].pbr = self.securities[symbol].price / (
                    self.securities[symbol].net_asset / float(self.securities[symbol].shares))

    def remove_no_pbr_symbols(self):
        for symbol in list(self.securities):
            if self.securities[symbol].pbr is None:
                del self.securities[symbol]

    def sort_by_pbr(self) -> List[Security]:
        return sorted(self.securities.values(), key=lambda security: security.pbr, reverse=True)


def divide_chunks(li, n):
    for i in range(0, len(li), n):
        yield li[i:i + n]
