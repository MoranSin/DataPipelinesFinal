import requests
import json
import sys
import os
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from genericScraper import get_chart_type, get_today_date, get_country_code

from os.path import join, dirname
from dotenv import load_dotenv
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
 
def convert_seconds(n):
    minutes, seconds = divmod(n, 60)
    return f"{minutes:02}:{seconds:02}"

class YoutubeScraper:
    def __init__(self, api_key, url_key, cookie):
        self.api_key = api_key
        self.base_url = f"https://charts.youtube.com/youtubei/v1/browse?alt=json&key={url_key}"
        self.headers = {
            "accept": "*/*",
            "accept-language": "he-IL,he;q=0.9,en-US;q=0.8,en;q=0.7",
            "authorization": f"{api_key}",
            "content-type": "application/json",
            "cookie": f"{cookie}",
            }
        self.payload = {
            'browseId': 'FEmusic_analytics_charts_home',
            'context': {
                'capabilities': {},
                'client': {
                    'clientName': "WEB_MUSIC_ANALYTICS",
                    'clientVersion': "2.0",
                    'experimentIds': [],
                    'experimentsToken': "",
                    'gl': 'IL',
                    'hl': 'en',
                    'theme': 'MUSIC'
                },
                'request': {
                    'internalExperimentFlags': [],
                }
            },
        }
        self.countries = [
            "ar",
            "au",
            "at",
            "be",
            "bo",
            "br",
            "ca",
            "cl",
            "co",
            "cr",
            "cz",
            "dk",
            "do",
            "ec",
            "eg",
            "sv",
            "ee",
            "fi",
            "fr",
            "de",
            "gt",
            "hn",
            "hu",
            "is",
            "in",
            "id",
            "ie",
            "il",
            "it",
            "jp",
            "ke",
            "lu",
            "mx",
            "nl",
            "nz",
            "ni",
            "ng",
            "no",
            "pa",
            "py",
            "pe",
            "pl",
            "pt",
            "ro",
            "ru",
            "sa",
            "rs",
            "za",
            "kr",
            "es",
            "se",
            "ch",
            "tz",
            "tr",
            "ug",
            "ug",
            "ua",
            "ae",
            "gb",
            "us",
            "uy",
            "zw",
        ]

    def get_payload(self, country, timing, youtube_chart_type):
        if youtube_chart_type == "Youtube Charts":
            self.payload['query'] = f"perspective=CHART_DETAILS&chart_params_country_code={country}&chart_params_chart_type=VIDEOS&chart_params_period_type={timing}"
        else:
            self.payload['query'] = f"perspective=CHART_DETAILS&chart_params_country_code={country}&chart_params_chart_type=TRENDING_VIDEOS"

        return self.payload

    def extract_relevant_data(self, chart_data, country, timing, youtube_chart_type):
        extracted_data = []
        country_code = get_country_code(country)
        chart_type = get_chart_type(timing)
        date = get_today_date()
        
        for entry in chart_data[:1]:
            song_name = entry.get("title", None)
            song_length = convert_seconds(entry.get("videoDuration", 0)) if entry.get("videoDuration") else None
            artist_name = entry.get("artists", [{}])[0].get("name", None)
            rank_value = entry.get("chartEntryMetadata", {}).get("currentPosition", None)
            song_link = f"https://www.youtube.com/watch?v={entry.get('id', '')}" if entry.get("id") else None

            extracted_data.append({
                "artist": {
                    "artist_name": artist_name,
                    "country_code": None,
                    "artist_gender": None,
                },
                "song": {
                    "song_name": song_name,
                    "song_link": song_link,
                    "song_lyrics": None,
                    "song_length": song_length,
                },
                "chart": {
                    "rank_value": rank_value,
                    "date": date,
                    "source": youtube_chart_type,
                    "country_code": country_code,
                    "chart_type": chart_type,
                }
            })
        
        return extracted_data    

    def fetch_charts(self, country, timing, youtube_chart_type):
        payload = self.get_payload(country, timing, youtube_chart_type)
        response = requests.post(self.base_url, headers=self.headers, json=payload)
        if response.status_code == 200:
            try:
                data = response.json()
                chart_data = data['contents']['sectionListRenderer']['contents'][0]['musicAnalyticsSectionRenderer']['content']["videos"][0]["videoViews"] 
                extracted_data = self.extract_relevant_data(chart_data, country, timing, youtube_chart_type)
                print("extracted_data: ", extracted_data) 
                return extracted_data
            except json.JSONDecodeError:
                print("Failed to decode JSON from the response.")
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}, Response: {response.text}")

    def fetch_all_countries_charts(self, timing, youtube_chart_type):
        all_countries_data = []
        for country in self.countries:
            country_data = self.fetch_charts(country, timing, youtube_chart_type)
            if country_data:
                all_countries_data.extend(country_data)
            time.sleep(2)
        return all_countries_data