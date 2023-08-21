"""
-------------------------------------------------------------------------------
Copyright (c) 2023, Sueun Cho

Project: AI Auto Trading
Version: v1.0.0 (Development)
Date: August 21, 2023
File name: analyzer.py

All rights reserved.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
-------------------------------------------------------------------------------
"""

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
