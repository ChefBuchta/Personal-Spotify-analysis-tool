import streamlit as st
import plotly.express as px
from main import SpotifyAnalyzer

st.set_page_config(page_title="Spotify Dashboard", layout="wide")

st.title("Spotify Data Analyzer")
st.write("Upload your JSON files from Spotify Privacy download.")

files = st.file_uploader("Upload files Streaming_History_Audio...", accept_multiple_files=True)

if files:
    analyzer = SpotifyAnalyzer("Martin", "Horak", uploadedFiles=files)
    
    # Basic metrics
    col_a, col_b, col_c = st.columns(3)
    col_a.metric("Total Hours", analyzer.getHoursSpentListening('All'))
    col_b.metric("Unique Artists", analyzer.df['artist_name'].nunique())
    col_c.metric("Unique Tracks", analyzer.df['track_name'].nunique())


    # Interactive buttons for input   
    c1, c2 = st.columns(2)
    with c1:
        years = sorted(analyzer.df['year'].unique().tolist(), reverse = True)
        selectedYear = st.selectbox("Time frame:", ["All"] + [str(y) for y in years])
    with c2:
        count = st.slider("How many", 5, 30, 10)
    
    st.divider()

    col11, col12 = st.columns(2)

    # Shows top 'Artists' based on input
    with col11:
        st.subheader(f"TOP {count}: Artists ({selectedYear})")

        data = analyzer.getTopStatsPerYearWithOpt(count, selectedYear, 'Artists').reset_index()
        data.columns = ['Artists', 'Play count']
        
        dynHeight = 300 + (count * 25)
        figBar = px.bar(
            data, 
            x = 'Play count',
            y = 'Artists',
            orientation = 'h', 
            color = 'Play count',
            color_continuous_scale = 'Greens')
        figBar.update_layout(yaxis = {'categoryorder':'total ascending'},
                             height = dynHeight )

        st.plotly_chart(figBar, use_container_width = True)

    # Shows top 'Songs' based on input
    with col12:
        st.subheader(f"TOP {count}: Songs ({selectedYear})")

        data = analyzer.getTopStatsPerYearWithOpt(count, selectedYear, 'Songs').reset_index()
        data.columns = ['Songs', 'Play count']
        
        dynHeight = 300 + (count * 25)
        figBar = px.bar(
            data, 
            x = 'Play count',
            y = 'Songs',
            orientation = 'h', 
            color = 'Play count',
            color_continuous_scale = 'Greens')
        figBar.update_layout(yaxis = {'categoryorder':'total ascending'},
                             height = dynHeight )

        st.plotly_chart(figBar, use_container_width = True)


    st.divider()

    col21, col22 = st.columns(2)

    # Shows top 'Albums' based on input
    with col21:
        st.subheader(f"TOP {count}: Albums ({selectedYear})")

        data = analyzer.getTopStatsPerYearWithOpt(count, selectedYear, 'Albums').reset_index()
        data.columns = ['Albums', 'Play count']
        
        dynHeight = 300 + (count * 25)
        figBar = px.bar(
            data, 
            x = 'Play count',
            y = 'Albums',
            orientation = 'h', 
            color = 'Play count',
            color_continuous_scale = 'Greens')
        figBar.update_layout(yaxis = {'categoryorder':'total ascending'},
                             height = dynHeight )

        st.plotly_chart(figBar, use_container_width = True)


    # If year is selected shows bar graph of all months
    # otherwise show the top unique months
    with col22:
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
    

    #TODO
    # Shows top 'Listening hours' based on input as a heatbar 
    col31, col32 = st.columns(2)
    with col31:
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
    

    # Shows top 'Podcasts' based on input as a bar chart
    with col32:
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










