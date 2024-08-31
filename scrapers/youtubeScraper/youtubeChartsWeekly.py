import os
from .youtubeScraper import YoutubeScraper  
import boto3
import json

from os.path import join, dirname
from dotenv import load_dotenv
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

YOUTUBE_CHARTS_API_KEY  = os.environ.get("YOUTUBE_CHARTS_API_KEY")
YOUTUBE_CHARTS_URL_KEY = os.environ.get("YOUTUBE_CHARTS_URL_KEY")
YOUTUBE_CHARTS_COOKIE = os.environ.get("YOUTUBE_CHARTS_COOKIE")

def handler(event, context):
    timing = "WEEKLY"
    youtube_chart = "Youtube Charts"

    youtube_scraper = YoutubeScraper(YOUTUBE_CHARTS_API_KEY, YOUTUBE_CHARTS_URL_KEY, YOUTUBE_CHARTS_COOKIE)
    global_charts = youtube_scraper.fetch_charts("global", timing, youtube_chart)
    countries_charts = youtube_scraper.fetch_all_countries_charts(timing, youtube_chart)

    data = []
    data.extend(global_charts)
    data.extend(countries_charts)

    # print(data)

    sqs = boto3.client(
        'sqs', 
        region_name="us-east-1",
        endpoint_url='http://sqs:9324',
        aws_access_key_id='x', 
        aws_secret_access_key='x'
    )

    queue_url = 'http://sqs:9324/queue/data-raw-q'

    try:
        scraped_data = data
        response = sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps(scraped_data, ensure_ascii=False)
        )
        return {"message": "Data from youtube weekly has been scraped and sent to SQS", "SQSResponse": response}
    except Exception as e:
        print(f"Error: {e}")
        raise e