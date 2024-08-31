import musicbrainzngs as mbz 
import os
import json

def get_alpha3_coutry_code(alpha2_cc):
    file_path = os.path.split(os.path.realpath(__file__))[0]
    file_name = file_path + '/country_code.json'
    file_data = open(file_name, "r")
    country_codes = json.load(file_data)
    if alpha2_cc in country_codes:
        return country_codes[alpha2_cc]
    else: 
        return None

def mb_get_gender_and_country(artist_name):
    mbz.set_useragent('TheRecordIndustry.io', '0.1')
    search_result = mbz.search_artists(query=artist_name)
    artist_list = search_result.get('artist-list', [])
    
    if not artist_list:
        return "No results found", None
    
    artist = artist_list[0]
    
    gender = artist.get("gender", "unknown")
    country = artist.get("country", "unknown").lower()
    new_country_code = get_alpha3_coutry_code(country)
    
    if gender == "unknown":
        return "group", new_country_code
    else:
        return gender, new_country_code