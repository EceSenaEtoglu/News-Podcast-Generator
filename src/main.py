from src import articles_to_audio
from src.api import Api
from src.config import*
from src.articles_to_audio import Audio


if __name__ == '__main__':

    news_api = Api(NEWS_API_KEY)
    articles = news_api.get_top_headlines("us")


    audio = Audio(articles[0:2],"en")
    audio.create_audio()
    print(audio.DB_text_articles)

    audio.create_audio()







