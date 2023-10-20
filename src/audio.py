from datetime import date

from article import Article
from gtts import gTTS
from translate import Translator
import helpers


class Audio:
    # gTTS library adds stops for these chars
    # use in between news to add a break
    gTTS_pause = "\n\n\n\n. "

    # add to appropriate places to eliminate the chance of stop in between sentences
    gTTS_break_token = ". "

    def __init__(self, articles: list, lang, str_intro, output_name):

        print(len(articles))

        """create audio object from ISO 361-1 lang code"""

        self._articles = articles
        self._lang = lang

        self.str_date_today = date.today().strftime('%B %d, %Y')  # Format the date as a readable string

        self.str_article_skip = 'Details are at '
        self.str_new_article = "Now we are heading to the next news."
        self.str_not_found = "Sorry, no news or articles were found."
        self.str_news_end = "These were the news."
        self.str_unkown_source = "Sorry, no source were found."
        self.str_news_end = "We've come to the end, thank you for listening."

        self.str_intro = str_intro

        self.OUTPUT_NAME = output_name

        # if lang is not english, need to translate these
        if lang != "en":
            self._translator = Translator(to_lang=lang)
            self.str_article_skip = self._translator.translate(self.str_article_skip)
            self.str_new_article = self._translator.translate(self.str_new_article)
            self.str_not_found = self._translator.translate(self.str_not_found)
            self.str_intro = self._translator.translate(self.str_intro)
            self.str_date_today = self._translator.translate(self.str_date_today)
            self.str_unkown_source = self._translator.translate(self.str_unkown_source)
            self.str_news_end = self._translator.translate(self.str_news_end)

    @classmethod
    def from_country_code(cls, articles: list, country_code: str, intro: str, output_file_name: str):
        """create Audio object from ISO 3661 country_code"""

        language_code = helpers.get_ISO639_code_from_ISO_1366(country_code)
        return cls(articles, language_code, intro, output_file_name)

    def _article_to_text(self, article: Article) -> str:
        """return text of article to audit, return empty text if both description and content is none"""

        text = ""
        title = article._title

        # add title to text
        text += title + f"{Audio.gTTS_pause}"

        if article._description is not None:
            text += article._description

        elif article._content is not None:
            text += article._content

        # response given by the API is problematic
        # nor content nor description is provided
        # for now just get the title
        else:
            pass

        # set the source
        source = article._source_to_audit if article._source_to_audit else self.str_unkown_source

        # pause is to create stop in between news
        # token is to eliminate the chance of stops in between sentences
        text += Audio.gTTS_break_token + self.str_article_skip + Audio.gTTS_break_token + source + f"{Audio.gTTS_pause}" * 2
        return text

    def create_audio(self):
        """create audio from provided articles"""

        tts = gTTS(text=self.str_not_found, lang=self._lang, tld="com")

        # if no article is found
        if len(self._articles) == 0:
            tts.save(self.OUTPUT_NAME)
            return

        text_articles = self.str_date_today + Audio.gTTS_pause + self.str_intro

        for id, article in enumerate(self._articles):
            text_article = self._article_to_text(article)

            if len(text_article) != 0:
                text_articles += Audio.gTTS_pause + text_article

                # if upcoming article exists, add string_new_article text
                if id != len(self._articles) - 1:
                    text_articles += self.str_new_article + Audio.gTTS_pause + Audio.gTTS_break_token

                # add ending text
                else:
                    text_articles += Audio.gTTS_pause + self.str_news_end

        tts.text = text_articles
        tts.save(self.OUTPUT_NAME)
