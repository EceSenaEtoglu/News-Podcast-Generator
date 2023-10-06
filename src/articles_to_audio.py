from article import Article
from gtts import gTTS
from translate import Translator
class Audio():


    def __init__(self,articles:list,lang):
        self._articles = articles
        self._lang = lang

        self.string_article_skip = 'Details are at'
        self.string_new_article = "Now we are heading to the next article.."

        # if lang is not english, need to translate these
        if lang != "en":

            # TODO use google translate
            self._translator = Translator(to_lang = lang)
            self.string_article_skip = self._translator.translate(self.string_article_skip)
            self.string_new_article = self._translator.translate(self.string_new_article)



    def _article_to_text(self,article:Article) -> str:

        # TODO eliminate author
        text = article._title
        text += "..."

        if article._description != None:
            text += article._description

        # TODO scrape from URL
        else:
            pass

        # hard coded API response
        # if article.source.name is not Google News, the source is article.source.name (see https://newsapi.org/s/us-news-api)
        if article._source != None and article._source["name"] != "Google News":
            source = article._source["name"]

        # else author is the source
        else:
            source = article._author


        text += self.string_article_skip + source + self.string_new_article
        return text

    def audit_article(self,article_text:str):

        tts = gTTS(self._article_to_text(article_text,self._lang))
        tts.save("audio.mp3")
