# tests/test_spotify_handler.py

import unittest
from unittest.mock import patch, MagicMock
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from spotifyScraper import spotify_handler

class TestSpotifyHandler(unittest.TestCase):
    @patch('scrapers.spotifyScraper.SpotifyScraper.fetch_charts')
    @patch('scrapers.spotifyScraper.boto3.client')
    def test_spotify_handler(self, mock_boto_client, mock_fetch_charts):
        # Mock the fetch_charts method
        mock_fetch_charts.return_value = [{"song": "Test Song", "chart": "Test Chart"}]

        # Mock SQS client and its send_message method
        mock_sqs = MagicMock()
        mock_boto_client.return_value = mock_sqs
        mock_sqs.send_message.return_value = {"ResponseMetadata": {"HTTPStatusCode": 200}}

        # Execute the handler function
        response = spotify_handler({}, {})
        self.assertEqual(response["message"], "Data scraped and sent to SQS")
        self.assertEqual(response["SQSResponse"]["ResponseMetadata"]["HTTPStatusCode"], 200)
        print("test_spotify_handler passed")

if __name__ == "__main__":
    unittest.main()
