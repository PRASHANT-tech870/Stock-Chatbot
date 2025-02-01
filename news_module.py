
import requests
from datetime import datetime, timedelta
import streamlit as st

NEWS_API_KEY = '146e09e29ae041d2aa81649d75227e2f'  # Replace with your NewsAPI key
BASE_URL = 'https://newsapi.org/v2/everything'

def get_news(company_name: str):
    # Calculate date range for last 30 days
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    params = {
        'q': f'{company_name} stock',
        'from': start_date.strftime('%Y-%m-%d'),
        'to': end_date.strftime('%Y-%m-%d'),
        'language': 'en',
        'sortBy': 'relevancy',
        'apiKey': NEWS_API_KEY
    }
    
    try:
        st.write("Fetching news articles...")
        response = requests.get(BASE_URL, params=params)
        
        if response.status_code != 200:
            st.error(f"API request failed with status code: {response.status_code}")
            return []
            
        data = response.json()
        
        if data['status'] != 'ok':
            st.error("API request failed")
            return []
            
        articles = data['articles']
        st.write(f"Found {len(articles)} articles")
        
        # Convert to same format as before
        formatted_articles = []
        for article in articles[:100]:  # Limit to 100 articles
            formatted_articles.append({
                'description': article.get('description', ''),
                'datePublished': article.get('publishedAt', ''),
                'url': article.get('url', ''),
                'title': article.get('title', '')
            })
            
        return formatted_articles

    except Exception as e:
        st.error(f"Error fetching news: {str(e)}")
        return []