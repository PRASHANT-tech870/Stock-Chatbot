import pandas as pd
from fuzzywuzzy import process  # fuzzywuzzy is used for string matching

# Load the CSV file into a DataFrame
tickers_and_names = pd.read_csv('tickers_and_names.csv')

def find_similar_names_and_tickers(query, threshold=80):
    # Find matches above a certain score threshold
    results = process.extractBests(query, tickers_and_names["Name"], score_cutoff=threshold)

    # Retrieve both name and ticker for each match
    matched_pairs = []
    for result in results:
        matched_name = result[0]
        matched_index = tickers_and_names[tickers_and_names["Name"] == matched_name].index[0]
        matched_ticker = tickers_and_names.loc[matched_index, "Ticker"]
        matched_pairs.append((matched_name, matched_ticker))

    return matched_pairs


