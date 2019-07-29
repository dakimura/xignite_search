# -*- coding:utf-8 -*-

import datetime
import json
from json.decoder import JSONDecodeError
from logging import getLogger
from typing import List

import requests

from xignite_search.api import date_util
from xignite_search.income.income_statement import IncomeStatement
from xignite_search.income.income_statement_history import IncomeStatementHistory
from xignite_search.pbr.balance_sheet import BalanceSheet
from xignite_search.pbr.balance_sheet_history import BalanceSheetHistory

logger = getLogger(__name__)


# TODO: consider Accounting Standard pritories: ConsolidatedIFRS > ConsolidatedUS > ConsolidatedJP

class XigniteAPIClient:
    """
    Attributes:
        session (requests.Session): session to call Xignite API
    """

    def __init__(self, base_url, api_token, closed_days: List[datetime.date], session=None):
        self.base_url = base_url
        self.api_token = api_token
        self.closed_days = closed_days
        if session == None:
            self.session = requests.session()
        else:
            self.session = session  # type: requests.Session

    def list_symbols(self, exchange):
        """
        call ListSymbols API
        https://www.marketdata-cloud.quick-co.jp/Products/QUICKEquityRealTime/Overview/ListSymbols
        :param exchange: (ex. "XTKS", "XJAS" )
        :type exchange: string
        :return: an array of symbol strings (ex. ['1301', '1303', '1304'] )
        """
        symbols = []

        url = "{}/QUICKEquityRealTime.json/ListSymbols?Exchange={}&" \
            .format(self.base_url, exchange)

        headers = {"Content-Type": "application/x-www-form-urlencoded",
                   "_token": self.api_token}

        # call the endpoint
        resp = self.session.get(url, headers=headers)
        logger.debug("list symbols api. response=%s", str(resp.content))

        try:
            resp_parsed = json.loads(resp.content)
        except JSONDecodeError as err:
            raise XigniteAPIError("malformed API response is returned from Xignite.") from err

        if resp_parsed["Outcome"] != "Success":
            raise XigniteAPIError("'Outcome':'Success' is not returned from Xignite. response=" + str(resp.content))

        for security in resp_parsed["ArrayOfSecurityDescription"]:
            symbols.append(security["Symbol"])

        return symbols

    def get_income_statement_history(self, identifiers):
        """
        call GetIncomeStatementHistory API
        https://www.marketdata-cloud.quick-co.jp/Products/QUICKFinancialStatements/Overview/GetIncomeStatementHistory

        :param identifiers:
        :type identifiers: list of string

        :return: an array of IncomeStatementHistory objects. sorted by the
        :rtype: list of IncomeStatementHistory
        """
        if len(identifiers) > 100:
            raise XigniteAPIError("GetIncomeStatementHistoryAPI doesn't accept 101 or more identifiers")

        url = "{}/QUICKFinancialStatements.json/GetIncomeStatementHistory".format(self.base_url)
        url += "?IdentifierType=Symbol&_Language=Japanese"
        url += "&AccountingStandards=ConsolidatedIFRS,ConsolidatedUS,ConsolidatedJP,NonConsolidated"

        headers = {"Content-Type": "application/x-www-form-urlencoded",
                   "_token": self.api_token}
        data = {"Identifiers": ",".join(identifiers)}

        # call the endpoint
        resp = self.session.post(url, data=data, headers=headers)
        logger.debug("get income statement history api. response=%s", str(resp.content))

        try:
            resp_parsed = json.loads(resp.content)
        except JSONDecodeError as err:
            raise XigniteAPIError(
                "malformed API response is returned from GetIncomeStatementHistory. response=" + str(resp)) from err

        histories = []

        # ----- convert the API response to an array of IncomeStatementHistory -------
        # for each requested symbol
        for income_statement_equity_quote in resp_parsed["ArrayOfIncomeStatementEquityQuote"]:
            symbol = income_statement_equity_quote["Security"]["Symbol"]
            name = income_statement_equity_quote["Security"]["Name"]

            income_statements = []
            # for each income statement
            for income_statement in income_statement_equity_quote["ArrayOfIncomeStatement"]:
                # for each sales and income
                for sales_and_income in income_statement["ArrayOfSalesAndIncome"]:

                    # "forecast" is not necessary for our analysis
                    if sales_and_income["ResultOrForecast"] != "Result":
                        continue

                    # empty string is returned when the incomes are not open.
                    # ignore if the incomes are not open
                    if sales_and_income["NetIncome"] == "" or sales_and_income["OperatingIncome"] == "":
                        continue

                    year, month = income_statement["FiscalPeriodEnd"].split("/")

                    income_statement = IncomeStatement(
                        fiscal_period_end_year=int(year),
                        fiscal_period_end_month=int(month),
                        net_income=int(sales_and_income["NetIncome"]),
                        operating_income=int(sales_and_income["OperatingIncome"])
                    )

                    income_statements.append(income_statement)

            histories.append(IncomeStatementHistory(symbol=symbol, name=name, income_statements=income_statements))
        # ------------------------------------------------------------------------------

        return histories

    def get_balance_sheet_history(self, identifiers):
        """
        call GetBalanceSheetHistory API
        http://api.marketdata-cloud.quick-co.jp/QUICKFinancialStatements.json/GetBalanceSheetHistory

        :param identifiers:
        :type identifiers: list of string
        :rtype: Dict[str, BalanceSheetHistory]
        key = symbol
        """

        if len(identifiers) > 100:
            raise XigniteAPIError("GetBalanceSheetHistoryAPI doesn't accept 101 or more identifiers")

        url = "{}/QUICKFinancialStatements.json/GetBalanceSheetHistory".format(self.base_url)
        url += "?IdentifierType=Symbol&_Language=Japanese"
        url += "&AccountingStandards=ConsolidatedIFRS,ConsolidatedUS,ConsolidatedJP,NonConsolidated"

        headers = {"Content-Type": "application/x-www-form-urlencoded", "_token": self.api_token}
        data = {"Identifiers": ",".join(identifiers)}

        # call the endpoint
        resp = self.session.post(url, data=data, headers=headers)
        logger.debug("get balance sheet history api. response=%s", str(resp.content))

        try:
            resp_parsed = json.loads(resp.content)
        except JSONDecodeError as err:
            raise XigniteAPIError(
                "malformed API response is returned from GetBalanceSheetHistory. response=" + str(resp)) from err

        histories = {}

        # ----- convert the API response to an array of BalanceSheetHistory -------
        # for each requested symbol
        for bs_equity_quote in resp_parsed["ArrayOfBalanceSheetEquityQuote"]:  # bs = balance sheet

            # ignore symbols that don't have Balance Sheet.  (ex. "1484" "One ETF JPX/S&P")
            if bs_equity_quote["Outcome"] == "RequestError":
                logger.debug("the symbol doesn't have balance sheets. response=" + str(resp.content))
                continue

            symbol = bs_equity_quote["Security"]["Symbol"]
            name = bs_equity_quote["Security"]["Name"]

            bs_array = []
            # for each income statement
            for bs in bs_equity_quote["ArrayOfBalanceSheetStatement"]:
                # empty string is returned when the net assets are not open.
                # ignore if not open
                if bs["BalanceSheet"]["NetAssets"] == "":
                    continue

                year, month = bs["FiscalPeriodEnd"].split("/")

                bs = BalanceSheet(
                    fiscal_period_end_year=int(year),
                    fiscal_period_end_month=int(month),
                    net_assets=int(bs["BalanceSheet"]["NetAssets"])
                )

                bs_array.append(bs)

            histories[symbol] = BalanceSheetHistory(symbol=symbol, name=name, balance_sheets=bs_array)
        # --------------------------------------------------------------------------

        return histories

    def get_end_of_day_prices(self, identifiers):
        """
        call QUICKEquityHistorical.json/GetQuotes API and get end-of-day prices
        https://www.marketdata-cloud.quick-co.jp/Products/QUICKEquityHistorical/Overview/GetQuotes

        because an error is returned if a day that market is closed is sent as the AsOfDate query parameter,
        it is necessary to calculate the last market-open date with the config.closed_days

        :returns dictionary of {symbol : end_of_day_price} (ex. {"6501":4048, "7751":3217, ...}
        """
        url = "{}/QUICKEquityHistorical.json/GetQuotes".format(self.base_url)
        url += "?IdentifierType=Symbol&_Language=Japanese&AdjustmentMethod=All"
        url += "&AsOfDate={}".format(
            date_util.calc_last_open_date(datetime.date.today(), self.closed_days).strftime("%Y-%m-%d"))

        headers = {"Content-Type": "application/x-www-form-urlencoded", "_token": self.api_token}
        data = {"Identifiers": ",".join(identifiers)}

        # call the endpoint
        resp = self.session.post(url, data=data, headers=headers)
        logger.debug("get quotes api. response=%s", str(resp.content))

        try:
            resp_parsed = json.loads(resp.content)
        except JSONDecodeError as err:
            raise XigniteAPIError(
                "malformed API response is returned from QUICKEquityHistorical/GetQuotes API. response=" + str(resp)) from err

        if resp_parsed["ArrayOfHistoricalEquityQuote"][0]["Outcome"] != "Success":
            raise XigniteAPIError("'Outcome':'Success' is not returned from Xignite. response=" + str(resp.content))

        end_of_day_prices = {}
        for equity_quote in resp_parsed["ArrayOfHistoricalEquityQuote"]:
            symbol = equity_quote["Security"]["Symbol"]
            # equity_quote["EndOfDayQuote"]["Close"] is "0" if there was no trade in a day.
            # ExchangeOfficialClose returns the final price even in the case.
            end_of_day_prices[symbol] = float(equity_quote["EndOfDayQuote"]["ExchangeOfficialClose"])

        return end_of_day_prices


class XigniteAPIError(Exception):
    """ Xignite API Error"""
