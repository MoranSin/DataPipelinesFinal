import requests
import json
import logging

from MusicAddedDataAPI.SpotifyApi import sp_get_token
from utils.dbUtils import get_artist_data_from_db, get_song_from_db, create_genre, create_artist, create_song, create_chart
from utils.utils import get_missing_data_for_song, get_missing_data_for_artist, get_genre_data

API_ENDPOINT_ARTISTS = "http://api:8001/dev/artists"
API_ENDPOINT_SONGS = "http://api:8001/dev/songs"
API_ENDPOINT_CHARTS = "http://api:8001/dev/charts"
API_ENDPOINT_GENERE = "http://api:8001/dev/genres"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def send_prepared_data(data):
    """Send the prepared data to the external API."""
    artist_id = 1  # Fabricated ID for the example
    song_id = 1  # Fabricated ID for the example

    for entry in data:
        artist = entry.get("artist", {})
        song = entry.get("song", {})
        chart = entry.get("chart", {})

        # Post artist data
        artist_payload = {
            "artist_name": artist.get("artist_name"),
            "genre_id": 1,
            "country_code": artist.get("country_code"),
            "artist_gender": artist.get("artist_gender"),
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
            "song_name": song.get("song_name"),
            "song_link": song.get("song_link"),
            "song_lyrics": song.get("song_lyrics"),
            "song_length": song.get("song_length"),
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
            "rank_value": chart.get("rank_value"),
            "date": chart.get("date"),
            "source": chart.get("source"),
            "country_code": chart.get("country_code"),
            "chart_type": chart.get("chart_type"),
        }
        try:
            response = requests.post(API_ENDPOINT_CHARTS, json=chart_payload)
            response.raise_for_status()  # Raise an exception for HTTP errors
            logger.info(f"Chart data sent successfully: {response.status_code}")
        except requests.RequestException as e:
            logger.error(f"Failed to send chart data: {e}")


def process(event, context):
    logger.info("Received event: %s", json.dumps(event))
    token = sp_get_token()
    genre_arr = get_genre_data(token)

    if event is None:
        raise ValueError("Event data is None")

    if "Records" not in event:
        raise ValueError("No records found in event data")

    for record in event.get("Records", []):
        body = record.get("body", None)
        if body:
            try:
                data = json.loads(body)
            except json.JSONDecodeError as e:
                logger.error("Failed to decode JSON: %s", e)
                continue

            if not isinstance(data, list):
                logger.error("Expected data to be a list, got %s", type(data).__name__)
                continue

            try:
                for entry in data:
                    if not isinstance(entry, dict):
                        logger.error(
                            "Expected entry to be a dict, got %s", type(entry).__name__
                        )
                        continue
                    
                    if not entry.get("artist") or not entry.get("song") or not entry.get("chart"):
                        logger.error("Missing data in entry")
                        continue
                    
                    artist_res = get_artist_data_from_db(entry["artist"]["artist_name"])
                    artist_id = None
                    if not artist_res:
                        artist = entry.get("artist", {})
                        entry["artist"] = get_missing_data_for_artist(artist)
                    else:
                        artist_id = artist_res["artist_id"]
                        
                    print("test-1")
                    song_res = None
                    if artist_id:    
                        song_res = get_song_from_db(entry["song"]["song_name"], artist_res["artist_id"])
                    
                    print("test-1.5")
                    if not song_res:
                        song = entry.get("song", {})
                        entry["song"] = get_missing_data_for_song(token,song, entry["artist"]["artist_name"])
                    
                    # if genre not exists, add genre
                    print("test-2")
                    ####it falls here####
                    if entry["song"]["genre_id"] not in genre_arr or entry["artist"]["genre_id"] not in genre_arr:
                        print("test-3")
                        genre_res = create_genre(token, entry["song"]["genre_id"])
                        entry["song"]["genre_id"] = genre_res["genre_id"]
                        entry["artist"]["genre_id"] = genre_res["genre_id"]
                        print("test-4")
                    else:
                        print("test-5")
                        entry["song"]["genre_id"] = genre_arr[entry["song"]["genre_id"]]
                        entry["artist"]["genre_id"] = genre_arr[entry["artist"]["genre_id"]]
                        print("test-6")
                        
                    # if artist not exists, add artist
                    if not artist_res:
                        print("test-7")
                        new_artist = create_artist(token, entry["artist"])
                        entry["artist"]["artist_id"] = new_artist["artist_id"]
                        print("test-8")
                    else:
                        print("test-9")
                        entry["artist"]["artist_id"] = artist_res["artist_id"] 
                        print("test-10")   
                    
                    # if song not exists, add song
                    
                    # entry["song"]["aritst_id"] = entry["artist"]["aritst_id"]
                    # if not song_res:
                    #     new_song = create_song(token, entry["song"])
                    #     entry["song"]["song_id"] = new_song["song_id"]
                    # else:
                    #     entry["song"]["song_id"] = song_res["song_id"]
                    
                    # # add chart
                    
                    # entry["chart"]["aritst_id"] = entry["artist"]["aritst_id"]
                    # entry["chart"]["song_id"] = entry["song"]["song_id"]
                    # create_chart(token, entry["chart"])
            except Exception as e:
                logger.error(f"Error processing data: {e}")
    return {"statusCode": 200, "body": json.dumps("Processing is done")}
    

    #     for record in event.get('Records', []):
    #         body = record.get('body', None)
    #         if body:
    #             try:
    #                 # Assume body is a JSON string, so parse it
    #                 data = json.loads(body)
    #             except json.JSONDecodeError as e:
    #                 logger.error("Failed to decode JSON: %s", e)
    #                 continue

    #             if not isinstance(data, list):
    #                 logger.error("Expected data to be a list, got %s", type(data).__name__)
    #                 continue

    #             for entry in data:
    #                 if not isinstance(entry, dict):
    #                     logger.error("Expected entry to be a dict, got %s", type(entry).__name__)
    #                     continue

    #                 artist = entry.get('artist', {})
    #                 song = entry.get('song', {})

    #                 artist_name = artist.get('artist_name', 'Unknown')
    #                 song_name = song.get('song_name', 'Unknown')

    #                 if not artist.get('artist_gender'):
    #                     try:
    #                         gender = get_gender(artist_name)
    #                         artist['artist_gender'] = gender
    #                     except Exception as e:
    #                         logger.error(f"Failed to get gender for {artist_name}: {e}")

    #                 if not song.get('song_lyrics'):
    #                     try:
    #                         lyrics = get_lyrics(artist_name, song_name)
    #                         song['song_lyrics'] = lyrics
    #                     except Exception as e:
    #                         logger.error(f"Failed to get lyrics for {song_name} by {artist_name}: {e}")

    #                 if not song.get('song_length'):
    #                     try:
    #                         artist_data = search_for_artist(token, artist_name)
    #                         if artist_data:
    #                             artist_id = artist_data['id']
    #                             songs = get_songs_by_artist(token, artist_id)
    #                             for song_item in songs:
    #                                 if song_item['name'].lower() == song_name.lower():
    #                                     duration_ms = song_item['duration_ms']
    #                                     song['song_length'] = convert_seconds(duration_ms // 1000)
    #                                     break
    #                     except Exception as e:
    #                         logger.error(f"Failed to get song length for {song_name} by {artist_name}: {e}")

    #             # After processing, send the data to the external API
    #             # send_prepared_data(data)
    #             # send_prepared_genre_data()
    #             print(data)

    #         else:
    #             logger.warning("No body found in this record")

    # except (json.JSONDecodeError, ValueError) as e:
    #     logger.error("Error processing data: %s", e)



# send_prepared_genere_data()
