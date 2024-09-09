import lyricsgenius
from dotenv import load_dotenv
import os

def gl_get_lyrics(artist_name, song_name):
    """Fetch the lyrics of a song by a specific artist."""
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
    """Search for a song by its name and artist."""
    try:
        load_dotenv()
        access_token = os.getenv("GENIUS_ACCESS_TOKEN")
        genius = lyricsgenius.Genius(access_token)
        song_search = genius.search_song(song_name, artist_name)
        if song_search:
            return song_search.id
        else:
            return None
    except Exception as e:
        print("Error searching for song: ", e)
        return None


def gl_get_song_details(song_id):
    """Retrieve detailed information about a song using its Genius song ID."""
    try:
        load_dotenv()
        access_token = os.getenv("GENIUS_ACCESS_TOKEN")
        genius = lyricsgenius.Genius(access_token)
        song_details = genius.song(song_id)
        return song_details  
    except Exception as e:
        print("Error getting song details: ", e)
        return None


def gl_extract_lyrics_language(song_details):
    """Extract the language of the lyrics from the song details."""
    try:
        if isinstance(song_details, dict) and 'language' in song_details:
            return song_details['language']
        return 'Unknown'
    except Exception as e:
        print("Error extracting lyrics language: ", e)
        return 'Unknown'    

def gl_get_song_lan(artist_name, song_name):
    """Retrieve the language of a song's lyrics based on the artist and song name."""
    try:
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
    except Exception as e:  
        print("Error getting song language: ", e)
        return "Unknown"