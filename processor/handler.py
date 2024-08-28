import requests
import json
import logging
from MusicAddedDataAPI.GeniusLyricsApi import get_lyrics
from MusicAddedDataAPI.MusicBrainzApi import get_gender
from MusicAddedDataAPI.SpotifyApi import get_token, search_for_artist, get_songs_by_artist

API_ENDPOINT_ARTISTS = "http://127.0.0.1:8001/dev/artists"
API_ENDPOINT_SONGS = "http://127.0.0.1:8001/dev/songs"
API_ENDPOINT_CHARTS = "http://127.0.0.1:8001/dev/charts"
API_ENDPOINT_GENERE = "http://127.0.0.1:8001/dev/genres"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def send_prepared_genre_data():
    genres = ["Rock", "Jazz", "Classical", "Pop", "Hip Hop", "Rap"]
    
    for genre_name in genres:
        response = requests.post(API_ENDPOINT_GENERE, json={"genre_name": genre_name}, headers={"Content-Type": "application/json"})
        
        if response.status_code == 200:
            print(f"Successfully sent genre: {genre_name}")
        else:
            print(f"Failed to send genre: {genre_name}, Status code: {response.status_code}, Response: {response.text}")


def send_prepared_data(data):
    """Send the prepared data to the external API."""
    artist_id = 1  # Fabricated ID for the example
    song_id = 1    # Fabricated ID for the example

    for entry in data:
        artist = entry.get('artist', {})
        song = entry.get('song', {})
        chart = entry.get('chart', {})

        # Post artist data
        artist_payload = {
            "artist_name": artist.get('artist_name'),
            "genre_id": 1,
            "country_code": artist.get('country'),
            "artist_gender": artist.get('artist_gender')
            
            
        }
        try:
            response = requests.post(API_ENDPOINT_ARTISTS, json=artist_payload)
            response.raise_for_status()  # Raise an exception for HTTP errors
            logger.info(f"Artist data sent successfully: {response.status_code}")
        except requests.RequestException as e:
            logger.error(f"Failed to send artist data: {e}")

        # Post song data
        song_payload = {
            "artist_id": artist_id,  
            "genre_id": 1,  # Fabricated ID for the genre
            "song_name": song.get('song_name'),
            "song_link": song.get('song_link'),
            "song_lyrics": song.get('song_lyrics'),
            "song_length": song.get('song_length')
        }
        try:
            response = requests.post(API_ENDPOINT_SONGS, json=song_payload)
            response.raise_for_status()  # Raise an exception for HTTP errors
            logger.info(f"Song data sent successfully: {response.status_code}")
        except requests.RequestException as e:
            logger.error(f"Failed to send song data: {e}")

        # Post chart data
        chart_payload = {
            "artist_id": artist_id,  # This would normally come from a previous POST response
            "song_id": song_id,  # This would normally come from a previous POST response
            "rank_value": chart.get('rank_value'),
            "date": chart.get('date'),
            "source": chart.get('source'),
            "country_code": chart.get('country'),
            "chart_type": chart.get('chart_type')
        }
        try:
            response = requests.post(API_ENDPOINT_CHARTS, json=chart_payload)
            response.raise_for_status()  # Raise an exception for HTTP errors
            logger.info(f"Chart data sent successfully: {response.status_code}")
        except requests.RequestException as e:
            logger.error(f"Failed to send chart data: {e}")

def convert_seconds(seconds):
    minutes, seconds = divmod(seconds, 60)
    return f"{minutes:02}:{seconds:02}"

def process(event, context):
    logger.info("Received event: %s", json.dumps(event))
    
    try:
        if event is None:
            raise ValueError("Event data is None")
        
        token = get_token()  

        for record in event.get('Records', []):
            body = record.get('body', None)
            if body: 
                try:
                    # Assume body is a JSON string, so parse it
                    data = json.loads(body)
                except json.JSONDecodeError as e:
                    logger.error("Failed to decode JSON: %s", e)
                    continue
                
                if not isinstance(data, list):
                    logger.error("Expected data to be a list, got %s", type(data).__name__)
                    continue
                
                for entry in data:
                    if not isinstance(entry, dict):
                        logger.error("Expected entry to be a dict, got %s", type(entry).__name__)
                        continue
                    
                    artist = entry.get('artist', {})
                    song = entry.get('song', {})
                    
                    artist_name = artist.get('artist_name', 'Unknown')
                    song_name = song.get('song_name', 'Unknown')
                    
                    if not artist.get('artist_gender'):
                        try:
                            gender = get_gender(artist_name)
                            artist['artist_gender'] = gender
                        except Exception as e:
                            logger.error(f"Failed to get gender for {artist_name}: {e}")

                    if not song.get('song_lyrics'):
                        try:
                            lyrics = get_lyrics(artist_name, song_name)
                            song['song_lyrics'] = lyrics
                        except Exception as e:
                            logger.error(f"Failed to get lyrics for {song_name} by {artist_name}: {e}")

                    if not song.get('song_length'):
                        try:
                            artist_data = search_for_artist(token, artist_name)
                            if artist_data:
                                artist_id = artist_data['id']
                                songs = get_songs_by_artist(token, artist_id)
                                for song_item in songs:
                                    if song_item['name'].lower() == song_name.lower():
                                        duration_ms = song_item['duration_ms']
                                        song['song_length'] = convert_seconds(duration_ms // 1000)
                                        break
                        except Exception as e:
                            logger.error(f"Failed to get song length for {song_name} by {artist_name}: {e}")
                
                # After processing, send the data to the external API
                # send_prepared_data(data)
                # send_prepared_genre_data()
                print(data)

            else:
                logger.warning("No body found in this record")
              
    except (json.JSONDecodeError, ValueError) as e:
        logger.error("Error processing data: %s", e)

    return {
        'statusCode': 200,
        'body': json.dumps('Processing is done')
    }

# send_prepared_genere_data()