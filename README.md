# Spotify Personal Analysis Tool

An interactive web application built with **Python**, **Pandas**, and **Streamlit** that turns your Spotify extended streaming history into visual insights. Discover your top artists, tracks, and albums, and visualize your listening habits over the years.

## Features

* **File Upload**: Directly upload your `Streaming_History_Audio_*.json` files exported from Spotify.
* **Dynamic Filtering**: Filter your data by specific years or view your "All Time" history.
* **Top Statistics**: Interactive horizontal bar charts for **Top Artists**, **Songs**, and **Albums**.
* **Listening Activity**: A chronological bar chart showing hours listened per month, helping you see when you were most active.
* **Smart Scaling**: The charts automatically adjust their height and scale based on the number of items you choose to display.
* **Yearly Stats Table**: A detailed breakdown of your top artist, track, album, and total playtime for every year in your history.

## Getting Started

### 1. Prerequisites

* **Python 3.8+**
* Your Spotify Data: Request your "Extended streaming history" from the [Spotify Privacy Settings](https://www.spotify.com/account/privacy/) page (https://www.youtube.com/shorts/A0Pp8iyj5SQ?themeRefresh=1).

### 2. Installation

Clone the repository and set up a virtual environment:

```bash
# Clone the repo
git clone https://github.com/ChefBuchta/Personal-Spotify-analysis-tool.git
cd Personal-Spotify-analysis-tool

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

```
### 3. Dependencies

The project was made using these libraries:

    pandas

    streamlit

    plotly
### 4. Running the App

Launch the Streamlit dashboard from your terminal:

```bash
streamlit run src/app.py

```

## Project Structure

* `src/main.py`: Contains the `SpotifyAnalyzer` class — the engine that handles data cleaning, grouping, and statistical calculations.
* `src/app.py`: The Streamlit frontend script that manages the UI layout, sliders, and Plotly visualizations.
* `.gitignore`: Configured to ignore local data, virtual environments, and sensitive `.env` files.

## Technical Details

The tool uses **Pandas** for heavy data lifting:

* **Aggregation**: Uses `.groupby()` and `.agg()` to find the most-played items and calculate time spent. * **Time Processing**: Converts Spotify timestamps into readable periods (Months, Years, Hours) using `pd.to_datetime`.
* **Visualization**: Uses **Plotly Express** for responsive, interactive charts that support hover-data and dynamic scaling.

## License

Distributed under the MIT License. See `LICENSE` for more information.
