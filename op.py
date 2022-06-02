import requests
import math
import re
import sys
import os
from dotenv import load_dotenv
import re
import json

load_dotenv()
AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
ME_URL = 'https://api.spotify.com/v1/me'
API_KEY = os.getenv("YT_KEY")
SPOTIFY_ID = os.getenv("SPOTIFY_ID")
SPOTIFY_KEY = os.getenv("SPOTIFY_KEY")
REDIRECT_URI = os.getenv("REDIRECT_URI")

spotify_token = ''


#Sér um að gera http requestið, token er fyrir næsta page ef needed    
def makeRequest(playlistId, token = ''):
    url = 'https://youtube.googleapis.com/youtube/v3/playlistItems?'
    headers = {'Accept' : 'application/json'}   #Held að sé useless?
    payload = {'part' : 'snippet', 
               'pageToken' : token, 
               'playlistId' : playlistId, 
               'maxResults' : 200, 
               'key' : API_KEY} 
    return requests.get(url, params = payload, headers = headers)


'''def getTitleAndArtist(youtube_url):
    song_name = None
    artist_name = None
 
    r = requests.get(youtube_url)
 
    raw_matches = re.findall('(\{"metadataRowRenderer":.*?\})(?=,{"metadataRowRenderer")', r.text)
    json_objects = [json.loads(m) for m in raw_matches if '{"simpleText":"Song"}' in m or '{"simpleText":"Artist"}' in m] # [Song Data, Artist Data]
 
    if len(json_objects) == 2:
        song_contents = json_objects[0]["metadataRowRenderer"]["contents"][0]
        artist_contents = json_objects[1]["metadataRowRenderer"]["contents"][0]
 
        if "runs" in song_contents:
            song_name = song_contents["runs"][0]["text"]
        else:
            song_name = song_contents["simpleText"]
           
        if "runs" in artist_contents:
            artist_name = artist_contents["runs"][0]["text"]
        else:
            artist_name = artist_contents["simpleText"]
 
    return song_name, artist_name
 '''

     
#Bætir titlum í playlist
def addToPlaylist(playlist, jsonMess):
    for item in jsonMess['items']:
        #song, artist = getTitleAndArtist(f"https://www.youtube.com/watch?v={item['snippet']['resourceId']['videoId']}")
        #Check if this works, if not use video title
        #if song is not None and artist is not None:
        #    playlist.append(artist + " - " + song)
        #else:
        track = re.sub("[\(\[].*?[\)\]]", "", item['snippet']['title']) #Remove parentheses and brackets (including what is inside them)
        track = track.rstrip() #Remove trailing white spaces
        playlist.append(track)
    
#Tekur inn url og skilar bara playlistId
def getPlaylistId(url):
    match = re.search("[&?]list=([^&]+)", url)       #Copy paste it works :)
    return (match.group()[6::])       #Mix til að ná ?list= af matchinu 

def main(url):
    playlist = []
    playlistId = getPlaylistId(url)
    res = makeRequest(playlistId)                 #Byrja að keyra fyrsta request
    print(res)
    jsonMess = res.json()                                           #
    totalResults = jsonMess['pageInfo']['totalResults']             #   
    resultsPerPage = jsonMess['pageInfo']['resultsPerPage']         #   Setup til að sjá hversu mörg requests þarf að gera

    addToPlaylist(playlist, jsonMess)
    #Koma í veg fyrir crash ef bara eitt page
    if 'nextPageToken' in jsonMess:
        nextPageToken = jsonMess['nextPageToken']
        numRequests = math.ceil(totalResults/resultsPerPage)
        for x in range(numRequests):                                                #TODO: Færa allt úr main í föll
            res = makeRequest(playlistId, nextPageToken)
            jsonMess = res.json()
            addToPlaylist(playlist, jsonMess)
            if 'nextPageToken' in jsonMess:
                nextPageToken = jsonMess['nextPageToken']
            else:
                nextPageToken = ''
    return playlist
    
    #TODO: Tengja við spotify
    accessToken = getSpotifyAuth()
    
    
    #TODO: Downloada lögum og setja í spotify playlist (Næs fyrir obscure tónlist sem er ekki á Spotify, þarf premium til að gera?)


