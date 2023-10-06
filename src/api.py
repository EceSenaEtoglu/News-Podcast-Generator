from multipledispatch import dispatch
from article import Article
import requests
import json


class Api():

    def __init__(self, api_key: str):
        self._api_key = api_key

    @staticmethod
    def _get_parsed_response(res_data: str):
        """return list of articles from parsing json data"""

        parsed_data = json.loads(res_data)
        articles_data = parsed_data.get("articles", [])

        articles = []

        # create list of article objects from article data
        for article_data in articles_data:
            article = Article(article_data)
            articles.append(article)

        return articles

    @dispatch(str, str)
    def get_top_headlines(self, country: str, category: str) -> list:
        "return top headlines for a category in country from country's news sources." \
        " Increasing order of publish time. E.g most recent headline is at the end"""

        url = f"https://newsapi.org/v2/top-headlines?country={country}&category={category}&apiKey={self._api_key}"
        res = requests.get(url)

        if res.status_code != 200:
            raise RuntimeError("Error fetching the headlines")

        return self._get_parsed_response(res.text)

    @dispatch(str)
    def get_top_headlines(self, country: str) -> list:
        """return top headlines for a country from country's news sources
        Increasing order of publish time. E.g most recent headline is at the end"""""

        url = f"https://newsapi.org/v2/top-headlines?country={country}&apiKey={self._api_key}"
        res = requests.get(url)

        if res.status_code != 200:
            raise RuntimeError("Error fetching the headlines")

        return self._get_parsed_response(res.text)
