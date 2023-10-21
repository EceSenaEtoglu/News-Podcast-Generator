import iso3166

# keys: countries supported by the API values: their official lang in ISO 639-1 format
country_to_lang= {'ae': 'ar', 'ar': 'es', 'at': 'de', 'au': 'en', 'be': 'nl', 'bg': 'bg', 'br': 'pt', 'ca': 'en', 'ch': 'de', 'cn': 'zh', 'co': 'es', 'cu': 'es',
'cz':'cs','de':'de','eg':'ar','fr':'fr','gb':'en','gr':'el','hk':'zh','hu':'hu','id':'id','ie':'en','il':'he','in':'hi',
'it':'it','jp':'ja','kr':'ko','lt':'lt','lv':'lv','ma':'ar','mx':'es','my':'ms','ng':'en','nl':'nl','no':'no','nz':'en',
'ph':'en','pl':'pl','pt':'pt','ro':'ro','rs':'sr','ru':'ru','sa':'ar','se':'sv','sg':'en','si':'sl','sk':'sk','th':'th',
'tr':'tr','tw':'zh','ua':'uk','us':'en','ve':'es','za':'af'}

def get_country_name(country_code: str):
    return iso3166.countries[country_code].name


def is_a_supported_country_code(country_code: str):
    return country_code in country_to_lang and len(country_code) == 2


def get_ISO639_code_from_ISO_1366(country_code: str):
    """return ISO 639-1 code (language code) from country code """
    # couldn't find conversion via a package, used a dict
    if country_code.lower() in country_to_lang:
        return country_to_lang.get(country_code.lower())
