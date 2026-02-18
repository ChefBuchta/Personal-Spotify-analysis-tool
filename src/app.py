import streamlit as st
import plotly.express as px
from main import SpotifyAnalyzer

st.set_page_config(page_title="Spotify Dashboard", layout="wide")

st.title("Spotify Data Analyzer")
st.write("Upload your JSON files from Spotify Privacy download.")

files = st.file_uploader("Upload files Streaming_History_Audio...", accept_multiple_files=True)

if files:
    analyzer = SpotifyAnalyzer("Martin", "Horak", uploadedFiles=files)
 
    col_a, col_b, col_c = st.columns(3)
    col_a.metric("Total Hours", analyzer.getHoursSpentListening('All'))
    col_b.metric("Unique Artists", analyzer.df['artist_name'].nunique())
    col_c.metric("Unique Tracks", analyzer.df['track_name'].nunique())

    c1, c2, c3 = st.columns(3)
    
    with c1:
        years = sorted(analyzer.df['year'].unique().tolist(), reverse = True)
        selectedYear = st.selectbox("Time frame:", ["All"] + [str(y) for y in years])
    with c2:
        viewType = st.selectbox("View TOP", ["Artists", "Songs", "Albums"])

    with c3:
        count = st.slider("How many", 5, 30, 10)
    
    st.divider()

    col11, col12 = st.columns(2)
    
    with col11:
        st.subheader(f"TOP {count}: Artists ({selectedYear})")

        data = analyzer.getTopStatsPerYearWithOpt(count, selectedYear, viewType).reset_index()
        data.columns = [viewType, 'Play count']
        
        dynHeight = 300 + (count * 25)
        figBar = px.bar(
            data, 
            x = 'Play count',
            y = viewType,
            orientation = 'h', 
            color = 'Play count',
            color_continuous_scale = 'Greens')
        figBar.update_layout(yaxis = {'categoryorder':'total ascending'},
                             height = dynHeight )

        st.plotly_chart(figBar, use_container_width = True)

    with col12:
        st.subheader(f"Listening Activity ({selectedYear})")

        hoursSpent = analyzer.getHoursSpentListening(selectedYear)

        st.write(f"Time spent listening **{hoursSpent}** hours") 
        

        monthData = analyzer.getTopMonthsByTime(selectedYear, count)
         
        figMonths = px.bar(
            monthData,
            x = 'Month',
            y = 'hours_played',
            color = 'hours_played',
            labels = {'Month': 'Period', 'hours_played':'Hours listened'},
            color_continuous_scale = 'Greens')

        figMonths.update_layout(height=450)
        
        if selectedYear == 'All':
            figMonths.update_xaxes(type='category')
        else:
            figMonths.update_xaxes(categoryorder='array', 
                                    categoryarray=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                                                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
        
        st.plotly_chart(figMonths, use_container_width=True)
    
    st.divider()

    col3, col4 = st.columns(2)
    
    with col3:
        st.subheader(f"You've listened the most during these hours")

        data = analyzer.getTopHours(selectedYear, count)
        
        data.columns = ['Hour', 'Play count']
        data['Hour'] = data['Hour'].astype(str) + ":00"

        figBar = px.bar(
            data,
            x = 'Play count',
            y = 'Hour',
            orientation = 'h',
            color = 'Play count',
            color_continuous_scale = 'Greens')

        figBar.update_layout(yaxis = {'categoryorder':'total ascending'},
                             height = dynHeight )

        st.plotly_chart(figBar, use_container_width = True)

    with col4:
        st.subheader(f"Your most listened podcasts")

        data = analyzer.getTopPodcasts(selectedYear, count)

        data.columns = ['Podcast name', 'Hours spent']

        figPodcasts = px.bar(
            data,
            x = 'Hours spent',
            y = 'Podcast name',
            color = 'Hours spent', 
            color_continuous_scale = 'Greens')

        figPodcasts.update_layout(yaxis = {'categoryorder':'total ascending'},
                             height = dynHeight )

        st.plotly_chart(figPodcasts, use_container_width = True)










