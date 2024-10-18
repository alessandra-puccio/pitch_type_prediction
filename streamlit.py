import streamlit as st
import pandas as pd
import json
import os
import matplotlib.pyplot as plt

# Load player names from data.csv
data = pd.read_csv('data.csv')
player_names = data['PLAYER_NAME'].tolist()

# Load predictions
predictions = pd.read_csv('predictions.csv')

# Function to load player stats for a given year and pitch type
# Load player stats from JSON files
def load_player_stats(year, pitch_type):
    filename = f'PLAYER_STATS_{pitch_type}_{year}.json'
    with open(filename, 'r') as f:
        data = [json.loads(line) for line in f.readlines()]
    return pd.DataFrame(data)

# Streamlit app
st.title('Player Pitch Type Predictions')

# Player selection dropdown
selected_player = st.selectbox('Select a Player', player_names)

# Get the BATTER_ID for the selected player
batter_id = data[data['PLAYER_NAME'] == selected_player]['BATTER_ID'].values[0]

# Initialize lists for storing values
years = [2021, 2022, 2023]
pitches = ['OS', 'FB', 'BB']

# Iterate through each pitch type to gather data
# Iterate through each pitch type to gather data
for pitch in pitches:  # Make sure you're using pitch_types as previously defined
    received_percentages = []
    avg_isos = []
    avg_babips = []
    avg_wobas = []

    for year in years:
        stats = load_player_stats(year, pitch)
        
        # Check if the stats DataFrame is not empty
        if not stats.empty:
            # Check if the player's BATTER_ID is in the stats DataFrame
            if batter_id in stats['BATTER_ID'].values:
                player_stats = stats[stats['BATTER_ID'] == batter_id]
                received_percentages.append(player_stats['PERC_RECEIVED'].values[0])
                avg_isos.append(player_stats['AVG_ISO'].values[0])
                avg_babips.append(player_stats['AVG_BABIP'].values[0])
                avg_wobas.append(player_stats['AVG_WOBA_HIT_INTO_PLAY'].values[0])
            else:
                # If the player is not found, append zeros
                received_percentages.append(0)
                avg_isos.append(0)
                avg_babips.append(0)
                avg_wobas.append(0)
        else:
            # If the JSON file does not contain any data, append zeros
            received_percentages.append(0)
            avg_isos.append(0)
            avg_babips.append(0)
            avg_wobas.append(0)

    # Now you have collected data for this pitch type, and you can continue with your plotting code


    # Retrieve the predicted percentage for 2024
    prediction_row = predictions[predictions['BATTER_ID'] == batter_id]
    if not prediction_row.empty:
        predicted_percentage = prediction_row[f'PITCH_TYPE_{pitch}'].values[0]
    else:
        predicted_percentage = 0  # No prediction available

    # Prepare data for plotting
    years_labels = [str(year) for year in years] + ['2024']
    received_percentages.append(predicted_percentage)
    
    # Create the plot
    fig, ax1 = plt.subplots(figsize=(10, 6))
    ax2 = ax1.twinx()  # Create a second y-axis for lines

    # Bar plot for received percentages
    ax1.bar(years_labels, received_percentages, color=['blue'] * 3 + ['orange'], label='Received Percentage')

    # Line plots for AVG_ISO, AVG_BABIP, and AVG_WOBA
    ax2.plot(years_labels[:-1], avg_isos, color='green', marker='o', label='AVG ISO')
    ax2.plot(years_labels[:-1], avg_babips, color='red', marker='o', label='AVG BABIP')
    ax2.plot(years_labels[:-1], avg_wobas, color='purple', marker='o', label='AVG WOBA')

    # Adding labels and legends
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Received Percentage (%)', color='black')
    ax2.set_ylabel('Average Metrics', color='black')
    ax1.set_title(f'{selected_player} - Pitch Type: {pitch}')
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')

    # Show the plot in the Streamlit app
    st.pyplot(fig)
