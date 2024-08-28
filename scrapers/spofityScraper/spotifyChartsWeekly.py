import os
import boto3
import json
from os.path import join, dirname, abspath
from dotenv import load_dotenv
from spotifyScraper import SpotifyScraper

dotenv_path = abspath(join(dirname(__file__), '.env'))
load_dotenv(dotenv_path)

SPOTIFY_API_KEY_WEEKLY = os.environ.get("SPOTIFY_API_KEY_WEEKLY")

# SQS Configuration
sqs = boto3.client(
    'sqs',
    region_name="us-east-1",
    endpoint_url='http://sqs:9324'
)
queue_url = 'http://sqs:9324/queue/data-raw-q'

api_key = SPOTIFY_API_KEY_WEEKLY
base_url = "https://charts-spotify-com-service.spotify.com/auth/v0/charts/regional-global-weekly"
headers = {"Authorization": api_key, "Accept": "application/json"}
timing = "WEEKLY"

print(api_key)

spotifyScraper = SpotifyScraper(api_key, base_url, headers)
global_charts = spotifyScraper.fetch_charts("global", timing)  # Ensure fetch_charts works with these parameters

data = global_charts
print("data", data)

try:
    scraped_data = data
    response = sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=json.dumps(scraped_data, ensure_ascii=False)
    )
    print({"message": "Data has been scraped and sent to SQS", "sqs_response": response})
except Exception as e:
    print(f"Error sending data to SQS: {str(e)}")
