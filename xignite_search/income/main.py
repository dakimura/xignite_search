# -*- coding:utf-8 -*-

import datetime


def searchCompanies_PositiveIncome(api_client, symbols, target_period_in_year, net_csv_path, operating_csv_path):
    now = datetime.datetime.today()
    from_date = now - datetime.timedelta(days=(target_period_in_year * 365))

    # check if each symbol has positive net/operating income for this n years
    output_net = []
    output_operating = []
    for c_symbols in divide_chunks(symbols, 100):
        # call the API with a chunk of up to 100 symbols
        histories = api_client.get_income_statement_history(identifiers=c_symbols)

        for history in histories:
            if history.has_positive_net_income_from(from_date=from_date, type="net"):
                output_net.append((history.symbol, history.name))
            if history.has_positive_net_income_from(from_date=from_date, type="operating"):
                output_operating.append((history.symbol, history.name))

    # output the result to csv
    output_to_csv(net_csv_path, output_net)
    output_to_csv(operating_csv_path, output_operating)


def divide_chunks(li, n):
    for i in range(0, len(li), n):
        yield li[i:i + n]


def output_to_csv(filepath, arr):
    with open(filepath, "w") as f:
        for symbol in arr:
            f.write(symbol[0] + ",\"" + symbol[1] + "\"\n")
