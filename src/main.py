import pandas as pd
import glob 
class SpotifyAnalyzer:
    def __init__(self, path: str, fName: str, sName: str):
        self.fName = fName
        self.sName = sName 

        # DF INPUT 
        path = 'data/Streaming_History_Audio*.json'
        files = glob.glob(path)
        dfList = [pd.read_json(f) for f in files]
        self.df = pd.concat(dfList, ignore_index=True)

        # CLEANING 
        self.df = self.df.drop(columns=["ip_addr", "spotify_track_uri", "platform", "offline_timestamp", "conn_country", "offline", "incognito_mode", "episode_name", "episode_show_name", "spotify_episode_uri", "audiobook_title", "audiobook_chapter_uri", "audiobook_chapter_title"])
        self.df['ts'] = pd.to_datetime(self.df['ts'])

        self.df["ms_played"] = self.df['ms_played'] / 1000
        self.df.rename(columns={'ms_played': 'sec_played', 'master_metadata_album_artist_name': 'artist_name','master_metadata_track_name': "track_name" }, inplace=True)

    # PRINTS TIME SPENT LISTENING SUM
    def printTimeSpentListening(self) -> None:
        timeSpent = self.df["sec_played"].sum()
        print(f"TIME SPENT LISTENING {(timeSpent/3600).round(2)} HOURS {((timeSpent/60)%60).round(2)} MINUTES {(timeSpent%60).round(2)} SECONDS")

    # RETURNS THE TOP 10 ARTIST BY NUMBER OF PLAYS 
    def getTop10ArtistBySongs(self) -> pd.DataFrame:
        return self.df['artist_name'].value_counts().head(10)  

    # PRINTS THE TOP 10 ARTIST BY NUMBER OF PLAYS
    def printTop10ArtistBySongs(self):
        artists = self.getTop10ArtistBySongs()
        print("\nTOP 10 ARTISTS BY SONGS PLAYED")
        print(artists)

    # RETURNS THE TOP 10 SONGS BY PLAYTIME 
    def getTop10ArtistByPlay(self) -> pd.DataFrame:
        return (self.df.groupby('artist_name')['sec_played'].sum().sort_values(ascending=False).head(10) / 3600).round(2)

    # PRINTS THE TOP 10 SONGS BY PLAYTIME 
    def printTop10ArtistBySongs(self):
        artists = self.getTop10ArtistByPlay()
        print("\nTOP 10 ARTISTS BY PLAYTIME")
        print(artists)

    # RETURNS THE TOP 10 SONGS BY PLAYTIME 
    def getTop10SongsByPlay(self) -> pd.DataFrame:
        return self.df[['track_name', 'artist_name']].value_counts().head(10) 

    # PRINTS THE TOP 10 SONGS BY PLAYTIME 
    def printTop10SongsByPlay(self) -> pd.DataFrame:
        songs = self.getTop10SongsByPlay()
        print("\nTOP 10 SONGS BY TIMES PLAYED")
        print(songs)

