import pandas as pd
import glob 

class SpotifyAnalyzer:
    def __init__(self, fName: str, sName: str, uploadedFiles = None, folderPath: str = None) -> None:
        self.fName = fName
        self.sName = sName 

        if uploadedFiles:
            dfList = [pd.read_json(f) for f in uploadedFiles if f.name.endswith('.json')]
        elif folderPath:
            path = f"{folderPath}/Streaming_History_Audio*.json"
            files = glob.glob(path)
            dfList = [pd.read_json(f) for f in files]
        else:
            raise FileNotFoundError("Couldn't find")

        self.df = pd.concat(dfList, ignore_index=True)
        self._preprocesData()
        
    def _preprocesData(self):
        """Internal method for cleaning and transformation of data"""

        self.df = self.df.drop(columns=["ip_addr", "spotify_track_uri", "platform", "offline_timestamp", "conn_country", "offline", "incognito_mode", "episode_name", "episode_show_name", "spotify_episode_uri", "audiobook_title", "audiobook_chapter_uri", "audiobook_chapter_title"])
        self.df['ts'] = pd.to_datetime(self.df['ts'])
        
        self.df['year'] = self.df['ts'].dt.year # 2026
        self.df['month'] = self.df['ts'].dt.to_period('M') # 2026-1 etc.
        self.df['hour'] = self.df['ts'].dt.hour # 19, 12

        
        self.df["ms_played"] = self.df['ms_played'] / 1000
        self.df.rename(columns={'ms_played': 'sec_played', 
                                'master_metadata_album_artist_name': 'artist_name',
                                'master_metadata_track_name': "track_name",
                                "master_metadata_album_album_name": "album_name",
                                }, 
                       inplace=True)

        self.df['track_with_artist'] = self.df["track_name"] + ' - ' + self.df["artist_name"]
        self.df['album_with_artist'] = self.df["album_name"] + ' - ' + self.df["artist_name"]
    
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
        return self.df['album_with_artist'].value_counts().head(count) 

    def printTopAlbums(self, count):
        """ Print top 'count' top listened albums by songs played """
        if count < 1:
            raise ValueError("Add valid count number")


        print(f"\nTOP {count} ALBUMS BY SONGS PLAYED")
        print(self.getTopAlbums(count))

    def getStatsPerYear(self, count: int = 5) -> pd.DataFrame:
        """ Return top artist, song, album, time listened per year """   
        if count < 1:
            raise ValueError("Add valid count number")

        result = self.df.groupby('year').agg(plays_count = ('track_name', 'count'), 
                                              top_artist = ('artist_name', lambda x: x.value_counts().idxmax()), 
                                              top_track = ('track_with_artist', lambda x: x.value_counts().idxmax()),
                                              top_album = ('album_name', lambda x: x.value_counts().idxmax()),
                                             time_spent = ('sec_played', lambda x: (x.sum() / 3600).round(2)))

        return result.sort_values('year', ascending=False).head(count)

    # ---------------------------------------------------------------------------------------------------------
    # Actually using these in frontend
    # Rest was testing
    def getTopStatsPerYearWithOpt(self, count: int = 10, year: str = "All", opt: str = "Artists") -> pd.DataFrame: 
        """ Returns DataFrame based on time period(year) and view option(opt) and top n (count)"""
        dfF = self.df.copy() 
        if year != "All":
            dfF = dfF[dfF['year'] == int(year)]
        
        map = {"Artists":'artist_name',
                   "Songs":"track_with_artist",
                   "Albums":"album_with_artist"}
        col = map.get(opt, "artist_name")

        return dfF[col].value_counts().head(count)  
        
    def getTopMonthsByTime(self, year: str = 'All', count: int = 10) -> pd.DataFrame:
        """
            With year = 'All', returns top unique months based of most time spent listening and top n count
            with year != 'All' returns all months with their listening time, sorted in standard order 
        """
        dfF = self.df.copy() 

        if year != "All":
            dfF = dfF[dfF['year'] == int(year)]
            result = dfF.groupby(dfF['ts'].dt.month).agg(hours_played = ('sec_played', lambda x: (x.sum() / 3600).round(2))).reset_index()

            result.columns = ['month_num', 'hours_played']

            monthMap = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 
                       7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
            result['Month'] = result['month_num'].map(monthMap)

            return result.sort_values('month_num')
        else:
            result = self.df.groupby('month').agg(hours_played = ('sec_played', lambda x: (x.sum() / 3600).round(2))).reset_index()

            result.columns = ['Month', 'hours_played']
            result['Month'] = result['Month'].astype(str)

            return result.sort_values('hours_played', ascending = False).head(count)

    def getHoursSpentListening(self, year: str = 'All') -> float:
        """ Returns hours spent listening, based on time frame """
        if year != 'All':
            timeSpent = self.df[self.df['year'] == int(year)]['sec_played'].sum() 
            return (timeSpent / 3600).round(2)
        else:
            timeSpent = self.df['sec_played'].sum() 
            return (timeSpent / 3600).round(2)













