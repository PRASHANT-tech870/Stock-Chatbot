#this code fetches recent finance news articles for a specified company, filtering the results to only include articles published in the current month.

import requests
from datetime import datetime

# Directly use the API key
BING_SEARCH_API_KEY = '4afa25ed79684f25b46a85bfec16b453'
search_url = "https://api.bing.microsoft.com/v7.0/news/search"

def bing_search_news(company_name: str):
    headers = {"Ocp-Apim-Subscription-Key": BING_SEARCH_API_KEY}
    params  = {
        "q": f"{company_name} stock price and finance news",
        "mkt": "en-US",  # Search in English
        "textDecorations": True,
        "textFormat": "HTML",
        "freshness": "Month",
        "count": 100,
    }
    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()

    current_month = datetime.now().month
    current_year = datetime.now().year

    filtered_articles = []
    for article in search_results["value"]:
        # Adjust the date format
        date_str = article["datePublished"]
        # Trimming microseconds to six digits and replacing 'Z' with '+00:00'
        date_str = date_str[:-2] + date_str[-1].replace('Z', '+00:00')
        published_date = datetime.fromisoformat(date_str)
        if published_date.month == current_month and published_date.year == current_year:
            filtered_articles.append(article)

    return filtered_articles


