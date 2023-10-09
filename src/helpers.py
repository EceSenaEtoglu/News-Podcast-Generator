import iso3166


def ISO_1366_countries():
    """return ISO_1366 countries """
    return iso3166.countries


def is_ISO_3166_country_code(country_code:str):
    pass

def is_ISO_639_lang_code(lang_code:str):
    pass

def get_ISO639_code_from_ISO_1366(country_code:str) -> str:
    """return ISO 639-1 code (language code) from country code """
