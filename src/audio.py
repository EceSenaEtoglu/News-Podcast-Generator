import pycountry as pycountry
from article import Article
from gtts import gTTS
from translate import Translator
import os

class Audio:

    gtts_pause = "\n\n\n\n ."
    def __init__(self, articles: list, lang,str_intro,output_name):

        self._articles = articles
        self._lang = lang

        self.str_article_skip = 'Details are at '
        self.str_new_article = "Now we are heading to the next news"
        self.str_not_found = "Sorry, no news or articles were found"
        self.str_intro = str_intro

        self._outputname = output_name

        # if lang is not english, need to translate these
        if lang != "en":
            # TODO use google translate
            self._translator = Translator(to_lang=lang)
            self.str_article_skip = self._translator.translate(self.str_article_skip)
            self.str_new_article = self._translator.translate(self.str_new_article)
            self.str_not_found = self._translator.translate(self.str_not_found)
            self.str_intro = self._translator.translate(self.str_intro)

    @classmethod
    def from_country_code(cls,articles:list,country_code:str,intro:str,output_file_name:str):
        """create Audio object from ISO 3661 country_code instead of ISO 639-1 lang_code
        return none if country_code is not valid"""

        # Get the country object based on the ISO 3166 code
        country = pycountry.countries.get(alpha_2=country_code)

        if country:
            # Get the ISO 639-1 language code for the primary language spoken in the country
            language_code = country.languages[0].alpha_2 if country.languages else None
            if language_code:
                return cls(articles,language_code,intro,output_file_name)

        else:
            return None

        return None

    def _article_to_text(self, article: Article) -> str:

        """return text of article to audit, return empty text if both description and content is none"""

        text = ""
        title = article._title

        # get title
        for i in range(-1,-1*len(article._title)-1,-1):

            # hard coded API response
            # eliminate author from title blabla - X
            # PROBLEM: blabla -X -Y cannot be eliminated
            char = article._title[i]

            if char == '-':
                title = article._title[-1*len(article._title):i]
                break

        # add title to text

        text += title + f"{Audio.gtts_pause}"


        if article._description is not None:
            text += article._description

        elif article._content is not None:
            text += article._content

        # response given by the API is problematic
        # nor content nor description is provided
        # for now just get the title
        # TODO scrape from url
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

        text += "\n" + self.str_article_skip + source + f"{Audio.gtts_pause}" * 2
        return text

    def create_audio(self):
        """convert given articles to audio. Call get_audio_path after this to get path"""

        tts = gTTS(text=self.str_not_found, lang=self._lang, tld="com")

        # if no article is found
        if len(self._articles) == 0:
            tts.save("audio.mp3")
            return

        text_articles = self.str_intro

        for id, article in enumerate(self._articles):
            text_article = self._article_to_text(article)

            if len(text_article) != 0:
                text_articles += Audio.gtts_pause + text_article

                # if upcoming article exists, add string_new_article text
                if id != len(self._articles) - 1:
                    text_articles += self.str_new_article + Audio.gtts_pause

        tts.text = text_articles
        tts.save(self._outputname)

    def get_audio_path(self) -> str:
        """return path of created audio. Call after creating audio"""
        return os.getcwd()+self._outputname