import pandas as pd
import glob 
class SpotifyAnalyzer:
    def __init__(self, folderPath: str, fName: str, sName: str) -> None:
        self.fName = fName
        self.sName = sName 

        path = f'{folderPath}/Streaming_History_Audio*.json'
        files = glob.glob(path)

        if not files:
            raise FileNotFoundError(f"Couldn't find")

        dfList = [pd.read_json(f) for f in files]
        self.df = pd.concat(dfList, ignore_index=True)
        self._preprocesData()
        
    def _preprocesData(self):
        """Internal method for cleaning and transformation of data"""
        self.df = self.df.drop(columns=["ip_addr", "spotify_track_uri", "platform", "offline_timestamp", "conn_country", "offline", "incognito_mode", "episode_name", "episode_show_name", "spotify_episode_uri", "audiobook_title", "audiobook_chapter_uri", "audiobook_chapter_title"])
        self.df['ts'] = pd.to_datetime(self.df['ts'])

        self.df["ms_played"] = self.df['ms_played'] / 1000
        self.df.rename(columns={'ms_played': 'sec_played', 'master_metadata_album_artist_name': 'artist_name','master_metadata_track_name': "track_name" }, inplace=True)

    def printTimeSpentListening(self) -> None:
        """Prints the play time."""
        timeSpent = self.df["sec_played"].sum()
        print(f"TIME SPENT LISTENING {(timeSpent/3600).round(2)} HOURS {((timeSpent/60)%60).round(2)} MINUTES {(timeSpent%60).round(2)} SECONDS")

    def getTop10ArtistBySongs(self) -> pd.DataFrame:
        """Returns top 10 Artist by number of song plays."""
        return self.df['artist_name'].value_counts().head(10)  

    def printTop10ArtistBySongs(self):
        """Prints top 10 artist by number of song plays."""
        artists = self.getTop10ArtistBySongs()
        print("\nTOP 10 ARTISTS BY SONGS PLAYED")
        print(artists)

    def getTop10ArtistByPlay(self) -> pd.DataFrame:
        """Returns top 10 Artist by number of time spent listening."""
        return (self.df.groupby('artist_name')['sec_played'].sum().sort_values(ascending=False).head(10) / 3600).round(2)

    def printTop10ArtistByPlay(self):
        """Prints top 10 Artist by number of time spent listening."""
        artists = self.getTop10ArtistByPlay()
        print("\nTOP 10 ARTISTS BY PLAYTIME")
        print(artists)

    def getTop10SongsByPlay(self) -> pd.DataFrame:
        """Returns top 10 songs by number of plays."""
        return self.df[['track_name', 'artist_name']].value_counts().head(10) 

    def printTop10SongsByPlay(self) -> pd.DataFrame:
        """Prints top 10 songs by number of plays."""
        songs = self.getTop10SongsByPlay()
        print("\nTOP 10 SONGS BY TIMES PLAYED")
        print(songs)

