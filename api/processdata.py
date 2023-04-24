import requests
import os
import json


def scrape_data():

    qry_url=f'{os.environ.get("STOCK_URL")}?function=CURRENCY_EXCHANGE_RATE&from_currency=BTC&to_currency=USD&apikey={os.environ.get("API_KEY")}'
    response = requests.request("GET", qry_url)
    respdata = response.json()
    rate = respdata['Realtime Currency Exchange Rate']['5. Exchange Rate']
    float_rate="{:.2f}".format(float(rate))
    return float_rate