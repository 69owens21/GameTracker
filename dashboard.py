import streamlit as st
import pandas as pd
import sqlite3

# Setup streamlit page configuration
st.set_page_config(page_title="Game Tracker", layout="wide")
st.title("Cross-Platform Game Tracker")

# Connect to database
@st.cache_data # This keeps the dashboard fast by not querying the DB on every click
def load_data():
    conn = sqlite3.connect('GameTracker.sqlite')

    # One master query using a LEFT JOIN to get games AND their session times
    query = """
        SELECT
            g.title AS Game,
            p.name AS Platform,
            o.format AS Format,
            -- Calculate hours played and round to 2 decimals
            ROUND(SUM((JULIANDAY(s.end_time) - JULIANDAY(s.start_time)) * 24), 2) AS HoursPlayed
        FROM game_ownership o
        JOIN games g ON o.game_id = g.game_id
        JOIN Platforms p ON o.platform_id = p.platform_id
        LEFT JOIN session s ON o.ownership_id = s.ownership_id
        GROUP BY g.title, p.name, o.format
    """

    df = pd.read_sql_query(query, conn)
    conn.close()

    # If a game has no logged sessions, fill the blank (NaN) with 0 hours
    df['HoursPlayed'] = df['HoursPlayed'].fillna(0)

    return df

# Load data
df = load_data()

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Format Breakdown")
    # count games owned in each formats
    format_counts = df['Format'].value_counts()
    st.bar_chart(format_counts)

with col2:
    st.subheader("Platform Distribution")
    # count games on each platform
    platform_counts = df['Platform'].value_counts()
    st.bar_chart(platform_counts)

with col3:
    st.subheader("Time Played (Hours)")
    # Filter out games with 0 hours, sort by most played, and grab the top 10
    played_games = df[df['HoursPlayed'] > 0].sort_values(by='HoursPlayed', ascending=False).head(10)

    # Draw the chart using our calculated 'HoursPlayed' column
    st.bar_chart(data=played_games, x='Game', y='HoursPlayed')

# raw data table
st.subheader("Raw Telemetry Data")

# search/filter
platform_filter = st.selectbox("Filter by Platform", ["All"] + list(df['Platform'].unique()))

if platform_filter == "All":
    st.dataframe(df, use_container_width=True)
else:
    st.dataframe(df[df['Platform'] == platform_filter], use_container_width=True)