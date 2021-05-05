import numpy as np
import pandas as pd
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

import matplotlib.pyplot as plt
import seaborn as sns
from time import sleep

## Command to install all dependancies => pip install -r requirements.txt
## Command to run the server => uvicorn --port 5000 --host 127.0.0.1 main:app --reload



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def CoinBase_Api():
  url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
  parameters = {
    'start':'1',
    'limit':'5000',
    'convert':'USD'
  }
  headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': 'c0aba75e-3c73-4c52-964b-65275ad6ed0b',
  }

  session = Session()
  session.headers.update(headers)

  try:
    response = session.get(url, params=parameters)
    data = json.loads(response.text)
    return data
  except (ConnectionError, Timeout, TooManyRedirects) as e:
    return e

def parseCrypto(data):
  result = []
  for i in data['data']:
    result.append({'Name':i['name'],'Symbol':i['symbol'],
                   'Price':i['quote']['USD']['price'],
                   'percent_change_1h':i['quote']['USD']['percent_change_1h'],
                   'percent_change_24h':i['quote']['USD']['percent_change_24h'],
                   'percent_change_7d':i['quote']['USD']['percent_change_7d'],
                   'percent_change_30d':i['quote']['USD']['percent_change_30d'],
                   'volume_24':i['quote']['USD']['volume_24h']})
  return pd.DataFrame(result)


@app.get("/")
def Alerts():
  data = CoinBase_Api()
  # Stroring the retrieved data in a dataFrame 
  crypto_data = parseCrypto(data)
  # Check if there exists a database where percent change in last 24h is higher than 100
  top = crypto_data[crypto_data['percent_change_24h']>500]
  Name_list = top["Name"].tolist()

  return Name_list




