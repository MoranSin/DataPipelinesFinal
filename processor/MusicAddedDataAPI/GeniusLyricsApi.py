import lyricsgenius
from dotenv import load_dotenv
import os


def gl_get_lyrics(artist_name, song_name):
    load_dotenv()
    access_token = os.getenv("GENIUS_ACCESS_TOKEN")

    genius = lyricsgenius.Genius(access_token)
    artist = genius.search_artist(artist_name, max_songs=0, sort="title")
    if not artist:
        return "unknown"
    song = artist.song(song_name)
    if not song:
        return "unknown"
    lyrics = song.lyrics if song.lyrics else "unknown"
    return lyrics
