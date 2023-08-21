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