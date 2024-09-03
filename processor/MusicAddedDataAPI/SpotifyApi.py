from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json

load_dotenv()

client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

def sp_get_token():
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


def sp_get_auth_header(token):
    return{"Authorization": "Bearer " + token}


def sp_search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = sp_get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"
    
    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result) == 0:
        print("NO artist with this name exists...")
        return None
    
    return json_result[0]
    
    
def sp_get_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = sp_get_auth_header(token)
    result = get(url,headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result

def sp_get_available_genre(token):
    url = f"https://api.spotify.com/v1/recommendations/available-genre-seeds"
    headers = sp_get_auth_header(token)
    result = get(url,headers=headers)
    json_result = json.loads(result.content)["genres"]
    return json_result

def search_for_track(token, track_name):
    url = "https://api.spotify.com/v1/search"
    headers = sp_get_auth_header(token)
    query = f"?q={track_name}&type=track&limit=1"
    
    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["tracks"]["items"]
    
    if len(json_result) == 0:
        return "Unkonwn"
    
    return json_result[0]


    
    

