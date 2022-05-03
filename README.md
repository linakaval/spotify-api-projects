# spotify-api-projects
A place for me to store my tinkering code with the Spotify API

9-23-2021:
I've decided to start my old song remover project. Spotify API stores some listening history, which I will grab and store locally on using MySQL daily at 9:30am.

1-2-2022:
song_guesser.py is the start of my Spotify game. In theory, the player guesses the song and artist title of the currently playing Spotify song. While this basic functionality works, some song titles in other languages such as Japanese and Korean have convoluted titles, which I am accounting for with my own rules. The Spotify API is used to grab the information of the currently playing song and the the FuzzyWuzzy library is used to string match this to the player's input. A certain limit of error is allowed in this way. The TextBlob library is used to identify Korean and the Korean_Romanizer library is used to romanize (coming soon to Japanese titles). I still have to decide what to do with Korean titles that have both the Korean and English titles in the track name. 

Features I'm working on:
- Korean and Japanese compatibility
- Multiple artists
- Handling for when the player doesn't guess the song before it ends
- Start music if it is not curently playing
- Songs with "Intro" and "Outro" in the title
- Find a way to smartly remove "-" from titles (don't want for "NO - Japanese Ver." but need to keep for "9-teen")
- Easy and Hard modes (hard modes will be: exact title matching, all artists featured on song must be identified, song skipped after 15 secs)

Other Notes:
This requires the creation of a separate Python module called "auth_credentials.py", where the Spotify API credentials, cid and secret, are stored. I simply have a function called spotify() that returns the cid and secret as a dictionary, which I reference within old_song_remover.py
