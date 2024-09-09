import json
import datetime
import os

def get_alpha3_coutry_code(alpha2_cc):
    """Given a 2-letter country code returns the corresponding 3-letter country code by looking it up in the 'country_code.json' file."""
    file_path = os.path.split(os.path.realpath(__file__))[0]
    file_name = file_path + '/country_code.json'
    file_data = open(file_name, "r")
    country_codes = json.load(file_data)
    if alpha2_cc in country_codes:
        return country_codes[alpha2_cc]
    else: 
        return None
    
def get_country_code(country):
    """
    Returns the 3-letter country code. If 'country' is 'global', it returns 'GBL'.
    If 'country' is a 2-letter country code, it returns the corresponding 3-letter country code.
    """
    if country == "global":
        return "GBL"
    else:
        return get_alpha3_coutry_code(country)
    
def get_chart_type(timing):
    """Determines the type of chart based on the timing."""
    if timing == "WEEKLY":
        return "Weekly"
    else:
        return "Daily"
    
def get_today_date():
    """Returns today's date in the format 'YYYY-MM-DD'."""
    today =  datetime.datetime.now().date()
    formatted_date = today.strftime("%Y-%m-%d")
    return formatted_date
