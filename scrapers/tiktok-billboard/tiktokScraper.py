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

        # for entry in chart_data['o-chart-results-list__item'][:top_n]:
        #     extracted_data.append(entry)
            # Extract song details
            # song_id = entry['trackMetadata'].get('trackUri', '').split(':')[-1]  
            # song_name = entry['trackMetadata'].get('trackName', '')
            # song_link = entry['trackMetadata'].get('trackUri', '') 
            # song_length = entry['trackMetadata'].get('durationMs', '') 

            # artist_data = entry['trackMetadata']['artists'][0] 
            # artist_id = artist_data.get('artistUri', '').split(':')[-1] 
            # artist_name = artist_data.get('name', '')
            # artist_genre = None  
            # artist_gender = None 

            # # Extract rank details
            # rank_value = entry['chartEntryData'].get('currentRank', 0)
            # streams = entry['chartEntryData']['rankingMetric'].get('value', 0)

            # # Build the relevant data structure
            # extracted_data.append({
            #     "song": {
            #         # "song_id": song_id,
            #         "song_name": song_name,
            #         "song_link": song_link,
            #         "song_length": song_length,
            #         "artist": {
            #             # "artist_id": artist_id,
            #             "artist_name": artist_name,
            #             "artist_genre": artist_genre,
            #             "artist_gender": artist_gender,
            #             "country": country
            #         }
            #     },
            #     "rank": {
            #         "rank_value": rank_value,
            #         "streams": streams,
            #         "date": date,
            #         "country": country,
            #         "source": "Spotify",
            #         # "song_id": song_id
            #     }
            # })
        return chart_data
    
    def fetch_charts(self):
        dates = self.get_weekly_dates("2024-08-22")
        all_data = {country: [] for country in self.countries}
        request_count = 0

        for country in self.countries:
            for date in dates:
                url = f"{self.base_url}/regional-{country}-weekly/{date}"
                print(f"Fetching URL: {url}")
                response = requests.get(url)

                if response.status_code == 200:
                    chart_data = response.json()
                    relevant_data = self.extract_relevant_data(country, date, chart_data)
                    # Append the extracted relevant data
                    # all_data[country].extend(relevant_data)
                else:
                    print(f"Failed to fetch data for {country} on {date}: {response.status_code}")
                    # print(response.text)

                request_count += 1
                if request_count % 10 == 0:
                    print("Sleeping for 2 seconds to avoid rate limiting...")
                    time.sleep(2)

        # with open('spotify_charts_data.json', 'w') as f:
        #     json.dump(all_data, f, indent=4)
        print(relevant_data.text)


tiktok_scraper = TiktokScraper()
tiktok_scraper.fetch_charts()
    



