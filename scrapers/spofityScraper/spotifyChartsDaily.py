import os
from os.path import join, dirname, abspath

dotenv_path = abspath(join(dirname(__file__),'.env'))
from dotenv import load_dotenv
load_dotenv(dotenv_path)

from spotifyScraper import SpotifyScraper


SPOTIFY_API_KEY_DAILY  = os.environ.get("SPOTIFY_API_KEY_DAILY")


api_key = SPOTIFY_API_KEY_DAILY
base_url = "https://charts-spotify-com-service.spotify.com/auth/v0/charts/regional-global-daily"
headers = {"Authorization": api_key, "Accept": "application/json"}
timing = "DAILY"


spotifyScraper = SpotifyScraper(api_key, base_url, headers)
global_charts = spotifyScraper.fetch_charts("global", timing) ## TO DO: match  the fetch_charts function to work with these parameters 

data = global_charts 

print("data", data)