# xignite_search
search companies under specific conditions using Quick Xignite API

## Python version
tested by python3.7

## Usage
```bash
# build a docker image
$ make build

# run 
$ docker run --env XIGNITE_API_TOKEN="your API token to call Xignite API goes here" --mount type=bind,src=$(pwd),dst=/tmp/output dakimura/xignite_search
```
Then, the following files will be output on the current directory:
- positive_net_income.csv

A list of stock symbols which net income is positive for this 5 consecutive years

- positive_operating_income.csv

A list of stock symbols which operating income is positive for this 5 consecutive years

- pbr_ranking.csv

Price-BookValue-Ratio ranking

Tokyo Stock Market and JASDAQ are the target markets for all the files above.

- net_assets.csv

Net Asset of the target symbols and in the year of `net_asset_target_year` config param
