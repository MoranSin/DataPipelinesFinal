import os
from .youtubeScraper import YoutubeScraper
import boto3
import json
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

YOUTUBE_CHARTS_API_KEY = os.environ.get("YOUTUBE_CHARTS_API_KEY")
YOUTUBE_CHARTS_URL_KEY = os.environ.get("YOUTUBE_CHARTS_URL_KEY")
YOUTUBE_CHARTS_COOKIE = os.environ.get("YOUTUBE_CHARTS_COOKIE")
YOUTUBE_TRENDS_API_KEY = os.environ.get("YOUTUBE_TRENDS_API_KEY")
YOUTUBE_TRENDS_COOKIE = os.environ.get("YOUTUBE_TRENDS_COOKIE")


def handler(event, context):
    """
    AWS Lambda handler function to fetch YouTube Charts data.

    This handler is invoked by a scheduler and processes the input event to fetch YouTube
    chart data based on the input parameters (country, timing, chart type).
    """
    print("Youtube Daily Handler")
    timing = "DAILY"
    youtube_chart = "Youtube Charts"
    youtube_trends = "Youtube Trends"

    youtube_charts_scraper = YoutubeScraper(
        YOUTUBE_CHARTS_API_KEY, YOUTUBE_CHARTS_URL_KEY, YOUTUBE_CHARTS_COOKIE)
    global_charts = youtube_charts_scraper.fetch_charts(
        "global", timing, youtube_chart)
    countries_charts = youtube_charts_scraper.fetch_all_countries_charts(
        timing, youtube_chart)

    data = []
    data.extend(global_charts)
    data.extend(countries_charts)

    youtube_trends_scraper = YoutubeScraper(
        YOUTUBE_CHARTS_API_KEY, YOUTUBE_TRENDS_API_KEY, YOUTUBE_TRENDS_COOKIE)
    trends_data = youtube_trends_scraper.fetch_all_countries_charts(
        timing, youtube_trends)

    data.extend(trends_data)

    sqs = boto3.client(
        'sqs',
        region_name="us-east-1",
        endpoint_url='http://sqs:9324',
        aws_access_key_id='x', 
        aws_secret_access_key='x'
    )

    queue_url = 'http://sqs:9324/queue/data-raw-q'

    try:
        response = sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps(data, ensure_ascii=False)
        )
        return {"message": "Data from youtube daily scraped and sent to SQS", "SQSResponse": response}
    except Exception as e:
        print(f"Error: {e}")
        raise e
