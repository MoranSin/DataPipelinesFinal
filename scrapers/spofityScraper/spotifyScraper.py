import os
from os.path import join, dirname
import sys
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from genericScraper import get_chart_type, get_today_date, get_country_code

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
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        dates = []
        
        if timing == "WEEKLY":
            delta = timedelta(days=7)
        else:
            delta = timedelta(days=1)
        
        end_date = datetime.now()
        while start_date <= end_date:
            dates.append(start_date.strftime("%Y-%m-%d"))
            start_date += delta
        
        return dates

    def extract_relevant_data(self, country, date, chart_data):
        """Extract relevant data from the chart data for the database schema."""
        extracted_data = []
        top_n = 10  

        for entry in chart_data['entries'][:top_n]:
            # Extract song details
            source = 'spotify'
            song_id = entry['trackMetadata'].get('trackUri', '').split(':')[-1]  
            song_name = entry['trackMetadata'].get('trackName', '')
            song_link = entry['trackMetadata'].get('trackUri', '') 
            song_length = entry['trackMetadata'].get('durationMs', '') 

            artist_data = entry['trackMetadata']['artists'][0] 
            artist_id = artist_data.get('artistUri', '').split(':')[-1] 
            artist_name = artist_data.get('name', '')
            artist_genre = None  
            artist_gender = None 

            rank_value = entry['chartEntryData'].get('currentRank', 0)
            streams = entry['chartEntryData']['rankingMetric'].get('value', 0)

            extracted_data.append({
                "song": {
                    "song_name": song_name,
                    "song_link": song_link,
                    "song_length": song_length,
                    "artist": {
                        "artist_id": artist_id,
                        "artist_name": artist_name,
                        "artist_genre": artist_genre,
                        "artist_gender": artist_gender,
                        "country": country
                    }
                },
                "chart": {
                    "rank_value": rank_value,
                    "date": date,
                    "country": country,
                    "source": "Spotify",
                    "song_id": song_id
                }
            })
        return extracted_data

    def fetch_charts(self, country, timing):
        country_code = get_country_code(country)
        chart_type = get_chart_type(timing)
        dates = self.get_dates(get_today_date(), timing)
        all_data = []

        for date in dates:
            url = f"{self.base_url}/regional-{country_code}-{chart_type.lower()}/{date}"
            print(f"Fetching URL: {url}")
            response = requests.get(url, headers=self.headers)

            if response.status_code == 200:
                chart_data = response.json()
                relevant_data = self.extract_relevant_data(country, date, chart_data)
                all_data.extend(relevant_data)
            else:
                print(f"Failed to fetch data for {country} on {date}: {response.status_code}")
                print(response.text)

        return all_data
