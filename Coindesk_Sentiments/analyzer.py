from nltk.sentiment.vader import SentimentIntensityAnalyzer
from concurrent.futures import ThreadPoolExecutor

# Initialize the SentimentIntensityAnalyzer outside the function
sid = SentimentIntensityAnalyzer()

def analyze_single_result(result):
    title, url, content = result
    sentiment = sid.polarity_scores(content)
    sentiment_result = "Positive" if sentiment['compound'] > 0 else "Negative" if sentiment['compound'] < 0 else "Neutral"
    return {
        "Title": title,
        "URL": url,
        "Sentiment": sentiment_result
    }

def analyze_sentiment(results):
    analyzed_results = []

    # Use ThreadPoolExecutor for parallel processing
    with ThreadPoolExecutor() as executor:
        analyzed_results = list(executor.map(analyze_single_result, results))

    return analyzed_results
