import os
from .spotifyScraper import SpotifyScraper
import boto3
import json
from fastapi import HTTPException
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

SPOTIFY_API_KEY_WEEKLY  = os.environ.get("SPOTIFY_API_KEY_WEEKLY")

def handler(event, context):
    api_key = SPOTIFY_API_KEY_WEEKLY
    print(api_key)
    base_url = "https://charts-spotify-com-service.spotify.com/auth/v0/charts/regional-global-weekly"
    headers = {"Authorization": api_key, "Accept": "application/json"}
    timing = "WEEKLY"

    spotifyScraper = SpotifyScraper(api_key, base_url, headers)
    global_charts = spotifyScraper.fetch_charts("global", timing) ## TO DO: match  the fetch_charts function to work with these parameters 

    data = global_charts 

    sqs = boto3.client(
        'sqs', 
        region_name="us-east-1",
        endpoint_url='http://sqs:9324'
    )

    queue_url = 'http://sqs:9324/queue/data-raw-q'

    try:
        response = sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps(data, ensure_ascii=False)
        )
        print({"message": "Data has been scraped and sent to SQS", "sqs_response": response})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))