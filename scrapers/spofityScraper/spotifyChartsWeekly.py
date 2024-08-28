import os
from os.path import join, dirname
from dotenv import load_dotenv
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

from spotifyScraper import SpotifyScraper

SPOTIFY_API_KEY_WEEKLY  = os.environ.get("SPOTIFY_API_KEY")

api_key = SPOTIFY_API_KEY_WEEKLY
base_url = "https://charts.spotify.com/charts/view/regional-global-weekly/latest"
headers = {"Authorization": api_key}

timing = "WEEKLY"

spotifyScraper = SpotifyScraper(api_key, base_url, headers)
global_charts = spotifyScraper.fetch_charts("global", timing) ## TO DO: match  the fetch_charts function to work with these parameters 

data = global_charts 
