import requests
import json
import logging
import os
from MusicAddedDataAPI.GeniusLyricsApi import gl_get_lyrics
from MusicAddedDataAPI.MusicBrainzApi import mb_get_gender_and_country
from MusicAddedDataAPI.SpotifyApi import sp_search_for_artist, sp_get_songs_by_artist, sp_get_available_genre
from dbUtils import get_gernes_from_db, create_genre

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
    return None

def get_missing_data_for_artist(artist):
    """Prepare the entry for sending to the external API."""
    try:
        artist_name = artist.get('artist_name', 'Unknown')
        if not artist_name:
            raise ValueError("Missing artist name")
        
        if not artist.get('genre_id') and not artist.get('country'):
            gender, country = mb_get_gender_and_country(artist_name)
            artist['genre_id'] = gender
            artist['country_code'] = country

        return artist
    except Exception as e:
        logger.error(f"Failed to prepare entry: {e}")
        return None


def get_missing_data_for_song(song, artist_name):
    """Prepare the entry for sending to the external API."""
    try:
        song_name = song.get('song_name', 'Unknown')
        if not song_name:
            raise ValueError("Missing artist or song name")

        if not song.get('song_lyrics'):
            lyrics = gl_get_lyrics(artist_name, song_name)
            song['song_lyrics'] = lyrics

        if not song.get('song_length'):
            song['song_length'] = get_song_length(artist_name, song_name)
        
        return song
    except Exception as e:
        logger.error(f"Failed to prepare entry: {e}")
        return None