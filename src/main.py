from src.api import Api
from src.config import*
from src.articles_to_audio import Audio


if __name__ == '__main__':
    news_api = Api(NEWS_API_KEY)
    intro_str = f"Latest news in Turkey about technology"
    articles = news_api.get_top_headlines("tr","technology")


    audio = Audio(articles[:10],"tr",intro_str)
    audio.create_audio()






