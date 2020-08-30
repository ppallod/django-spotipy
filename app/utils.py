import requests
import os
import base64
import urllib
import datetime
import time
import json

class SpotifyAPI():

    #Default Initialization
    def __init__(self,client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.authenticated = False
        try:
            self.expires_at
        except AttributeError:
            self.expires_at = datetime.datetime.now()

    #Performs Authorization
    def perform_auth(self):
        if self.expires_at > datetime.datetime.now():
            self.authenticated = True
            print("Still Authenticated")
            return True

        url = "https://accounts.spotify.com/api/token"
        client_creds = f"{self.client_id}:{self.client_secret}" 
        client_creds_b64 = base64.b64encode(client_creds.encode())

        data = {"grant_type":"client_credentials"}
        headers = {"Authorization": f"Basic {client_creds_b64.decode()}"}

        r = requests.post(url=url,data=data, headers=headers)
        if r.status_code == 200:
            response = r.json()
            self.access_token = response['access_token']
            expires_in = response['expires_in'] 
            self.expires_at = datetime.datetime.now() + datetime.timedelta(seconds=expires_in) 
            self.authenticated = True
            return True
        else:
            return "authentication failed"
    
    def search(self,query,entity='track'):
        endpoint = "https://api.spotify.com/v1/search"
        headers = {"Authorization":f"Bearer {self.access_token}"}
        data = urllib.parse.urlencode({"q":query, "type": entity.lower()})
        url = f"{endpoint}?{data}"
        r = requests.get(url=url, headers=headers)
        if r.status_code == 200:
            return r.json()
        else:
            return "search failed"
        
    def get_artist(self, id, entity='albums'):
        url = f"https://api.spotify.com/v1/artists/{id}/{entity}"
        if entity == 'top-tracks':
            url = f"https://api.spotify.com/v1/artists/{id}/{entity}?country=US"
        headers = {"Authorization":f"Bearer {self.access_token}"}
        r = requests.get(url=url,headers=headers)
        if r.status_code == 200:
            return r.json()
        else:
            return "search failed"
    
    def get_album(self, id, entity=''):
        url = f"https://api.spotify.com/v1/albums/{id}/{entity}"
        headers = {"Authorization":f"Bearer {self.access_token}"}
        r = requests.get(url=url,headers=headers)
        if r.status_code == 200:
            return r.json()
        else:
            return "search failed"

