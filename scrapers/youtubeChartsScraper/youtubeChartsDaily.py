import os
from youtubeChartsScraper import YoutubeChartsScraper

from os.path import join, dirname
from dotenv import load_dotenv
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

YOUTUBE_CHARTS_API_KEY  = os.environ.get("YOUTUBE_CHARTS_API_KEY")
YOUTUBE_CHARTS_URL_KEY = os.environ.get("YOUTUBE_CHARTS_URL_KEY")
YOUTUBE_CHARTS_COOKIE = os.environ.get("YOUTUBE_CHARTS_COOKIE")

api_key = YOUTUBE_CHARTS_API_KEY
url_key = YOUTUBE_CHARTS_URL_KEY
ytube_cookie = YOUTUBE_CHARTS_COOKIE
timing = "DAILY"

youtube_scraper = YoutubeChartsScraper(api_key, url_key, ytube_cookie)
global_charts = youtube_scraper.fetch_charts("global", timing)
countries_charts = youtube_scraper.fetch_all_countries_charts(timing)

data = global_charts + countries_charts
