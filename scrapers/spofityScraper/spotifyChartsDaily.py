import os
from .spotifyScraper import SpotifyScraper
import boto3
import json
from fastapi import HTTPException
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

SPOTIFY_API_KEY_DAILY  = os.environ.get("SPOTIFY_API_KEY_DAILY")

def handler(event, context):
    api_key = SPOTIFY_API_KEY_DAILY
    print(SPOTIFY_API_KEY_DAILY)
    base_url = "https://charts-spotify-com-service.spotify.com/auth/v0/charts/regional-global-daily"
    headers = {"Authorization": f"Bearer {api_key}", "Accept": "application/json"}
    timing = "DAILY"

    spotifyScraper = SpotifyScraper(api_key, base_url, headers)
    global_charts = spotifyScraper.fetch_charts("global", timing) ## TO DO: match  the fetch_charts function to work with these parameters 

    data = global_charts 

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
        return {"message": "Data from spotify daily has been scraped and sent to SQS", "SQSResponse": response}
    except Exception as e:
        print(f"Error: {e}")
        raise e