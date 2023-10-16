from multipledispatch import dispatch
from article import Article
import requests
import json
import helpers

class InvalidInputError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class Api:

    #https://newsapi.org/

    CATEGORIES = ["business","entertainment","general","health","science","sports","technology"]

    # countries are all ISO 3166 countrys

    def __init__(self, api_key: str):
        self._api_key = api_key
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
    def get_top_headlines(self, country_code: str, category: str) -> list:
        """Return top headlines in a category(api.CATEGORIES) for a country, from country's news sources

        Increasing order of publish time. E.g most recent headline is at the end

        Raise InvalidInputError if inputs are invalid."""

        # if country or category data is invalid
        # raise InvalidInputError
        if not (helpers.is_ISO_3166_country_code(country_code) and category in Api.CATEGORIES):
            raise InvalidInputError("Category or country data is invalid.")

        url = f"https://newsapi.org/v2/top-headlines?country={country_code}&category={category}&apiKey={self._api_key}"
        res = requests.get(url)

        if res.status_code != 200:
            raise RuntimeError("Error fetching the headlines")

        return self._get_parsed_response(res.text)

    @dispatch(str)
    def get_top_headlines(self, country_code: str) -> list:
        """Return top headlines for a country from country's news sources
        Increasing order of publish time. E.g most recent headline is at the end
        Raise InvalidInputError if inputs are invalid."""

        # if country or category data is invalid
        # raise InvalidInputError
        if not helpers.is_ISO_3166_country_code(country_code):
            raise InvalidInputError("Country data is invalid.")

        url = f"https://newsapi.org/v2/top-headlines?country={country_code}&apiKey={self._api_key}"
        res = requests.get(url)

        if res.status_code != 200:
            raise RuntimeError("Error fetching the headlines")

        return self._get_parsed_response(res.text)