import pandas as pd
import glob 

path = 'data/Streaming_History_Audio*.json'
files = glob.glob(path)
dfList = [pd.read_json(f) for f in files]
df = pd.concat(dfList, ignore_index=True)

df = df.drop(columns=["ip_addr", "spotify_track_uri", "platform", "offline_timestamp", "conn_country", "offline", "incognito_mode", "episode_name", "episode_show_name", "spotify_episode_uri", "audiobook_title", "audiobook_chapter_uri", "audiobook_chapter_title"])
df['ts'] = pd.to_datetime(df['ts'])


df["ms_played"] = df['ms_played'] / 1000
df.rename(columns={'ms_played': 'sec_played'}, inplace=True)
# print(df.head())
# TIME SPENT LISTENING SUM

timeSpent = df["sec_played"].sum()
# print(f"TIME SPENT LISTENING {(timeSpent/3600).round(2)} HOURS {((timeSpent/60)%60).round(2)} MINUTES {(timeSpent%60).round(2)} SECONDS")

print("\nTOP 10 ARTISTS BY SONGS PLAYED")
print(df['master_metadata_album_artist_name'].value_counts().head(10))

print("\nTOP 10 ARTISTS BY PLAYTIME")
print((df.groupby('master_metadata_album_artist_name')['sec_played'].sum().sort_values(ascending=False).head(10) / 3600).round(2))

print("\nTOP 10 SONGS BY TIMES PLAYED")
print(df[['master_metadata_track_name', 'master_metadata_album_artist_name']].value_counts().head(10))

