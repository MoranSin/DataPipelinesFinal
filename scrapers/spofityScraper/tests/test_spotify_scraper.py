# tests/test_spotify_scraper.py

import unittest
from unittest.mock import patch, MagicMock
from spotifyScraper import SpotifyScraper
from genericScraper import get_chart_type, get_today_date, get_country_code
import os

class TestSpotifyScraper(unittest.TestCase):
    def setUp(self):
        # Setup mock environment
        self.api_key = "test_api_key"
        self.base_url = "https://charts.spotify.com/charts/view/regional-global-weekly/latest"
        self.headers = {"Authorization": f"Bearer {self.api_key}"}
        self.scraper = SpotifyScraper(self.api_key, self.base_url, self.headers)

    @patch('spotifyScraper.requests.get')
    def test_fetch_charts(self, mock_get):
        # Mock the requests.get to simulate API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "entries": [
                {
                    "trackMetadata": {
                        "trackUri": "spotify:track:123",
                        "trackName": "Test Song",
                        "durationMs": 210000,
                        "artists": [
                            {"artistUri": "spotify:artist:456", "name": "Test Artist"}
                        ]
                    },
                    "chartEntryData": {
                        "currentRank": 1,
                        "rankingMetric": {"value": 1000}
                    }
                }
            ]
        }
        mock_get.return_value = mock_response

        # Execute the fetch_charts function
        data = self.scraper.fetch_charts("global", "WEEKLY")
        self.assertTrue(len(data) > 0)
        self.assertEqual(data[0]['song']['song_name'], "Test Song")
        self.assertEqual(data[0]['chart']['rank_value'], 1)
        print("test_fetch_charts passed")

    def test_get_dates(self):
        # Test the get_dates function
        dates = self.scraper.get_dates("2024-01-01", "WEEKLY")
        self.assertTrue(len(dates) > 0)
        print("test_get_dates passed")

    def test_get_chart_type(self):
        # Test get_chart_type helper function
        self.assertEqual(get_chart_type("WEEKLY"), "Weekly")
        self.assertEqual(get_chart_type("DAILY"), "Daily")
        print("test_get_chart_type passed")

if __name__ == "__main__":
    unittest.main()
