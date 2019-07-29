# -*- coding:utf-8 -*-

from logging import getLogger

from xignite_search.income.income_statement import IncomeStatement

logger = getLogger(__name__)


class IncomeStatementHistory:
    """
    Attributes:
        income_statements (list of IncomeStatement): an array of income statements
    """

    def __init__(self, symbol: str, name: str, income_statements: list):
        self.symbol = symbol
        self.name = name
        self.income_statements = income_statements

    def has_positive_net_income_from(self, from_date, type):
        """
        check if the symbol has positive net income for n consecutive years
        :param type: "net" or "operating". The type of income to analyze.
        :param now_datetime
        :return: true if the company of this symbol has positive incomes for this n consecutive years
        """
        if type not in ["net", "operating"]:
            raise ValueError("type should be 'net' or 'operating'")

        target_statement_num = 0
        for statement in self.income_statements:
            if not statement.is_after(from_date):
                continue

            target_statement_num += 1
            if type == "net":
                if statement.net_income < 0:
                    logger.debug(
                        "{}: {}-{} net income is negative".format(self.name, statement.fiscal_period_end_year,
                                                                  statement.fiscal_period_end_month))
                    return False
            else:  # "operating"
                if statement.operating_income < 0:
                    logger.debug(
                        "{}: {}-{} operating income is negative".format(self.name, statement.fiscal_period_end_year,
                                                                        statement.fiscal_period_end_month))
                    return False

        # at least 1 statement should be analyzed
        if target_statement_num == 0:
            logger.debug("{}: no income statement is found".format(self.name))
            return False

        return True
