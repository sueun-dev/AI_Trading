"""
-------------------------------------------------------------------------------
Copyright (c) 2023, Sueun Cho

Project: AI Auto Trading
Version: v1.0.0 (Development)
Date: August 21, 2023
File name: scraper.py
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

import requests
from bs4 import BeautifulSoup
import json
import re
import logging
from concurrent.futures import ThreadPoolExecutor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_ether_info(url: str):
    with requests.Session() as session:
        response = session.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        script_tag = soup.find('script', {'id': 'fusion-metadata', 'type': 'application/javascript'})

        results = []

        if script_tag:
            script_content = script_tag.string
            matches = re.findall(r'"subheadlines":{.*?}', script_content)
            canonical_matches = re.findall(r'"canonical_url":\s*"(.*?)"', script_content)

            # Filter out URLs containing "static"
            canonical_matches = [match for match in canonical_matches if 'static' not in match]

            with ThreadPoolExecutor() as executor:
                urls = ["https://www.coindesk.com" + canonical_match for canonical_match in canonical_matches]
                # print(urls) 가져오는 주소 모두 출력
                articles_content = executor.map(get_article_content, urls)

                for match, canonical_url, article_content in zip(matches, urls, articles_content):
                    subheadlines_object = '{' + match + '}'
                    try:
                        subheadlines_dict = json.loads(subheadlines_object)
                        basic_info = subheadlines_dict["subheadlines"]["basic"]
                        results.append((basic_info, canonical_url, article_content))
                    except json.JSONDecodeError as e:
                        logger.error(f"Error decoding JSON for URL {canonical_url}: {e}")

        return results


def get_article_content(url: str) -> str:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    paragraphs = soup.find_all('p')
    content = " ".join([p.text for p in paragraphs])
    return content