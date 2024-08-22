import requests
import time
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import json

class TiktokScraper:
    def __init__(self):
        self.base_url = "https://www.billboard.com/charts/tiktok-billboard-top-50/"
        self.countries = ["us", "gb", "de", "fr", "au", "br", "jp", "ca"]

    def get_weekly_dates(self, start_date_str):
        """Generate a list of dates for the most recent week."""
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = start_date - timedelta(days=1)  
        dates = []

        while start_date >= end_date:
            dates.append(start_date.strftime("%Y-%m-%d"))
            start_date -= timedelta(days=7)  

        return dates
    
    def extract_relevant_data(self, country, date, chart_data):
        """Extract relevant data from the chart data for the database schema."""
        extracted_data = []
        top_n = 10  

        for entry in chart_data['entries'][:top_n]:
            # Extract song details
            song_id = entry['trackMetadata'].get('trackUri', '').split(':')[-1]  
            song_name = entry['trackMetadata'].get('trackName', '')
            song_link = entry['trackMetadata'].get('trackUri', '') 
            song_length = entry['trackMetadata'].get('durationMs', '') 

            artist_data = entry['trackMetadata']['artists'][0] 
            artist_id = artist_data.get('artistUri', '').split(':')[-1] 
            artist_name = artist_data.get('name', '')
            artist_genre = None  
            artist_gender = None 

            # Extract rank details
            rank_value = entry['chartEntryData'].get('currentRank', 0)
            streams = entry['chartEntryData']['rankingMetric'].get('value', 0)

            # Build the relevant data structure
            extracted_data.append({
                "song": {
                    "song_id": song_id,
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
                "rank": {
                    "rank_value": rank_value,
                    "streams": streams,
                    "date": date,
                    "country": country,
                    "source": "Spotify",
                    "song_id": song_id
                }
            })
        return extracted_data


