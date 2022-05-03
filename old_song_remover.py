import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import sys
sys.path.append("/Users/linakaval/Documents/Github/")
import auth_credentials #module with credentials
import mysql.connector
from mysql.connector import Error
from datetime import datetime
from dateutil import tz
from dateutil import parser

#Spotify stores in UTC -> want to have EST
def convertDateTime(dt):
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz('America/New_York')
    date = parser.parse(dt).replace(tzinfo=from_zone)
    #date = datetime.strptime(dt, '%Y-%m-%dT%H:%M:%S').replace(tzinfo=from_zone)
    date = date.astimezone(to_zone).strftime('%Y-%m-%d %H:%M:%S')
    return date

def getHistory(sp, sql, err):
    URI = ""
    history = sp.current_user_recently_played()
    for item in history['items']:
        #get URI
        URI = item['track']['uri'].replace('spotify:track:', '')
        #print(URI)
        play_date = convertDateTime(item['played_at'])
        #print(play_date)

        insert_query = """
        CALL `Spotify`.`sp_addPlay`('{}', '{}');
        """.format(URI, play_date)
        execute_query(sql, insert_query, err)

def getCurrentLibrary(sp, sql, err, first_load = 0):
    if first_load:
        results = sp.current_user_saved_tracks()
        tracks = results['items']
        while results['next']:
            results = sp.next(results)
            tracks.extend(results['items'])
        with open("myfile.txt", "w") as myfile:
            myfile.write(str(tracks))
    else:
        results = sp.current_user_saved_tracks()
        tracks = results['items']
    #print(tracks)
    #with open("cleaned.txt", "w") as cleanedfile:
    for item in tracks:
        #print(item)
        add_date = convertDateTime(item['added_at'])
        #print(add_date)
        track = item['track']['name'].replace("'", "''")
        #print('Track: {}'.format(track))
        artist = item['track']['artists'][0]['name'].replace("'", "''")
        #print('Artist: {}'.format(artist))
        URI = item['track']['uri'].replace('spotify:track:', '')
        #print('URI: {}'.format(URI))
        #cleanedfile.write("Track: {}\nArtist: {}\nURI: {}\n\n".format(track, artist, URI))
        sql_query = """CALL `Spotify`.`sp_addSong`('{}', '{}', '{}', '{}');
        """.format(URI, track, artist, add_date)
        execute_query(sql, sql_query, err)
            
def getLastLibraryAdd():
    #sql_query = """SELECT add_date FROM Spotify.songs ORDER BY add_date desc LIMIT 1;"""
    sql_query = """CALL songs.`sp_getLastLibraryAdd`();"""
    execute_query(sql_query)
    #result = getResultFromSql(connection, sql_query)
    #print(result)
    #return result

#def getResultFromSql(connection, qry):
#    cursor = connection.cursor()
#    cursor.execute(qry)
#    #get all records
#    records = cursor.fetchall()
#    print("Total number of rows in table: ", cursor.rowcount)
#    cursor.close()
#
#    return records

def getSongPlays(connection):
    song_plays = []
    sql_query = """SELECT songs.song_title, songs.song_artist, songs.song_id, play_history.song_plays, play_history.last_played
	FROM songs
	LEFT JOIN play_history
	ON songs.song_id = play_history.song_id
	ORDER BY songs.add_date, play_history.song_plays desc
    LIMIT 10;"""
  
    records = getResultFromSql(connection, sql_query)

    for row in records:
        #print("Title = {}\nArtist: {}\nID: {}\nPlays: {}\nLast played: {}".format(row[0], row[1], row[2], row[3], row[4]))
        song_plays.append({row[0], row[1], row[2], row[3], row[4]})
    return song_plays

def analyzeSongPlays(songs):
    lastTenSongs = songs[-10:]
    for item in lastTenSongs:
        print(item)


def execute_query(connection, query, err):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        #print("Query executed successfully")
    except Error as e:
        err.append(f"The error '{e}' occurred")
        #print(f"The error '{e}' occurred")

def connectToSql(host_name, user_name, user_password, err):
    connection = None
    try:
        connection = mysql.connector.connect(
        host=host_name,
        user=user_name,
        passwd=user_password)
        print("Connection to MySQL DB successful")
    except Error as e:
        err.append(f"The error '{e}' occurred")
        #print(f"The error '{e}' occurred")
    return connection


def main():
    spotify_auth = auth_credentials.spotify()
    sql_auth = auth_credentials.mysql()
    scope = "user-library-read user-top-read"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(spotify_auth['cid'], spotify_auth['secret'], redirect_uri='http://localhost:8080', scope=scope))
    
    query_errors = []

    try:
        connection = connectToSql(sql_auth['host'], sql_auth['user'], sql_auth['password'], query_errors)
        #last_add_date = getLastAdd(connection)
        #print(last_add_date)
        getHistory(sp, connection, query_errors)
        
        #add last arg 1 to grab all time current library
        #getCurrentLibrary(sp, connection, query_errors, 1)
        #songs = getSongPlays(connection)
        #analyzeSongPlays(songs)
    except Error as e:
        print("Some error occurred: {}".format(e))
    finally:
        connection.close()

    if query_errors:
        print(query_errors)
    else:
        print("No obvious SQL errors logged.")
    
   
if __name__ == "__main__":
    main()

