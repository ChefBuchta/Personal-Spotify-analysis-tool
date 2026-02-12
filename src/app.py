import streamlit as st
import plotly.express as px
from main import SpotifyAnalyzer

st.set_page_config(page_title="Spotify Dashboard", layout="wide")

st.title("Spotify Data Analyzer")
st.write("Upload your JSON files from Spotify Privacy download.")

files = st.file_uploader("Upload files Streaming_History_Audio...", accept_multiple_files=True)

if files:
    analyzer = SpotifyAnalyzer("Martin", "Horak", uploadedFiles=files)
    
    c1, c2, c3 = st.columns(3)

    with c1:
        years = sorted(analyzer.df['year'].unique().tolist(), reverse = True)
        selectedYear = st.selectbox("Time frame:", ["All"] + [str(y) for y in years])
    with c2:
        viewType = st.selectbox("View TOP", ["Artists", "Songs", "Albums"])

    with c3:
        count = st.slider("How many", 5, 30, 10)
    
    st.divider()

    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(f"TOP {count}: {viewType} ({selectedYear})")

        data = analyzer.getTopStatsPerYearWithOpt(count, selectedYear, viewType).reset_index()
        data.columns = [viewType, 'Play count']
        
        dynHeight = 300 + (count * 25)
        figBar = px.bar(data, x = 'Play count', y = viewType, orientation = 'h', 
                        color = 'Play count', color_continuous_scale = 'Greens')
        figBar.update_layout(yaxis = {'categoryorder':'total ascending'},
                             height = dynHeight )

        st.plotly_chart(figBar, use_container_width = True)
