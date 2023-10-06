from article import Article
from gtts import gTTS
from translate import Translator


class Audio:
    def __init__(self, articles: list, lang):
        self._articles = articles
        self._lang = lang

        self.string_article_skip = '\nDetails are at '
        self.string_new_article = "\nNow we are heading to the next article......\n"

        # if lang is not english, need to translate these
        if lang != "en":
            # TODO use google translate
            self._translator = Translator(to_lang=lang)
            self.string_article_skip = self._translator.translate(self.string_article_skip)
            self.string_new_article = self._translator.translate(self.string_new_article)

    def _article_to_text(self, article: Article) -> str:

        """get text of article to audit"""

        # TODO eliminate author from title (in form - X)
        text = article._title
        text += ".\n"

        if article._description is not None:
            text += article._description

        # TODO scrape from URL
        else:
            pass

        # hard coded API response
        # if article.source.name is not Google News,
        # the source is article.source.name (see https://newsapi.org/s/us-news-api)

        if article._source is not None and article._source["name"] != "Google News":
            source = article._source["name"]

        # else author is the source
        else:
            source = article._author

        text += self.string_article_skip + source
        return text

    def create_audio(self):
        """convert given articles to audio"""

        tts = gTTS(text="Sorry, no news or articles were found", lang=self._lang,tld="com")
        # for debuggin
        self.DB_text_articles = ""

        for id, article in enumerate(self._articles):
            text_article = self._article_to_text(article)
            self.DB_text_articles+= text_article

            # if upcoming article exists, add string_new_article text
            if id != len(self._articles) - 1:
                self.DB_text_articles += self.string_new_article

        # if article(s) found
        if len(self.DB_text_articles) != 0:
            tts.text = self.DB_text_articles

        tts.save("audio.mp3")
