import streamlit as st
import plotly.express as px
from main import SpotifyAnalyzer

st.set_page_config(page_title="Spotify Dashboard", layout="wide")

st.title("Spotify Data Analyzer")
st.write("Upload your JSON files from Spotify Privacy download.")

files = st.file_uploader("Upload files Streaming_History_Audio...", accept_multiple_files=True)


if files:
    analyzer = SpotifyAnalyzer("Martin", "Horak", uploadedFiles=files)
    
    st.header("Basic overview")
    time_spent = analyzer.df["sec_played"].sum()
    st.metric("Time spent", (time_spent/3600).round(1))
    
    st.header("Time analysis")
    
    count = st.slider("How many TOP picks do you want to see?", 5, 20, 10)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("TOP Artists")
        top_artists = analyzer.getTopArtistBySongs(count).reset_index()
        fig = px.bar(top_artists, x='count', y='artist_name', orientation='h', 
                     color='count', color_continuous_scale='Greens')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("TOP months")
        top_months = analyzer.getTopUniqueMonths(count).reset_index()
        top_months['month'] = top_months['month'].astype(str)
        fig_months = px.line(top_months, x='month', y='plays_count', markers=True)
        st.plotly_chart(fig_months, use_container_width=True)
