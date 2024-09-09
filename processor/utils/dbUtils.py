import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

API_ENDPOINT_ARTISTS = "http://api:8001/dev/artists"
API_ENDPOINT_SONGS = "http://api:8001/dev/songs"
API_ENDPOINT_CHARTS = "http://api:8001/dev/charts"
API_ENDPOINT_GENERE = "http://api:8001/dev/genres"

def get_gernes_from_db():
    """Fetches the list of genres from the database via a REST API."""
    try:
        response = requests.get(API_ENDPOINT_GENERE)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Failed to fetch genre data: {e}")
        return None


def create_genre(genre_name):
    """Creates a new genre entry in the database via a REST API."""
    try:
        response = requests.post(
            API_ENDPOINT_GENERE,
            json={"genre_name": genre_name},
            headers={"Content-Type": "application/json"},
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Failed to create genre: {e}")
        return None

def get_artist_data_from_db(artist_name):
    """Fetches artist data from the database via a REST API."""
    try:
        response = requests.get(f"{API_ENDPOINT_ARTISTS}/name/{artist_name}")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Failed to fetch artist data: {e}")
        return None

def create_artist(artist_entry):
    """Creates a new artist entry in the database via a REST API."""
    try:
        response = requests.post(
            API_ENDPOINT_ARTISTS,
            json=artist_entry,
            headers={"Content-Type": "application/json"},
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Failed to create an artist: {e}")
        return None

def get_song_from_db(song_name, artist_id):
    """Fetches a song's data from the database via a REST API."""
    try:
        response = requests.get(f"{API_ENDPOINT_SONGS}/name/{song_name}/artist/{artist_id}")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Failed to fetch song data: {e}")
        return None

def create_song(song):
    """Creates a new song entry in the database via a REST API."""
    try:
        response = requests.post(
            API_ENDPOINT_SONGS,
            json=song,
            headers={"Content-Type": "application/json"},
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Failed to create song: {e}")
        return None

def create_chart(chart):
    """Creates a new chart entry in the database via a REST API."""
    try:
        response = requests.post(
            API_ENDPOINT_CHARTS,
            json=chart,
            headers={"Content-Type": "application/json"},
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Failed to create chart: {e}")
        return None
