import os
from os.path import join, dirname, abspath
import sys
sys.path.append(abspath(join(dirname(__file__), '..')))
from genericScraper import get_chart_type, get_country_code
import requests
from datetime import datetime, timedelta
# from dotenv import load_dotenv

# dotenv_path = abspath(join(dirname(__file__),'..', '.env'))
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# load_dotenv(dotenv_path)
# print(f"Loaded .env from: {dotenv_path}")


class SpotifyScraper:
    def __init__(self, api_key, base_url, headers):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = headers
        self.countries = [
            "ar", "au", "at", "by", "be", "bo", "br", "bg", "ca", "cl", "co", "cr", "cy", "cz", "dk",
            "do", "ec", "eg", "sv", "ee", "fi", "fr", "de", "gr", "gt", "hn", "hk", "hu", "is", "in", "id",
            "ie", "il", "it", "jp", "kz", "lv", "lt", "lu", "my", "mx", "ma", "nl", "nz", "ni", "ng", "no",
            "pk", "pa", "py", "pe", "ph", "pl", "pt", "ro", "sa", "sg", "sk", "za", "kr", "es", "se", "ch",
            "tw", "th", "tr", "ae", "ua", "gb", "uy", "us", "ve", "vn"
        ]

    # def get_dates(self, start_date_str, timing):
    #     """Generate a list of dates based on timing (weekly or daily)."""

    #     dates = []

    #     if timing == "WEEKLY":
    #         delta = timedelta(days=7)
    #         start_date = datetime.strptime("2024-08-29", "%Y-%m-%d")

    #     else:
    #         delta = timedelta(days=1)
    #         start_date = datetime.now() - timedelta(weeks=4)
    #         start_date_str = start_date.strftime("%Y-%m-%d")
    #         start_date = datetime.strptime(start_date_str, "%Y-%m-%d")

    #     end_date = datetime.now() - timedelta(weeks=1)
    #     while start_date <= end_date:
    #         dates.append(start_date.strftime("%Y-%m-%d"))
    #         start_date += delta

    #     return dates

    def extract_relevant_data(self, country, chart_data, timing):
        """Extract relevant data from the chart data and return in a flat JSON structure."""
        extracted_data = []
        top_n = 10
        chart_type = get_chart_type(timing)

        for entry in chart_data['entries'][:top_n]:
            extracted_data.append({
                "artist": {
                    "artist_name": entry['trackMetadata']['artists'][0].get('name', None),
                    "country_code": None,
                },
                "song": {
                    "song_name": entry['trackMetadata'].get('trackName', None),
                    "song_link": entry['trackMetadata'].get('trackUri', None),
                    "song_lyrics": None,
                    "song_length": entry['trackMetadata'].get('durationMs', None),
                },
                "chart": {
                    "rank_value": entry['chartEntryData'].get('currentRank', None),
                    "date": entry['chartEntryData'].get('entryDate', None),
                    "source": "Spotify",
                    "country_code": country,
                    "chart_type": chart_type,
                }
            })
        return extracted_data

    def fetch_charts(self, country, timing):
        country_code = get_country_code(country)
        chart_type = get_chart_type(timing)
        
        all_data = []
        print("base_url", self.base_url)

        # for date in dates:
        url = f"{self.base_url}/latest"
        print(f"Fetching URL: {url}")  # Debug: Print URL

        response = requests.get(url, headers=self.headers)
        try:
            if response.status_code == 200:
                chart_data = response.json()
                relevant_data = self.extract_relevant_data(
                    country, chart_data, timing)
                all_data.extend(relevant_data)
            else:
                print(f"Response Content: {response.text}")
        except requests.exceptions.JSONDecodeError:
            print(f"Error decoding JSON for {url}. Response was not JSON: {response.text}")

        return all_data

## DEBUGINGGG ##

# API_KEY = os.environ.get("SPOTIFY_API_KEY_DAILY")
# BASE_URL = "https://charts-spotify-com-service.spotify.com/auth/v0/charts/regional-global-daily" 
# HEADERS = {
#     "Authorization": f"Bearer {API_KEY}",
#     "Accept": "application/json"
# }

# scraper = SpotifyScraper(API_KEY, BASE_URL, HEADERS)
# output_data = scraper.fetch_charts(country="us", timing="DAILY")
# print("API_KEY", API_KEY)
# print("Fetched Spotify Charts Data:", output_data)

