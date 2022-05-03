import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import sys
sys.path.append("/Users/linakaval/Documents/Github/")
import auth_credentials #module with credentials

def getBTS():
    client_credentials_manager = SpotifyClientCredentials(client_id = cid, client_secret = secret)
    sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

    track_results = sp.search(q = 'artist: BTS')
    print(track_results)


def main():
    auth = auth_credentials.spotify()
    scope = "user-library-read user-top-read streaming"

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(auth['cid'], auth['secret'], redirect_uri='http://localhost:8080', scope=scope))
    #print(sp.me())
    results = sp.current_user_saved_tracks(6)
    for idx, item in enumerate(results['items']):
        track = item['track']
        print(item)
        #print(idx, track['artists'][0]['name'], " – ", track['name'])
    #print(results)
    top_tracks = sp.current_user_top_tracks(100, 0, 'medium_term')
    for idx, item in enumerate(top_tracks['items']):
        track = item['name']
        #print(item['artists'][0]['name'], " – ", track)

    
    #print(results)
    #for idx, item in enumerate(results['tracks']):
    #    r = item['name']
    #    print(r)

    
if __name__ == "__main__":
    main()

