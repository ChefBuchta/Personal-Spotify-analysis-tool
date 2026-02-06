import pandas as pd
import glob 

class SpotifyAnalyzer:
    def __init__(self, folderPath: str, fName: str, sName: str) -> None:
        self.fName = fName
        self.sName = sName 
        
        path = f'{folderPath}/Streaming_History_Audio*.json'
        files = glob.glob(path)

        if not files:
            raise FileNotFoundError("Couldn't find")

        # Raw nputs files into a list and the concats them together into a single Data Frame 
        dfList = [pd.read_json(f) for f in files]
        self.df = pd.concat(dfList, ignore_index=True)

        # Prepares data
        self._preprocesData()
        
    def _preprocesData(self):
        """Internal method for cleaning and transformation of data"""

        self.df = self.df.drop(columns=["ip_addr", "spotify_track_uri", "platform", "offline_timestamp", "conn_country", "offline", "incognito_mode", "episode_name", "episode_show_name", "spotify_episode_uri", "audiobook_title", "audiobook_chapter_uri", "audiobook_chapter_title"])
        self.df['ts'] = pd.to_datetime(self.df['ts'])

        self.df['month'] = self.df['ts'].dt.to_period('M')
        self.df['hour'] = self.df['ts'].dt.hour

        
        self.df["ms_played"] = self.df['ms_played'] / 1000
        self.df.rename(columns={'ms_played': 'sec_played', 
                                'master_metadata_album_artist_name': 'artist_name',
                                'master_metadata_track_name': "track_name",
                                "master_metadata_album_album_name": "album_name",
                                }, 
                       inplace=True)

        self.df['track_with_artist'] = self.df["track_name"] + ' - ' + self.df["artist_name"]
    
    def printTimeSpentListening(self) -> None:
        """Prints the play time."""
        timeSpent = self.df["sec_played"].sum()
        print(f"TIME SPENT LISTENING {(timeSpent/3600).round(2)} HOURS {((timeSpent/60)%60).round(2)} MINUTES {(timeSpent%60).round(2)} SECONDS")

    def getTopArtistBySongs(self, count: int = 5) -> pd.DataFrame:
        """Returns top 'count' Artist by number of song plays."""
        if count < 1:
            raise ValueError("Add valid count number")

        return self.df['artist_name'].value_counts().head(count)  

    def printTop10ArtistBySongs(self, count: int = 5) -> None:
        """Prints top 'count' artist by number of song plays."""
        if count < 1:
            raise ValueError("Add valid count number")

        artists = self.getTopArtistBySongs(count)
        print(f"\nTOP {count} ARTISTS BY SONGS PLAYED")
        print(artists)

    def getTopArtistByPlay(self, count: int = 5) -> pd.DataFrame:
        """Returns top 'count' Artist by number of time spent listening."""
        if count < 1:
            raise ValueError("Add valid count number")

        return (self.df.groupby('artist_name')['sec_played'].sum().sort_values(ascending=False).head(count) / 3600).round(2)

    def printTopArtistByPlay(self, count: int = 5) -> None:
        """Prints top 'count' Artist by number of time spent listening."""
        if count < 1:
            raise ValueError("Add valid count number")

        artists = self.getTopArtistByPlay(count)
        print(f"\nTOP {count} ARTISTS BY PLAYTIME")
        print(artists)

    def getTopSongsByPlay(self, count: int = 5) -> pd.DataFrame:
        """Returns top 'count' songs by number of plays."""
        if count < 1:
            raise ValueError("Add valid count number")

        return self.df[['track_name', 'artist_name']].value_counts().head(count) 


    def printTopSongsByPlay(self, count: int = 5) -> None:
        """Prints top 'count' songs by number of plays."""
        if count < 1:
            raise ValueError("Add valid count number")

        
        print(f"\nTOP {count} SONGS BY TIMES PLAYED")
        print(self.getTopSongsByPlay(count))
    
    def getTopHours(self, count: int = 5) -> pd.DataFrame:
        """Returns top 'count' hours in a day, with most plays"""
        if count < 1 or count > 24:
            raise ValueError("Add valid count number")

        return self.df['hour'].value_counts().head(count)

    def printTopHours(self, count: int = 5) -> None:
        """Prints top 'count' hours in a day, with most plays"""
        if count < 1 or count > 24:
            raise ValueError("Add valid count number")

        print(f"\nTOP {count} HOURS IN A DAY BY SONGS PLAYED")
        print(self.getTopHours(count)
)

    def getTopMonths(self, count: int = 5) -> pd.DataFrame:
        """Returns top 'count' months, with most plays"""
        if count < 1 or count > 12:
            raise ValueError("Add valid count number")

        return self.df['ts'].dt.month.value_counts().head(count)

    def printTopMonths(self, count: int = 5) -> None:
        """Months top 'count' months, with most plays"""
        if count < 1 or count > 12:
            raise ValueError("Add valid count number")

        print(f"\nTOP {count} MONTHS BY SONGS PLAYED")
        print(self.getTopMonths(count))


    def getTopUniqueMonths(self, count: int = 5) -> pd.DataFrame:
        """Returns top 'count' unique months, with most plays"""
        if count < 1:
            raise ValueError("Add valid count number")

        result = self.df.groupby('month').agg(plays_count = ('track_name', 'count'), 
                                              top_artist = ('artist_name', lambda x: x.value_counts().idxmax()), 
                                              top_track = ('track_with_artist', lambda x: x.value_counts().idxmax()))
        return result.sort_values('plays_count', ascending=False).head(count)

    def printTopUniqueMonths(self, count: int = 5) -> None:
        """Months top 'count' unique months, with most plays"""
        if count < 1:
            raise ValueError("Add valid count number")

        months = self.getTopUniqueMonths(count)
        print(f"\nTOP {count} UNIQUE MONTHS BY SONGS PLAYED")
        print(months)
    
    def getTopAlbums(self, count):
        """ Returns top 'count' top listened albums by songs played """
        if count < 1:
            raise ValueError("Add valid count number")
        return self.df['album_name'].value_count().head(count) 

    def printTopAlbums(self, count):
        """ Print top 'count' top listened albums by songs played """
        if count < 1:
            raise ValueError("Add valid count number")


        print(f"\nTOP {count} ALBUMS BY SONGS PLAYED")
        print(self.getTopAlbums(count))


MyTop = SpotifyAnalyzer("data", 'Martin', "Horak")
print(MyTop.printTopUniqueMonths(12))
print(MyTop.printTopAlbums(10))
