#from requests import Request, Session
#from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import requests
#import json

apikey = 'b6a8f90f-c980-429a-bdf9-54f3a1b7662a'



headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': apikey
}
params = {
  'start':'1',
  'limit':'5',
  'convert':'USD'
}
url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

json = requests.get(url, params=params, headers=headers).json()

#coin = json['data']
#for x in coin:
    #print(x['id'], x['symbol'], x['quote']['USD']['price'])
print(json)
