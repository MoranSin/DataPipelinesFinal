# tests/test_integration.py
import os
import json
import boto3
from spotifyScraper import SpotifyScraper
from dotenv import load_dotenv

load_dotenv()

def test_spotify_scraper_integration():
    # Initialize SpotifyScraper
    api_key = os.getenv('SPOTIFY_API_KEY')
    base_url = "https://charts.spotify.com/charts/view/regional-global-weekly/latest"
    headers = {"Authorization": f"Bearer {api_key}"}
    spotify_scraper = SpotifyScraper(api_key, base_url, headers)
    
    # Fetch charts data
    data = spotify_scraper.fetch_charts("global", "WEEKLY")
    assert data is not None, "Data fetch failed"
    print("Data fetched successfully!")

    # Set up SQS
    sqs = boto3.client(
        'sqs', 
        endpoint_url='http://sqs:9324',
        region_name='us-east-1',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
    )
    
    queue_url = 'http://sqs:9324/queue/data-raw-q'

    # Send message to SQS
    response = sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=json.dumps(data, ensure_ascii=False)
    )
    
    assert response['ResponseMetadata']['HTTPStatusCode'] == 200, "Failed to send message to SQS"
    print("Message sent to SQS successfully!")

test_spotify_scraper_integration()
