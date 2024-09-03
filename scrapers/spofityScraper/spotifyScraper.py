from genericScraper import get_chart_type, get_today_date, get_country_code
import os
from os.path import join, dirname, abspath
import sys
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

dotenv_path = abspath(join(dirname(__file__), '..', '.env'))

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

load_dotenv()


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

    def get_dates(self, start_date_str, timing):
        """Generate a list of dates based on timing (weekly or daily)."""

        dates = []

        if timing == "WEEKLY":
            delta = timedelta(days=7)
            start_date = datetime.strptime("2024-08-29", "%Y-%m-%d")

        else:
            delta = timedelta(days=1)
            start_date = datetime.now() - timedelta(weeks=4)
            start_date_str = start_date.strftime("%Y-%m-%d")
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")

        end_date = datetime.now() - timedelta(weeks=1)
        while start_date <= end_date:
            dates.append(start_date.strftime("%Y-%m-%d"))
            start_date += delta

        return dates

    def extract_relevant_data(self, country, date, chart_data):
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
                    "date": date,
                    "source": "Spotify",
                    "country_code": country,
                    "chart_type": "Weekly",
                }
            })

    def fetch_charts(self, country, timing):
        country_code = get_country_code(country)
        chart_type = get_chart_type(timing)
        dates = self.get_dates(get_today_date(), timing)
        all_data = []

        for date in dates:
            url = f"{self.base_url}/{date}"
            print(f"Fetching URL: {url}")  # Debug: Print URL

            response = requests.get(url, headers=self.headers)

            try:
                if response.status_code == 200:
                    chart_data = response.json()
                    relevant_data = self.extract_relevant_data(
                        country, date, chart_data)
                    all_data.extend(relevant_data)
                else:
                    print(f"Failed to fetch data for {country} on { date}: {response.status_code}")
                    # Debug: Response content
                    print(f"Response Content: {response.text}")
            except requests.exceptions.JSONDecodeError:
                print(f"Error decoding JSON for {url}. Response was not JSON: {response.text}")

        return all_data
