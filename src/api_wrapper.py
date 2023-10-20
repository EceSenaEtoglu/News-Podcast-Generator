from multipledispatch import dispatch
from article import Article
import requests
import helpers


class InvalidInputError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class Api:
    # https://newsapi.org/

    CATEGORIES = ["business", "entertainment", "general", "health", "science", "sports", "technology"]
    CONTENT_LENGTH_UPPER_BOUND = 30

    def __init__(self, api_key: str):
        self._api_key = api_key

    # old logic to trim the full article content such that returned content ends at a full sentence
    # and is of closest length to UPPER_BOUND

    # API does not return full content so can't be used via this API
    """"@staticmethod
    #def __trimming_logic(content,title,source,author):"""

    """""Trim full article content close to specified upper bound

        Trims the article at stopping by the closest "." to the upperbound
        Raise RuntimeError if can't be trimmed
        """"""

        # if article does not contain any "."
        #   message = f"Problem in trimming content \n "\
        #   f"Article {title} written by {author} from {source} does not contain any '.'" \
        #   f"Content {content}"
    
        #   raise RuntimeError(message)
    
        # get the approximate words
    
        if len(content) >= Api.CONTENT_LENGTH_UPPER_BOUND:
    
            for i in range(len(content)):
                if i >= Api.CONTENT_LENGTH_UPPER_BOUND and content[i] == '.':
                    break
    
        # this is not an expected case but still included it because not sure what could be the API's response
        # if full article content is less than the determined upper bound length
        # find nearest "." to the end
        else:
            for i in range(-1, -1 * len(content) - 1, -1):
                if content[i] == '.':
                    # convert i to positive index
                    i = len(content) + i
                    break
    
            # return content[:i+1]  # trimmed content
    
        return content[:i + 1]  # trimmed content"""

    @staticmethod
    def _trim_article_content(content: str):
        """clean char data from api response, return trimmed article

        if content is none return none"""

        if content:
            for id, char in enumerate(content):
                if char == '[':
                    break

            return content[:id]

    @staticmethod
    def _get_cleaned_source(source: dict, author: str) -> str:

        # if article source is none or Google News
        # author is the source

        # else
        # the source is article.source.name
        # (compare sources https://newsapi.org/s/us-news-api, https://newsapi.org/s/turkey-news-api)

        if source is None or source["name"] == "Google News":
            source = author

        else:
            source = source["name"]

        return source

    @staticmethod
    def _get_cleaned_title(title: str) -> str:
        """ Clean author from title
        blabla - X (clean "- X")

        PROBLEM: blabla -X -Y, -Y cannot be cleaned"""

        # get title
        for i in range(-1, -1 * len(title) - 1, -1):

            # hard coded API response
            # eliminate author from title blabla - X
            # PROBLEM: blabla -X -Y cannot be eliminated
            char = title[i]

            if char == '-':
                title = title[-1 * len(title):i]
                break
        return title
    @staticmethod
    def _get_cleaned_response(res):
        """Return list of articles from cleaning json data"""

        articles_data = res.json()

        articles_data = articles_data.get("articles")
        articles = []

        # create list of article objects from article data
        for article_data in articles_data:
            author = article_data["author"]
            title = Api._get_cleaned_title(article_data["title"])

            source = article_data["source"]
            url = article_data["url"]
            published_at = article_data["publishedAt"]

            source_to_audit = Api._get_cleaned_source(source, author)

            # short summary of content
            description = article_data["description"]

            trimmed_content = Api._trim_article_content(article_data["content"])
            article = Article(author, title, source, published_at, url, description, trimmed_content, source_to_audit)
            articles.append(article)

        articles_data.clear()

        return articles

    @dispatch(str, str)
    def get_top_headlines(self, country_code: str, category: str) -> list:
        """Return top headlines in a category(api.CATEGORIES) for a country, from country's news sources

        Increasing order of publish time. E.g most recent headline is at the end

        Raise InvalidInputError if inputs are invalid."""

        # if country or category data is invalid
        # raise InvalidInputError
        if not (helpers.is_a_supported_country_code(country_code) and category in Api.CATEGORIES):
            raise InvalidInputError("Category or country data is invalid.")

        url = f"https://newsapi.org/v2/top-headlines?country={country_code}&category={category}&apiKey={self._api_key}"
        res = requests.get(url)

        if res.status_code != 200:
            raise RuntimeError(f"Error fetching the headlines for {country_code} in {category}")


        return Api._get_cleaned_response(res)

    @dispatch(str)
    def get_top_headlines(self, country_code: str) -> list:
        """Return top headlines for a country from country's news sources
        Increasing order of publish time. E.g. most recent headline is at the end
        Raise InvalidInputError if inputs are invalid."""

        # if country or category data is invalid
        # raise InvalidInputError
        if not helpers.is_a_supported_country_code(country_code):
            raise InvalidInputError("Country data is invalid.")

        url = f"https://newsapi.org/v2/top-headlines?country={country_code}&apiKey={self._api_key}"
        res = requests.get(url)

        if res.status_code != 200:
            raise RuntimeError(f"Error fetching the headlines  for {country_code}")

        return Api._get_cleaned_response(res)