import requests
import math
import re
import sys


AUTH_URL = 'https://accounts.spotify.com/api/token'

playlist = []

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
#Bætir titlum í playlist
def addToPlaylist(playlist, jsonMess):
    for item in jsonMess['items']:
        playlist.append(item['snippet']['title'])
        
def getSpotifyAuth():
    auth_response = requests.post(AUTH_URL, {
    'grant_type': 'client_credentials',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET})
    auth_response_data = auth_response.json()
    return auth_response_data['access_token']

def spotifyRequest(accessToken):
    url = 'https://api.spotify.com/v1/'
    headers = { 'Authorization': 'Bearer {token}'.format(token=accessToken)}
    
#Tekur inn url og skilar bara playlistId
def getPlaylistId(url):
    print(url)
    match = re.search("[&?]list=([^&]+)", url)       #Copy paste it works :)
    return (match.group()[6::])       #Mix til að ná ?list= af matchinu 

def main(url):
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
            print(nextPageToken)
            res = makeRequest(playlistId, nextPageToken)
            jsonMess = res.json()
            addToPlaylist(playlist, jsonMess)
            if 'nextPageToken' in jsonMess:
                nextPageToken = jsonMess['nextPageToken']
            else:
                nextPageToken = ''

    print(playlist)
    return playlist
    
    #TODO: Tengja við spotify
    accessToken = getSpotifyAuth()
    
    
    #TODO: Downloada lögum og setja í spotify playlist (Næs fyrir obscure tónlist sem er ekki á Spotify, þarf premium til að gera?)

if __name__ == "__main__":
    main(sys.argv[1])


