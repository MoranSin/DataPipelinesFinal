import requests
import json
import logging

from MusicAddedDataAPI.GeniusLyricsApi import gl_get_lyrics
from MusicAddedDataAPI.MusicBrainzApi import mb_get_gender_and_country
from MusicAddedDataAPI.SpotifyApi import sp_search_for_artist, sp_get_songs_by_artist, sp_get_available_genre, search_for_track
from .dbUtils import get_gernes_from_db, create_genre, get_artist_data_from_db, get_song_from_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def convert_seconds(seconds):
    minutes, seconds = divmod(seconds, 60)
    return f"{minutes:02}:{seconds:02}"

def get_genre_data(token):
    genres = get_gernes_from_db()
    if not genres:
        new_genres = []
        genres = sp_get_available_genre(token)
        for genre_name in genres:
            genre_res = create_genre(genre_name)
            if genre_res:
                print(f"Successfully sent genre: {genre_res}")
                new_genres.append(genre_res)
        return new_genres 
    else:
        return  genres    

def get_song_length(token, artist_name, song_name):
    artist_data = sp_search_for_artist(token, artist_name)
    if artist_data:
        artist_id = artist_data['id']
        songs = sp_get_songs_by_artist(token, artist_id)
        for song_item in songs:
            if song_item['name'].lower() == song_name.lower():
                duration_ms = song_item['duration_ms']
                return convert_seconds(duration_ms // 1000)
    return 'Unknown'

def get_missing_data_for_artist(artist):
    """Prepare the entry for sending to the external API."""
    try:
        artist_name = artist.get('artist_name', 'Unknown')
        if not artist_name:
            raise ValueError("Missing artist name")
        
        gender, country = mb_get_gender_and_country(artist_name)
        artist['genre_id'] = gender if gender else "Unknown"
        artist['country_code'] = country if country else "Unknown"
        return artist
    except Exception as e:
        logger.error(f"Failed to prepare entry: {e}")
        return None


def get_missing_data_for_song(token,song, artist_name):
    """Prepare the entry for sending to the external API."""
    new_song = song
    try:
        song_name = song.get('song_name', 'Unknown')
        if not song_name:
            raise ValueError("Missing artist or song name")

        if not song.get('song_lyrics'):
            lyrics = gl_get_lyrics(artist_name, song_name)
            new_song['song_lyrics'] = lyrics

        if not song.get('song_length'):
            new_song['song_length'] = get_song_length(token,artist_name, song_name)
        
        if not song.get('song_link'):
            track = search_for_track(token, artist_name)
            new_song['song_link'] = track['external_urls']['spotify'] if track['external_urls']['spotify'] else "Unknown"
        
        return new_song
    except Exception as e:
        logger.error(f"Failed to prepare entry: {e}")
        return None

def get_song_payload(token, entry, artist_id, artist_name):
    try:
        song_payload = {
            "artist_id": None,
            "genre_id": None,
            "song_name": None,
            "song_link": None,
            "song_lyrics": None,
            "song_length": None,
        }

        song_payload["song_name"] = entry["song"]["song_name"] if entry["song"]["song_name"] else None
        song_payload["genre_id"] = None
        song_payload["artist_id"] = None
        song_payload["song_link"] = entry["song"]["song_link"] if entry["song"]["song_link"] else None
        song_payload["song_length"]= entry["song"]["song_length"] if entry["song"]["song_length"] else None
        song_payload["song_lyrics"] = None

        song_name = entry["song"]["song_name"]
        song_res = None
        if artist_id:
            song_res = get_song_from_db(song_name, artist_id)

        song_pl_res = None
        if song_res == None:
            song_pl_res = get_missing_data_for_song(token, song_payload, artist_name)
            print("Line 108")
        else:
            song_pl_res = song_res

        print("get song payload 109: ", song_pl_res)

        return song_pl_res
    except Exception as e:
        logger.error(f"Error in song payload: {e}")
        return None


def get_artist_payload(entry):
    try:
        artist_payload = {
            "artist_name": None,
            "genre_id": None,
            "country_code": None,
            "artist_gender": None,
        }

        artist_payload["artist_name"] = entry["artist"]["artist_name"] if entry["artist"]["artist_name"] else None
        artist_payload["genre_id"] = None
        artist_payload["country_code"] = entry["artist"]["country_code"] if entry["artist"]["country_code"] else None
        artist_payload["artist_gender"] = None

        artist_res = get_artist_data_from_db(entry["artist"]["artist_name"])
        if not artist_res:
            artist = entry.get("artist", {})
            artist_payload = get_missing_data_for_artist(artist)
        else:
            artist_payload = artist_res
            
        return artist_payload
    except Exception as e:
        logger.error(f"Error in artist payload: {e}")
        return None


def get_chart_payload(entry):
    chart_payload = {
        "artist_id": None,
        "song_id": None,
        "rank_value": None,
        "date": None,
        "source": None,
        "country_code": None,
        "chart_type": None,
      }

    chart_payload["artist_id"] = None
    chart_payload["genre_id"] = None
    chart_payload["rank_value"] = entry["chart"]["rank_value"] if entry["chart"]["rank_value"] else None
    chart_payload["date"] = entry["chart"]["date"] if entry["chart"]["date"] else None
    chart_payload["source"] = entry["chart"]["source"] if entry["chart"]["source"] else None
    chart_payload["country_code"] = entry["chart"]["country_code"] if entry["chart"]["source"] else None
    chart_payload["chart_type"] = entry["chart"]["chart_type"] if entry["chart"]["chart_type"] else None

    return chart_payload