import os
import boto3
import json
from os.path import join, dirname, abspath
from dotenv import load_dotenv
from .spotifyScraper import SpotifyScraper

dotenv_path = abspath(join(dirname(__file__), '.env'))
load_dotenv(dotenv_path)

SPOTIFY_API_KEY_WEEKLY = os.environ.get("SPOTIFY_API_KEY_WEEKLY")

def handler(event, context):
    print("Spotify Weekly Handler") 
    api_key = SPOTIFY_API_KEY_WEEKLY

    base_url = "https://charts-spotify-com-service.spotify.com/auth/v0/charts/regional-global-weekly"
    headers = {"Authorization": f"Bearer {api_key}", "Accept": "application/json"}
    timing = "WEEKLY"


    spotifyScraper = SpotifyScraper(api_key, base_url, headers)
    global_charts = spotifyScraper.fetch_charts("global", timing) ## TO DO: match  the fetch_charts function to work with these parameters 

    print("weekly spotify charts: ",global_charts)

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
            MessageBody=json.dumps(global_charts, ensure_ascii=False)
        )
        return {"message": "Data from spotify weekly has been scraped and sent to SQS", "SQSResponse": response}
    except Exception as e:
        print(f"Error: {e}")
        raise e
