import requests
import json
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from genericScraper import get_alpha3_coutry_code

from os.path import join, dirname
from dotenv import load_dotenv
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

YOUTUBE_CHARTS_API_KEY  = os.environ.get("YOUTUBE_CHARTS_API_KEY")
YOUTUBE_CHARTS_URL_KEY = os.environ.get("YOUTUBE_CHARTS_URL_KEY")
YOUTUBE_CHARTS_COOKIE = os.environ.get("YOUTUBE_CHARTS_COOKIE")

class YoutubeChartsScraper:
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

    def get_payload(self, country, timing):
        self.payload['query'] = f"perspective=CHART_DETAILS&chart_params_country_code={country}&chart_params_chart_type=VIDEOS&chart_params_period_type={timing}"
        return self.payload

    def extract_relevant_data(self, chart_data, country):
        extracted_data = []
        country_code = "GBL"
        if country != "global":
            country_code = get_alpha3_coutry_code(country)
        
        for entry in chart_data:
            song_name = entry["title"] if entry["title"] else None
            song_length = entry["videoDuration"] if entry["videoDuration"] else None
            artist_name = entry["artists"][0]["name"] if entry["artists"] else None
            rank_value = entry["chartEntryMetadata"]["currentPosition"] if entry["chartEntryMetadata"]["currentPosition"] else None
            song_link = f"https://www.youtube.com/watch?v={entry['id']}" if entry["id"] else None
            
            print("Song Name: ", song_name)
            print("Song Length: ", song_length)
            print("Artist Name: ", artist_name)
            print("Rank Value: ", rank_value)
            print("Song Link: ", song_link)
            print("Country Code: ", country_code)
            
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
                    "date": None,
                    "source": "Youtube Charts",
                    "country_code": country_code,
                }
            })
        
        return extracted_data    

    def fetch_charts(self, country, timing):
        payload = self.get_payload(country, timing)
        response = requests.post(self.base_url, headers=self.headers, json=payload)
        if response.status_code == 200:
            try:
                data = response.json()
                chart_data = data['contents']['sectionListRenderer']['contents'][0]['musicAnalyticsSectionRenderer']['content']["videos"][0]["videoViews"]
                # i = 0
                # for entry in chart_data:
                #     print(entry)
                #     i += 1
                #     if i == 5:
                #         break
                extracted_data = self.extract_relevant_data(chart_data, country)
                return extracted_data
            except json.JSONDecodeError:
                print("Failed to decode JSON from the response.")
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}, Response: {response.text}")


api_key = YOUTUBE_CHARTS_API_KEY
url_key = YOUTUBE_CHARTS_URL_KEY
ytube_cookie = YOUTUBE_CHARTS_COOKIE
countries = "global"
timing = "WEEKLY"

youtube_scraper = YoutubeChartsScraper(api_key, url_key, ytube_cookie)
data = youtube_scraper.fetch_charts(countries, timing)
