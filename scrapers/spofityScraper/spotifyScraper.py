import os
from os.path import join, dirname, abspath
import sys
sys.path.append(abspath(join(dirname(__file__), '..')))
from genericScraper import get_chart_type, get_country_code
import requests

class SpotifyScraper:
    def __init__(self, api_key, base_url, headers):
        """Initializes the SpotifyScraper with API credentials, base URL, and request headers."""
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


    def extract_relevant_data(self, country, chart_data, chart_type):
        """Extract relevant data from the chart data and return in a flat JSON structure."""
        extracted_data = []
        top_n = 10

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
        print("Extracted data:", extracted_data)
        return extracted_data

    def fetch_charts(self, country, timing):
        """Fetches chart data for a specific country and time period and returns the extracted relevant data."""
        country_code = get_country_code(country)
        chart_type = get_chart_type(timing)
        
        all_data = []
        url = f"{self.base_url}/latest"

        response = requests.get(url, headers=self.headers)
        try:
            if response.status_code == 200:
                chart_data = response.json()
                relevant_data = self.extract_relevant_data(
                    country_code, chart_data, chart_type)
                all_data.extend(relevant_data)
            else:
                print(f"Response Content: {response.text}")
        except requests.exceptions.JSONDecodeError:
            print(f"Error decoding JSON for {url}. Response was not JSON: {response.text}")

        return all_data


