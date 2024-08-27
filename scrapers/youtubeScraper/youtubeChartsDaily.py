import os
from youtubeScraper import YoutubeScraper


from os.path import join, dirname
from dotenv import load_dotenv
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

YOUTUBE_CHARTS_API_KEY  = os.environ.get("YOUTUBE_CHARTS_API_KEY")
YOUTUBE_CHARTS_URL_KEY = os.environ.get("YOUTUBE_CHARTS_URL_KEY")
YOUTUBE_CHARTS_COOKIE = os.environ.get("YOUTUBE_CHARTS_COOKIE")
YOUTUBE_TRENDS_API_KEY = os.environ.get("YOUTUBE_TRENDS_API_KEY")
YOUTUBE_TRENDS_COOKIE = os.environ.get("YOUTUBE_TRENDS_COOKIE")

timing = "DAILY"
youtube_chart = "Youtube Charts"
youtube_trends = "Youtube Trends"

youtube_charts_scraper = YoutubeScraper(YOUTUBE_CHARTS_API_KEY, YOUTUBE_CHARTS_URL_KEY, YOUTUBE_CHARTS_COOKIE)
global_charts = youtube_charts_scraper.fetch_charts("global", timing, youtube_chart)
countries_charts = youtube_charts_scraper.fetch_all_countries_charts(timing, youtube_chart)

charts_data = global_charts + countries_charts

youtube_trends_scraper = YoutubeScraper(YOUTUBE_CHARTS_API_KEY, YOUTUBE_TRENDS_API_KEY, YOUTUBE_TRENDS_COOKIE)
trends_data = youtube_charts_scraper.fetch_all_countries_charts(timing, youtube_trends)

print("First 10 entries from Global Charts:")
for entry in global_charts:
    print(entry)

print("\nFirst 10 entries from Countries Charts:")
for entry in countries_charts:
    print(entry)

print("\nFirst 10 entries from Trends Data:")
for entry in trends_data:
    print(entry)

