from ssl import DefaultVerifyPaths
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import sys
import re
import logging
from fuzzywuzzy import fuzz
from time import sleep
sys.path.append("/Users/linakaval/Documents/Github/")
import auth_credentials #module with credentials
import numpy


def main():
    spotify_auth = auth_credentials.spotify()
    scope = 'user-read-currently-playing user-modify-playback-state user-read-playback-position user-read-playback-state'
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(spotify_auth['cid'], spotify_auth['secret'], redirect_uri='http://localhost:8080', scope=scope))
    #track = sp.current_user_playing_track()
    
    features = {'danceability' : 0,         #index 1
                'energy': 0,                #index 2
                'speechiness': 0,           #index 3
                'acousticness': 0,          #index 4
                'instrumentalness': 0,      #index 5
                'liveness': 0,              #index 6
                'valence': 0,               #index 7
                'tempo': 0}                 #index 8
    
    songs_played = []
    
    
    track_id = sp.current_playback()['item']['uri'].replace('spotify:track:', '')
    artist_id = sp.current_playback()['item']['artists'][0]['uri'].replace('spotify:track:', '')
    track_name = sp.current_playback()['item']['name']
    track_time =  sp.current_playback()['progress_ms']
    test = sp.currently_playing()
    print(test)
    #print(sp.audio_features(track_id))
    song_danceability = sp.audio_features(track_id)[0]['danceability']
    song_energy = sp.audio_features(track_id)[0]['energy']
    song_speechiness = sp.audio_features(track_id)[0]['speechiness']
    song_acousticness = sp.audio_features(track_id)[0]['acousticness']
    song_instrumentalness = sp.audio_features(track_id)[0]['instrumentalness']
    song_liveness = sp.audio_features(track_id)[0]['liveness']
    song_valence = sp.audio_features(track_id)[0]['valence']
    song_tempo = sp.audio_features(track_id)[0]['tempo']
    
    #while(track_time < 30000):
    #    sleep(3)
    #    track_time =  sp.current_playback()['progress_ms']
    #    print('Inside loop')
    #if(sp.current_playback()['item']['name'] == track_name):
        #songs_played.append([track_name, song_danceability, song_energy, song_speechiness, song_acousticness, song_instrumentalness, song_liveness, song_valence, song_tempo])
        #print(track_time)
        #next_song = sp.recommendation_genre_seeds()
        #print(next_song)

    #print(track_name)
    #print(track_time)
    #print(track_id)


if __name__ == "__main__":
    main()