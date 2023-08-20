import requests
from bs4 import BeautifulSoup
import json
import re
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from flask import Flask, jsonify


app = Flask(__name__)

def get_ether_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    script_tag = soup.find('script', {'id': 'fusion-metadata', 'type': 'application/javascript'})

    results = []

    if script_tag:
        script_content = script_tag.string
        matches = re.findall(r'"subheadlines":{.*?}', script_content)
        canonical_matches = re.findall(r'"canonical_url":\s*"(.*?)"', script_content)

        for match, canonical_match in zip(matches, canonical_matches):
            subheadlines_object = '{' + match + '}'
            try:
                subheadlines_dict = json.loads(subheadlines_object)
                basic_info = subheadlines_dict["subheadlines"]["basic"]
                canonical_url = "https://www.coindesk.com" + canonical_match
                article_content = get_article_content(canonical_url)
                results.append((basic_info, canonical_url, article_content))
            except json.JSONDecodeError as e:
                print(f"Expected Error: {e}")

    return results

def get_article_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    paragraphs = soup.find_all('p')
    content = " ".join([p.text for p in paragraphs])
    return content

def analyze_sentiment(results):
    # Use the NLTK library to initialize the sentiment analyzer
    sid = SentimentIntensityAnalyzer()
    analyzed_results = []

    for title, url, content in results:
        # Use the sentiment analyzer to analyze the sentiment of the content
        sentiment = sid.polarity_scores(content)

        # Determine if the news is positive or negative based on the compound sentiment score
        sentiment_result = "Positive" if sentiment['compound'] > 0 else "Negative" if sentiment['compound'] < 0 else "Neutral"

        analyzed_results.append({
            "Title": title,
            "URL": url,
            "Sentiment": sentiment_result
        })

    return analyzed_results


@app.route('/results', methods=['GET'])
def get_results():
    url = 'https://www.coindesk.com/tag/ether/'
    results = get_ether_info(url)
    analyzed_results = analyze_sentiment(results)
    return jsonify(analyzed_results)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="3000", debug=True)
