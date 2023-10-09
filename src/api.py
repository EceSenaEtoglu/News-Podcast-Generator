from multipledispatch import dispatch
from article import Article
import requests
import json
import iso3166

class InvalidInputError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class Api:

    CATEGORIES = ["business","entertainment","general","health","science","sports","technology"]
    COUNTRIES = iso3166.countries

    def __init__(self, api_key: str):
        self._api_key = api_key

    @staticmethod
    def is_a_valid_country(country):
        """return if a country is valid for the API (in iso 3166 format)"""
        return country in iso3166.countries

    @staticmethod
    def _get_parsed_response(res_data: str):
        """return list of articles from parsing json data"""

        print(res_data)

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
        """Return top headlines in a category(api.CATEGORIES) for a country, from country's news sources

        Increasing order of publish time. E.g most recent headline is at the end

        Raise InvalidInputError if inputs are invalid."""

        # if country or category data is invalid
        # raise InvalidInputError
        if not (country in iso3166 and category in Api.CATEGORIES):
            raise InvalidInputError("Category or country data is invalid.")

        url = f"https://newsapi.org/v2/top-headlines?country={country}&category={category}&apiKey={self._api_key}"
        res = requests.get(url)

        if res.status_code != 200:
            raise RuntimeError("Error fetching the headlines")

        return self._get_parsed_response(res.text)

    @dispatch(str)
    def get_top_headlines(self, country: str) -> list:
        """Return top headlines for a country from country's news sources
        Increasing order of publish time. E.g most recent headline is at the end
        Raise InvalidInputError if inputs are invalid."""

        # if country or category data is invalid
        # raise InvalidInputError
        if country not in iso3166.countries:
            raise InvalidInputError("Country data is invalid.")

        url = f"https://newsapi.org/v2/top-headlines?country={country}&apiKey={self._api_key}"
        res = requests.get(url)

        if res.status_code != 200:
            raise RuntimeError("Error fetching the headlines")

        return self._get_parsed_response(res.text)