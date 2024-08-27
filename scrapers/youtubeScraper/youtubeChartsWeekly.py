import os
from youtubeScraper import YoutubeScraper

from os.path import join, dirname
from dotenv import load_dotenv
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

YOUTUBE_CHARTS_API_KEY  = os.environ.get("YOUTUBE_CHARTS_API_KEY")
YOUTUBE_CHARTS_URL_KEY = os.environ.get("YOUTUBE_CHARTS_URL_KEY")
YOUTUBE_CHARTS_COOKIE = os.environ.get("YOUTUBE_CHARTS_COOKIE")

timing = "WEEKLY"
youtube_chart = "Youtube Charts"

youtube_scraper = YoutubeScraper(YOUTUBE_CHARTS_API_KEY, YOUTUBE_CHARTS_URL_KEY, YOUTUBE_CHARTS_COOKIE)
global_charts = youtube_scraper.fetch_charts("global", timing, youtube_chart)
countries_charts = youtube_scraper.fetch_all_countries_charts(timing, youtube_chart)

data = global_charts + countries_charts
