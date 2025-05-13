#!/bin/zsh

curl -X 'GET' \
  'https://api.doge.gov/savings/contracts?sort_by=date&sort_order=asc&page=1&per_page=500' \
  -H 'accept: application/json' > savings_contracts_page_1.json

./src/main.py

