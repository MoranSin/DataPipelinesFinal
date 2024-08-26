
from abc import ABC, abstractmethod
import json
import datetime
import os

class genericScraper:
    @abstractmethod
    def scrape(self, run_only_on_latest_chart = True):
        pass

def get_alpha3_coutry_code(alpha2_cc):
    file_path = os.path.split(os.path.realpath(__file__))[0]
    file_name = file_path + '/country_code.json'
    file_data = open(file_name, "r")
    country_codes = json.load(file_data)
    if alpha2_cc in country_codes:
        return country_codes[alpha2_cc]
    else: 
        return None
    
def get_country_code(country):
    if country == "global":
        return "GBL"
    else:
        return get_alpha3_coutry_code(country)
    
def get_chart_type(timing):
    if timing == "WEEKLY":
        return "Weekly"
    else:
        return "Daily"
    
def get_today_date():
    today =  datetime.datetime.now().date()
    formatted_date = today.strftime("%Y-%m-%d")
    return formatted_date
