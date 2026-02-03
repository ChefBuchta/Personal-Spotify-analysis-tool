import pandas as pd
import glob 

# INPUT 
path = 'data/Streaming_History_Audio*.json'
files = glob.glob(path)
dfList = [pd.read_json(f) for f in files]
df = pd.concat(dfList, ignore_index=True)

df = df.drop(columns=["ip_addr", "spotify_track_uri", "platform", "offline_timestamp", "conn_country", "offline", "incognito_mode", "episode_name", "episode_show_name", "spotify_episode_uri", "audiobook_title", "audiobook_chapter_uri", "audiobook_chapter_title"])
df['ts'] = pd.to_datetime(df['ts'])


df["ms_played"] = df['ms_played'] / 1000
df.rename(columns={'ms_played': 'sec_played', 'master_metadata_album_artist_name': 'artist_name','master_metadata_track_name': "track_name" }, inplace=True)
# print(df.head())


# PRINTS TIME SPENT LISTENING SUM
def printTimeSpentListening(df: pd.DataFrame) -> None:
    timeSpent = df["sec_played"].sum()
    print(f"TIME SPENT LISTENING {(timeSpent/3600).round(2)} HOURS {((timeSpent/60)%60).round(2)} MINUTES {(timeSpent%60).round(2)} SECONDS")

# RETURNS THE TOP 10 ARTIST BY NUMBER OF PLAYS 
def getTop10ArtistBySongs(df: pd.DataFrame) -> pd.DatFrame:
   return df['artist_name'].value_counts().head(10)  

# PRINTS THE TOP 10 ARTIST BY NUMBER OF PLAYS
def printTop10ArtistBySongs(df):
    artists = getTop10ArtistBySongs(df)
    print("\nTOP 10 ARTISTS BY SONGS PLAYED")
    print(artists)

# RETURNS THE TOP 10 SONGS BY PLAYTIME 
def getTop10ArtistByPlay(df: pd.DataFrame) -> pd.DataFrame:
    return (df.groupby('artist_name')['sec_played'].sum().sort_values(ascending=False).head(10) / 3600).round(2)

# PRINTS THE TOP 10 SONGS BY PLAYTIME 
def printTop10ArtistBySongs(df):
    artists = getTop10ArtistByPlay(df)
    print("\nTOP 10 ARTISTS BY PLAYTIME")
    print(artists)

# RETURNS THE TOP 10 SONGS BY PLAYTIME 
def getTop10SongsByPlay(df: pd.DataFrame) -> pd.DataFrame:
    return df[['track_name', 'artist_name']].value_counts().head(10) 

# PRINTS THE TOP 10 SONGS BY PLAYTIME 
def printTop10SongsByPlay(df: pd.DataFrame) -> pd.DataFrame:
    songs = getTop10SongsByPlay(df)
    print("\nTOP 10 SONGS BY TIMES PLAYED")
    print(songs)

