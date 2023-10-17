import iso3166

countries = {"tr": "tr", "us": "en", "de": "de","es":"es","fr":"fr"}

def get_country_name(country_code: str):
    return iso3166.countries[country_code].name


def is_ALPHA2_ISO_3166_country_code(country_code: str):
    return country_code in iso3166.countries and len(country_code) == 2


def get_ISO639_code_from_ISO_1366(country_code: str):
    """return ISO 639-1 code (language code) from country code """
    # TODO find an automatic way to include all countries

    if country_code.lower() in countries:
        return countries.get(country_code.lower())
