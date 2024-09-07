import lyricsgenius
from dotenv import load_dotenv
import os

def gl_get_lyrics(artist_name, song_name):
    try:
        load_dotenv()
        access_token = os.getenv("GENIUS_ACCESS_TOKEN")
        
        genius = lyricsgenius.Genius(access_token)
        artist = genius.search_artist(artist_name, max_songs=0, sort="title")
        if artist == None:
            return None
        song = artist.song(song_name)
        if song == None:
            return None
        return(song.lyrics)
    except Exception as e:
        print("Error getting lyrics: ", e)
        return None

def gl_search_song(artist_name, song_name):
    load_dotenv()
    access_token = os.getenv("GENIUS_ACCESS_TOKEN")
    genius = lyricsgenius.Genius(access_token)
    song_search = genius.search_song(song_name, artist_name)
    if song_search:
        return song_search.id
    else:
        return None


def gl_get_song_details(song_id):
    load_dotenv()
    access_token = os.getenv("GENIUS_ACCESS_TOKEN")
    genius = lyricsgenius.Genius(access_token)
    song_details = genius.song(song_id)
    return song_details  


def gl_extract_lyrics_language(song_details):
    if isinstance(song_details, dict) and 'language' in song_details:
        return song_details['language']
    return 'Unknown'

def gl_get_song_lan(artist_name, song_name):
    song_id = gl_search_song(artist_name, song_name)
    if song_id:
        song_details = gl_get_song_details(song_id)

        if isinstance(song_details, dict):
            language = gl_extract_lyrics_language(song_details.get('song', {}))
            return language
        else:
            return "Unknown"
    else:
        return "Unknown"