# -*- coding:utf-8 -*-

from xignite_search.api.client import XigniteAPIClient
from typing import List


def divide_chunks(li, n):
    for i in range(0, len(li), n):
        yield li[i:i + n]

class Symbol:
    def __init__(self, code: str, name: str):
        self.code = code
        self.name = name


class NetAsset:
    def __init__(self, symbol: Symbol, net_asset: int):
        self.symbol = symbol
        self.net_asset = net_asset


class NetAssetCollector:
    """
    NetAssetCollector collects the net asset of specified symbols and a specified year
    """

    def __init__(self, api_client: XigniteAPIClient):
        self.api_client = api_client

    def get_net_assets(self, symbols: List[str], fiscal_year: int) -> List[NetAsset]:
        """
        get net assets of specified symbols and of a specified fiscal year
        """
        # get BalanceSheetHistory data
        all_histories = {}
        for c_symbols in divide_chunks(list(symbols), 100):
            histories = self.api_client.get_balance_sheet_history(c_symbols)
            # merge the result into all_histories
            dict.update(all_histories, histories)

        # List of NetAsset objects
        net_assets = []
        already_added_symbols = set([])
        for symbol in symbols:
            # get the net assets (in annual report) if it is included in the retrieved Balance Sheet Histories
            if symbol in all_histories:
                history = all_histories[symbol]
                for balance_sheet in history.balance_sheets:
                    if balance_sheet.fiscal_year == fiscal_year and balance_sheet.report_type == "Annual" and history.symbol not in already_added_symbols:
                        net_assets.append(
                            NetAsset(symbol=Symbol(code=history.symbol, name=history.name),
                                     net_asset=balance_sheet.net_assets * 1000000))
                        already_added_symbols.add(history.symbol)

        return net_assets

    def output_to_csv(self, filepath: str, net_assets: List[NetAsset]):
        with open(filepath, "w") as f:
            f.write("symbol,name,net_asset\n")
            for na in net_assets:
                f.write("{},\"{}\",{}\n".format(na.symbol.code, na.symbol.name, na.net_asset))
