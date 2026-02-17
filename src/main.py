import pandas as pd
import glob 

class SpotifyAnalyzer:
    def __init__(self, fName: str, sName: str, uploadedFiles = None, folderPath: str = None) -> None:
        self.fName = fName
        self.sName = sName 

        if uploadedFiles:
            # Songs
            dfList = [pd.read_json(f) for f in uploadedFiles if f.name.endswith('.json') and f.name.startswith('Streaming_History_Audio')]

            # Albums
            dfPodcastList = [pd.read_json(f) for f in uploadedFiles if f.name.endswith('.json') and f.name.startswith('Streaming_History_Video')]

        elif folderPath:
            # Songs
            path = f"{folderPath}/Streaming_History_Audio*.json"
            files = glob.glob(path)
            dfList = [pd.read_json(f) for f in files]

            # Albums
            podcastPath = f"{folderPath}/Streaming_History_Video*.json"
            podcastFiles = glob.glob(podcastPath)
            dfList = [pd.read_json(f) for f in files]



        else:
            raise FileNotFoundError("Couldn't find")

        self.df = pd.concat(dfList, ignore_index=True)
        self.podcastDf = pd.concat(dfPodcastList, ignore_index=True)
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

    def getTopHours(self, year: str = 'All', count: int = 5) -> pd.DataFrame:
        """Returns top 'count' hours in a day, with most plays"""

        if count > 24:
            count = 24 

        if year != 'All':
            filterDf = self.df.copy()
            filterDf = filterDf[filterDf['year'] == int(year)]
            result = filterDf['hour'].value_counts().head(count).reset_index()
            return result
        else:
            result = self.df['hour'].value_counts().head(count).reset_index()
            return result













