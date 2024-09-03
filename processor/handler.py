import requests
import json
import logging

from MusicAddedDataAPI.SpotifyApi import sp_get_token
from utils.dbUtils import (
    create_genre,
    create_artist,
    create_song,
    create_chart,
)
from utils.utils import (
    get_genre_data,
    get_song_payload,
    get_artist_payload,
    get_chart_payload,
    get_genre_by_name_or_id
)


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def process(event, context):
    logger.info("Received event: %s", json.dumps(event))
    print("start")
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
                        logger.error("Expected entry to be a dict, got %s", type(entry).__name__)
                        continue
                    if (not entry.get("artist") or not entry.get("song") or not entry.get("chart")):
                        logger.error("Missing data in entry")
                        continue
                                     
                    artist_payload = get_artist_payload(token, entry)
                    artist_id = artist_payload.get("artist_id") or None
                    artist_name = artist_payload.get("artist_name") or None
                    song_payload = get_song_payload(token, entry, artist_id, artist_name)
                    chart_payload = get_chart_payload(entry)
                    
                    genre_payload = artist_payload.get("genre_id") or "Unknown"
                    # print("genre_payload:", genre_payload)
                    genre_id = get_genre_by_name_or_id(genre_arr, genre_payload)
                    print("genre_id:", genre_id)
                    if not genre_id:
                        genre_res = create_genre(genre_payload)
                        artist_payload["genre_id"] = genre_res["genre_id"]
                        song_payload["genre_id"] = genre_res["genre_id"]
                    else:
                        artist_payload["genre_id"] = genre_id
                        song_payload["genre_id"] = genre_id

                    if not artist_id:
                        new_artist = create_artist(artist_payload)
                        artist_payload["artist_id"] = new_artist["artist_id"]
                    
                    # print("artist_payload:", artist_payload)
                    song_payload["artist_id"] = artist_payload["artist_id"]
                    if not song_payload.get("song_id"):
                        new_song = create_song(song_payload)
                        song_payload["song_id"] = new_song["song_id"]

                    # print("after song_payload:", song_payload)                    
                    chart_payload["artist_id"] = artist_payload["artist_id"]
                    chart_payload["song_id"] = song_payload["song_id"]
                    chart_res = create_chart(chart_payload)
                
                    # print("chart_payload:", chart_res)
                    
                    print(f"Added song {song_payload['song_name']} by artist {artist_payload['artist_name']} to chart in rank {chart_payload['rank_value']}")
                    
            except Exception as e:
                logger.error(f"Error processing data: {e}")
    print("finished processing")
    return {"statusCode": 200, "body": json.dumps("Processing is done")}
