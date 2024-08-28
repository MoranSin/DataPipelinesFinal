import os
from os.path import join, dirname

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
from dotenv import load_dotenv

from spotifyScraper import SpotifyScraper


SPOTIFY_API_KEY_DAILY  = os.environ.get("SPOTIFY_API_KEY_DAILY")


api_key = SPOTIFY_API_KEY_DAILY
base_url = "https://charts.spotify.com/charts/view/regional-global-daily/latest"
headers = {"Authorization": api_key}
timing = "DAILY"

spotify_scraper = SpotifyScraper(api_key, base_url, headers)
global_charts = spotify_scraper.fetch_charts("global", timing)

data = global_charts
