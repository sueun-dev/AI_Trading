"""
-------------------------------------------------------------------------------
Copyright (c) 2023, Sueun Cho

Project: AI Auto Trading
Version: v1.0.0 (Development)
Date: August 21, 2023
File name: app.py

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

from flask import Flask, jsonify
from scraper import get_ether_info
from analyzer import analyze_sentiment

app = Flask(__name__)

@app.route('/results', methods=['GET'])
def get_results():
    url = 'https://www.coindesk.com/tag/ether/'
    results = get_ether_info(url)
    analyzed_results = analyze_sentiment(results)

    # 각각의 감정을 세기
    sentiment_counts = {"Positive": 0, "Negative": 0, "Neutral": 0}
    for result in analyzed_results:
        sentiment_counts[result["Sentiment"]] += 1

    total_results = len(analyzed_results)
    # 감정 비율 계산
    sentiment_percentages = {key: (value / total_results) * 100 for key, value in sentiment_counts.items()}

    # 가장 높은 확률을 가진 감정 찾기
    max_sentiment = max(sentiment_percentages, key=sentiment_percentages.get)

    return jsonify({
        "results": analyzed_results,
        "percentages": sentiment_percentages,
        "most_probable_sentiment": max_sentiment
    })

if __name__ == '__main__':
    app.run(host= "0.0.0.0", port="3000", debug=True)