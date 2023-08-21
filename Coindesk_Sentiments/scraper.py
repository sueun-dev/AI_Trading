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