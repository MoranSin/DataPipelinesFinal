from genericScraper import get_chart_type, get_today_date, get_country_code
import requests
import json
import sys
import os
import time
from os.path import join, dirname
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


def convert_seconds(n):
    """ Converts a given number of seconds, n, into a string formatted as MM:SS (minutes and seconds)."""
    minutes, seconds = divmod(n, 60)
    return f"{minutes:02}:{seconds:02}"


class YoutubeScraper:
    """
    A class used to scrape YouTube Charts data for various countries.

    Attributes:
        api_key (str): The API key used for authorization.
        base_url (str): The base URL for YouTube Charts API.
        headers (dict): The request headers, including authorization and cookie.
        payload (dict): The base payload for the POST request, including client and context data.
        countries (list): A list of country codes to fetch charts from.
    """

    def __init__(self, api_key, url_key, cookie):
        """
        Initializes the YoutubeScraper with API key, base URL, headers, and a list of countries.

        Args:
            api_key (str): The API key for authorization in the request.
            url_key (str): The URL key used to construct the base URL for the YouTube Charts API.
            cookie (str): The cookie used in the request headers.
        """
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
            "ar", "au", "at", "be", "bo", "br", "ca", "cl", "co", "cr", "cz", "dk", "do", "ec", "eg", "sv", "ee", "fi", "fr",
            "de", "gt", "hn", "hu", "is", "in", "id", "ie", "il", "it", "jp", "ke", "lu", "mx", "nl", "nz", "ni", "ng", "no",
            "pa", "py", "pe", "pl", "pt", "ro", "ru", "sa", "rs", "za", "kr", "es", "se", "ch", "tz", "tr", "ug", "ua", "ae",
            "gb", "us", "uy", "zw",
        ]


    def get_payload(self, country, timing, youtube_chart_type):
        """
        Builds the payload for the POST request to fetch YouTube chart data.

        Args:
            country (str): The country code to fetch chart data for.
            timing (str): The time period for the chart data (e.g., 'daily', 'weekly').
            youtube_chart_type (str): The type of chart to fetch (e.g., "Youtube Charts" or "Trending Videos").

        Returns:
            dict: The payload used in the POST request.
        """
        if youtube_chart_type == "Youtube Charts":
            self.payload['query'] = f"perspective=CHART_DETAILS&chart_params_country_code={country}&chart_params_chart_type=VIDEOS&chart_params_period_type={timing}"
        else:
            self.payload['query'] = f"perspective=CHART_DETAILS&chart_params_country_code={country}&chart_params_chart_type=TRENDING_VIDEOS"

        return self.payload

    def extract_relevant_data(self, chart_data, country, timing, youtube_chart_type):
        """
        Extracts and formats relevant data from the YouTube chart response.

        Args:
            chart_data (list): The raw chart data returned by the API.
            country (str): The country code for the chart data.
            timing (str): The time period of the chart data (e.g., 'weekly').
            youtube_chart_type (str): The type of chart (e.g., "Youtube Charts" or "Trending Videos").

        Returns:
            list: A list of dictionaries containing structured chart data (artist, song, rank, etc.).
        """
        extracted_data = []
        country_code = get_country_code(country)
        chart_type = get_chart_type(timing)
        date = get_today_date()
        
        for entry in chart_data[:5]:
            song_name = entry.get("title", None)
            song_length = convert_seconds(entry.get("videoDuration", 0)) if entry.get("videoDuration") else None
            artist_name = entry.get("artists", [{}])[0].get("name", None)
            rank_value = entry.get("chartEntryMetadata", {}).get("currentPosition", None)
            song_link = f"https://www.youtube.com/watch?v={entry.get('id', '')}" if entry.get("id") else None

            extracted_data.append({
                "artist": {
                    "artist_name": artist_name,
                    "country_code": None,
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
        """
        Fetches the YouTube chart data for a specific country and chart type.

        Args:
            country (str): The country code for which to fetch the charts.
            timing (str): The time period for the chart data (e.g., 'daily', 'weekly').
            youtube_chart_type (str): The type of chart (e.g., "Youtube Charts" or "Trending Videos").

        Returns:
            list: A list of extracted chart data if successful, None otherwise.
        """
        payload = self.get_payload(country, timing, youtube_chart_type)
        response = requests.post(self.base_url, headers=self.headers, json=payload)
        if response.status_code == 200:
            try:
                data = response.json()
                chart_data = data['contents']['sectionListRenderer']['contents'][0]['musicAnalyticsSectionRenderer']['content']["videos"][0]["videoViews"] 
                extracted_data = self.extract_relevant_data(chart_data, country, timing, youtube_chart_type)
                return extracted_data
            except json.JSONDecodeError:
                print("Failed to decode JSON from the response.")
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}, Response: {response.text}")

    def fetch_all_countries_charts(self, timing, youtube_chart_type):
        """
        Fetches YouTube chart data for all countries in the list and aggregates the results.

        Args:
            timing (str): The time period for the chart data (e.g., 'daily', 'weekly').
            youtube_chart_type (str): The type of chart to fetch (e.g., "Youtube Charts" or "Trending Videos").

        Returns:
            list: A list of chart data for all countries.
        """
        all_countries_data = []
        for country in self.countries:
            country_data = self.fetch_charts(country, timing, youtube_chart_type)
            if country_data:
                all_countries_data.extend(country_data)
            time.sleep(2)
        return all_countries_data