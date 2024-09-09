from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json

load_dotenv()

client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

def sp_get_token():
    """Generate an access token for Spotify API using client credentials."""
    try:
        auth_string = client_id + ":" + client_secret
        auth_bytes  = auth_string.encode("utf-8")
        auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
        
        url = "https://accounts.spotify.com/api/token"
        headers = {
            "Authorization": "Basic " + auth_base64,
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {"grant_type": "client_credentials"}
        result = post(url, headers=headers, data=data)
        json_result = json.loads(result.content)
        token = json_result["access_token"]
        return token
    except Exception as e:
        print("Error getting Spotify token: ", e)
        return None


def sp_get_auth_header(token):
    """Return the authorization header with the provided token."""
    return{"Authorization": "Bearer " + token}


def sp_search_for_artist(token, artist_name):
    """Search for an artist by name and return the artist's information if found."""
    try:
        url = "https://api.spotify.com/v1/search"
        headers = sp_get_auth_header(token)
        query = f"?q={artist_name}&type=artist&limit=1"
        
        query_url = url + query
        result = get(query_url, headers=headers)
        json_result = json.loads(result.content)["artists"]["items"]
        if len(json_result) == 0:
            return None    
        return json_result[0]
    except Exception as e:
        print("Error searching for artist: ", e)
        return None
    
def sp_get_songs_by_artist(token, artist_id):
    """Get the top tracks of an artist by their Spotify ID."""
    try:
        url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
        headers = sp_get_auth_header(token)
        result = get(url,headers=headers)
        json_result = json.loads(result.content)["tracks"]
        return json_result
    except Exception as e:
        print("Error getting artist's top tracks: ", e)
        return None

def sp_get_available_genre(token):
    """Retrieve a list of available genre seeds from Spotify."""
    try:
        url = f"https://api.spotify.com/v1/recommendations/available-genre-seeds"
        headers = sp_get_auth_header(token)
        result = get(url,headers=headers)
        json_result = json.loads(result.content)["genres"]
        return json_result
    except Exception as e:
        print("Error getting available genre seeds: ", e)
        return None 

def search_for_track(token, track_name):
    """Search for a track by its name and return the first matching result."""
    try:
        url = "https://api.spotify.com/v1/search"
        headers = sp_get_auth_header(token)
        query = f"?q={track_name}&type=track&limit=1"
        
        query_url = url + query
        result = get(query_url, headers=headers)
        json_result = json.loads(result.content)["tracks"]["items"]
        
        if len(json_result) == 0:
            return "Unknown"
        return json_result[0]
    except Exception as e:
        print("Error searching for track: ", e)
        return "Unknown"


    
    

