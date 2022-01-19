import pprint
from datetime import date
import json
import requests
from twilio.rest import Client



STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
STOCK_API_KEY = "3TPTZYJ7XAXVS8M3"
NEWS_API_KEY = "314e72fdfd2d407faa2527e153f36e96"
TWILIO_SID = "ACa889ca6fa3d18a9a1a304e6868e52997"
TWILIO_AUTH_TOKEN = "6c5d784f3f59b996a69aff87d5f10b8e"


    ## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").


stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY
}

response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]

yesterday = float(data_list[0]["4. close"])


day_before = float(data_list[1]["4. close"])


difference = abs(yesterday - day_before)

percentage_difference = ((yesterday - day_before)/abs(day_before))*100


if True:
    url = ('https://newsapi.org/v2/everything?'
           'q=Tesla&'
           f'from={date.today().__str__()}&'
           'sortBy=popularity&'
           'apiKey=314e72fdfd2d407faa2527e153f36e96')
    NEWS_RESPONSE = requests.get(url).json()["articles"]

    with open("data.txt", "w") as file:
        pprint.pprint(NEWS_RESPONSE, file)

    first_tree_articles =NEWS_RESPONSE[:3]

    list_top_articles = [f"brief: {article['title']}\n url: {article['url']}" for article in first_tree_articles]

    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    for article in list_top_articles:
        message = client.messages.create(
            body=article,
            from_="+19377350301",
            to="+3546188164"
        )

"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

