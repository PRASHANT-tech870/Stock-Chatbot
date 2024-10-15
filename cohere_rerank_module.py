from dotenv import load_dotenv
import os
import cohere

load_dotenv()  # This loads the variables from .env

COHERE_API_KEY = 'XDA0U62spbzCWXfkXqFLvOr09PUU5bPjF2APVkgY'

co = cohere.Client(COHERE_API_KEY)

def rerank_search_results(company_name: str, search_results: list[str], top_n: int):
    query = f"Filter and prioritize news headlines explicitly discussing factors influencing {company_name}'s stock price, including market trends, financial reports, corporate announcements, and industry-specific news impacting {company_name}'s performance."
    results = co.rerank(model="rerank-english-v2.0", query=query, documents=search_results, top_n=top_n)
    return [result.document['text'] for result in results]


'''

This code is designed to filter and prioritize search results (e.g., news headlines) about a company, 
focusing specifically on information that might impact the company's stock price. 
The Cohere API's reranking feature helps reorder the search results according to their relevance to the query.

'''