# xignite_search
search companies under specific conditions using Quick Xignite API

## Python version
3.5~

## Usage
- put config.py under the `xignite_search/conf` directory
- run `xignite_search/main.py`
  -- companies which net/operating income are positive in consecutive n years are output to a filepath specified by `number_of_issued_shares_csv` config param
  -- PBR ranking is output to stdout
