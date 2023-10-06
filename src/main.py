from src.api import Api
from src.config import*


if __name__ == '__main__':

    news_api = Api(NEWS_API_KEY)
    articles = news_api.get_top_headlines("tr")
    print(articles)





