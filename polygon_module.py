from dotenv import load_dotenv
import requests
import os

load_dotenv() 

POLYGON_API_KEY = '6o_Lp1wx5AlDHYD5uGwB1GIdvsH6b2bV'

# Monthly Stock Price History Data
def get_stock_price_history(ticker: str, start_date: str, end_date: str):
  # Polygon.io API URL for AAPL stock data
  url = f'https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/month/{start_date}/{end_date}?apiKey={POLYGON_API_KEY}'

  # Make the GET request
  response = requests.get(url)

  # Check if the request was successful
  if response.status_code == 200:
      # Parse the JSON data
      data = response.json()
      return [result['vw'] for result in data['results']]
  else:
      print(f'Failed to retrieve data: {response.status_code}')


'''
helps find companies with names similar to the user's input and returns their corresponding stock tickers. 
It's useful for cases where the user might not know the exact name of the company but wants to find related stocks.

'''