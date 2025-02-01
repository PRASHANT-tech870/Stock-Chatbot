import streamlit as st
from name_ticker_module import find_similar_names_and_tickers
from news_module import get_news
from polygon_module import get_stock_price_history
from calendar_module import get_first_last_days
# from cohere_rerank_module import rerank_search_results
from financial_bert_module import predict_monthly_stock_price_change_rate
import matplotlib.pyplot as plt

def rerank_search_results(name, articles_content, top_n):
    if not articles_content:
        st.warning("No articles found to rerank")
        return []
    
    # Filter out None values and empty strings
    valid_articles = [article for article in articles_content if article and isinstance(article, str)]
    
    if not valid_articles:
        st.warning("No valid articles found after filtering")
        return []
    
    st.write(f"Found {len(valid_articles)} valid articles to rerank")
    
    # Simple scoring based on article length and relevance to company name
    reranked_results = []
    for article in valid_articles:
        score = len(article)  # Simple scoring based on length
        if name.lower() in article.lower():
            score += 1000  # Boost articles containing company name
        reranked_results.append((article, score))
    
    reranked_results = sorted(reranked_results, key=lambda x: x[1], reverse=True)[:top_n]
    return [article for article, _ in reranked_results]

# Streamlit app layout
st.title('Stock Analysis and Prediction')

# Company Name Search
user_input = st.text_input("Enter a company name", "Tesla")
if user_input:
    search_results = find_similar_names_and_tickers(user_input)
    option = st.selectbox('Choose a company:', search_results)
    name, ticker = option

    calculate_button = st.button('Calculate')
    if calculate_button:
        this_month_articles = get_news(name)
        # Filter out None values when extracting descriptions
        articles_content = [article['description'] for article in this_month_articles if article.get('description')]
        
        # Debug print
        st.write(f"Number of articles with descriptions: {len(articles_content)}")
        
        reranked_articles_content = rerank_search_results(name, articles_content, 5)
        st.subheader("Cohere Reranked Articles:")
        for article in reranked_articles_content:
            st.write("-", article)

        concatenated_articles_content = " ".join(reranked_articles_content)
        monthly_stock_price_change_rate = predict_monthly_stock_price_change_rate(concatenated_articles_content)

        past_month_first_day_str, current_month_last_day_str, year_month_labels = get_first_last_days()
        stock_price_history = get_stock_price_history(ticker, past_month_first_day_str, current_month_last_day_str)

        if not stock_price_history:
            st.error("No stock price history found for the selected company.")
        elif monthly_stock_price_change_rate is None:
            st.error("Failed to predict the monthly stock price change rate.")
        else:
            # Debug prints
            st.write(f"Number of months in history: {len(year_month_labels)}")
            st.write(f"Number of price points: {len(stock_price_history)}")

            #calculation of next month
            predicted_next_month_stock_price = stock_price_history[-1] * (1 + monthly_stock_price_change_rate)
            stock_price_history.append(predicted_next_month_stock_price)
            
            # Ensure labels and prices have the same length
            if len(year_month_labels) < len(stock_price_history):
                year_month_labels.append("Next Month")
            
            # More debug prints
            st.write(f"Final lengths - Labels: {len(year_month_labels)}, Prices: {len(stock_price_history)}")

            # Display the predicted stock price
            st.subheader("Predicted Stock Price for Next Month:")
            st.write(f"The predicted stock price for next month is: ${predicted_next_month_stock_price:.2f}")

            # Plotting the data
            fig, ax = plt.subplots(figsize=(12, 6))  # Made figure wider to accommodate more months
            
            # Ensure we have all consecutive months
            all_months = year_month_labels.copy()
            if len(stock_price_history) > len(all_months):
                next_month = datetime.strptime(all_months[-1], '%Y-%m')
                if next_month.month == 12:
                    next_month = next_month.replace(year=next_month.year + 1, month=1)
                else:
                    next_month = next_month.replace(month=next_month.month + 1)
                all_months.append(next_month.strftime('%Y-%m'))
            
            # Plot historical data
            ax.plot(all_months[:-1], stock_price_history[:-1], label='Historical', marker='o', color='blue')
            # Plot prediction
            ax.plot(all_months[-2:], stock_price_history[-2:], label='Prediction', color='red', marker='o', linestyle='--')

            # Adjust x-axis for better readability
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()  # Adjust layout to prevent label cutoff

            # Adding labels and title
            ax.set_xlabel('Year-Month')
            ax.set_ylabel('Stock Price')
            ax.set_title('Stock Price History and Prediction')
            plt.xticks(rotation=45)

            # Adding legend
            ax.legend()

            # Show the plot in Streamlit
            st.pyplot(fig)
