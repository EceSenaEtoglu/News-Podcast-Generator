from src.api import *
from src.config import*
from src.audio import Audio


if __name__ == '__main__':


    news_api = Api(NEWS_API_KEY)
    intro_str = f"Latest news in US"

    try :
        articles = news_api.get_top_headlines("US")
    except InvalidInputError as e:
        print(e.message)

    else:
        audio = Audio(articles[:10], "en", "intro_str")
        audio.create_audio()










