from multipledispatch import dispatch
from article import Article
import requests
import helpers

class InvalidInputError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class Api:

    #https://newsapi.org/

    CATEGORIES = ["business","entertainment","general","health","science","sports","technology"]
    CONTENT_LENGTH_UPPER_BOUND = 30

    def __init__(self, api_key: str):
        self._api_key = api_key

    @staticmethod
    def _trim_article_content(content,author,source,title):
        """Trim full article content close to specified upper bound

        Trims the article at stopping by the closest "." to the upperbound
        Raise RuntimeError if can't be trimmed
        """

        if content:

            # if article does not contain any "."
            if "." not in content:
                message = f"Problem in trimming content \n "\
                f"Article {title} written by {author} from {source} does not contain any '.'" \

                raise RuntimeError(message)

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

            return content[:i+1]  # trimmed content

    def _get_parsed_response(self,res):
        """return list of articles from parsing json data"""

        articles_data = res.json()

        articles_data = articles_data.get("articles")
        articles = []

        # create list of article objects from article data
        for article_data in articles_data:

            author = article_data["author"]
            title = article_data["title"]
            source = article_data["source"]
            url = article_data["url"]
            published_at = article_data["publishedAt"]

            # short summary of content
            description = article_data["description"]

            trimmed_content = Api._trim_article_content(article_data["content"],author,source,title)
            article = Article(author,title,source,published_at,url,description,trimmed_content)
            articles.append(article)

        return articles

    @dispatch(str, str)
    def get_top_headlines(self, country_code: str, category: str) -> list:
        """Return top headlines in a category(api.CATEGORIES) for a country, from country's news sources

        Increasing order of publish time. E.g most recent headline is at the end

        Raise InvalidInputError if inputs are invalid."""

        # if country or category data is invalid
        # raise InvalidInputError
        if not (helpers.is_ALPHA2_ISO_3166_country_code(country_code) and category in Api.CATEGORIES):
            raise InvalidInputError("Category or country data is invalid.")

        url = f"https://newsapi.org/v2/top-headlines?country={country_code}&category={category}&apiKey={self._api_key}"
        res = requests.get(url)

        if res.status_code != 200:
            raise RuntimeError(f"Error fetching the headlines for {country_code}")

        return self._get_parsed_response(res)

    @dispatch(str)
    def get_top_headlines(self, country_code: str) -> list:
        """Return top headlines for a country from country's news sources
        Increasing order of publish time. E.g most recent headline is at the end
        Raise InvalidInputError if inputs are invalid."""

        # if country or category data is invalid
        # raise InvalidInputError
        if not helpers.is_ALPHA2_ISO_3166_country_code(country_code):
            raise InvalidInputError("Country data is invalid.")

        url = f"https://newsapi.org/v2/top-headlines?country={country_code}&apiKey={self._api_key}"
        res = requests.get(url)

        if res.status_code != 200:
            raise RuntimeError(f"Error fetching the headlines  for {country_code}")

        return self._get_parsed_response(res)