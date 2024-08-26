
from abc import ABC, abstractmethod
import json


class genericScraper:
    @abstractmethod
    def scrape(self, run_only_on_latest_chart = True):
        pass


def get_alpha3_coutry_code(alpha2_cc):
    file_name = "country_codes.json"
    file_data = open(file_name, "r")
    country_codes = json.load(file_data)
    if alpha2_cc in country_codes:
        return country_codes[alpha2_cc]
    else: 
        return None