from fastapi import FastAPI, Response
from fastapi.responses import PlainTextResponse, JSONResponse
import uvicorn
from dotenv import load_dotenv
import os
import requests
import json
from prometheus_client import Gauge, CollectorRegistry, generate_latest
from datetime import date
import redis

load_dotenv()

def scrape_data():
    qry_url = f'{os.environ.get("STOCK_URL")}?function=CURRENCY_EXCHANGE_RATE&from_currency=BTC&to_currency=USD&apikey={os.environ.get("API_KEY")}'
    response = requests.request("GET", qry_url)
    respdata = response.json()
    rate = respdata['Realtime Currency Exchange Rate']['5. Exchange Rate']
    float_rate = "{:.2f}".format(float(rate))
    return float_rate

registry = CollectorRegistry()
exchange_rate_btc_usd = Gauge('exchange_rate_btc_usd', 'Exchange rate between BTC and USD', registry=registry)

app = FastAPI()

@app.get("/", response_class=JSONResponse)
async def root():
    return {"message": "Hello World"}

@app.get("/exchangemetrics", response_class=PlainTextResponse)
async def get_exchange_metrics():
    r = redis.Redis(host="redis", port=os.environ.get('REDIS_PORT'), password=os.environ.get('REDIS_PASSWORD'), db=0)
    scraped_data = 0.0
    try:
        todays_date = str(date.today())
        redis_key = f'exchange_rate-{todays_date}'
        tmpdata = r.get(redis_key)
        scraped_data = tmpdata.decode("utf-8")
        exchange_rate_btc_usd.set(float(scraped_data))
    except Exception as e:
        print(e)
        print('responding default value')
    return Response(generate_latest(registry), media_type="text/plain")


@app.get("/getexchangedata", response_class=PlainTextResponse)
async def get_exchange_data():
    r = redis.Redis(host="redis", port=os.environ.get('REDIS_PORT'), password=os.environ.get('REDIS_PASSWORD'), db=0)
    scraped_data = 0.0
    respdata = "error"
    try:
        scraped_data = scrape_data()
        todays_date = str(date.today())
        r.set(f'exchange_rate-{todays_date}', scraped_data)
        respdata = "done"
    except Exception as e:
        print(e)
        print('responding default value')
        todays_date = str(date.today())
        r.set(f'exchange_rate-{todays_date}', scraped_data)
    return respdata

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)

