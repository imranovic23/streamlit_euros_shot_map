import json
import streamlit as st
import pandas as pd
from mplsoccer import VerticalPitch

st.title("UEFA Euro 2024 - Shot Map by Imran Nordin™")
st.subheader("Filter by team and player to see all their shot attempts!")

# Load data
df = pd.read_csv('euros_2024_shot_map.csv')
df = df[df['type'] == 'Shot'].reset_index(drop=True)
df['location'] = df['location'].apply(json.loads)

# Team and player filter selection
team = st.selectbox('Select a team', df['team'].sort_values().unique(), index=None)
player = st.selectbox('Select a player', df[df['team'] == team]['player'].sort_values().unique(), index=None)

# Filtering function
def filter_data(df, team, player):
    if team:
        df = df[df['team'] == team]
    if player:
        df = df[df['player'] == player]
    return df

# Get filtered data
filtered_df = filter_data(df, team, player)

# Create the pitch plot
pitch = VerticalPitch(pitch_type='statsbomb', half=True)
fig, ax = pitch.draw(figsize=(10, 10))

# Plot shots function
def plot_shots(df, ax, pitch):
    for x in df.to_dict(orient='records'):
        pitch.scatter(
            x=float(x['location'][0]),
            y=float(x['location'][1]),
            ax=ax,
            s=1000 * x['shot_statsbomb_xg'],
            color='red' if x['shot_outcome'] == 'Goal' else 'white',
            edgecolors='black',
            alpha=1 if x['type'] == 'goal' else .5,
            zorder=2 if x['type'] == 'goal' else 1
        )

# Plot the shots on the pitch
plot_shots(filtered_df, ax, pitch)

# Display the plot
st.pyplot(fig)
