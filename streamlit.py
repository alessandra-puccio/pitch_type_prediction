import streamlit as st
import pandas as pd
import json
import os
import matplotlib.pyplot as plt

# Load player names from data.csv
data = pd.read_csv('data.csv')
player_names = data['PLAYER_NAME'].unique().tolist()

# Load predictions
predictions = pd.read_csv('predictions.csv')

# Function to load player stats for a given year and pitch type
def load_player_stats(year, pitch_type):
    folder_path = 'player_stat_files'  # The folder where all your player stat files are stored
    filename = f'PLAYER_STATS_{pitch_type}_{year}.json'
    file_path = os.path.join(folder_path, filename)
    
    with open(file_path, 'r') as f:
        data = [json.loads(line) for line in f.readlines()]
        
    return pd.DataFrame(data)


# Streamlit app
st.title('Player Pitch Type Predictions')

default_index = player_names.index("Benintendi, Andrew")
# Player selection dropdown with default set to "Benintendi, Andrew"
selected_player = st.selectbox('Select a Player', player_names, index=default_index)


# Get the BATTER_ID for the selected player
batter_id = data[data['PLAYER_NAME'] == selected_player]['BATTER_ID'].values[0]

# Initialize lists for storing values
years = [2021, 2022, 2023]
pitches = ['OS', 'FB', 'BB']

# Iterate through each pitch type to gather data
for pitch in pitches:  # Make sure you're using pitch_types as previously defined
    received_percentages = []
    avg_isos = []
    avg_babips = []
    avg_wobas = []
    valid_years = []  # Track years with valid data

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
                valid_years.append(str(year))  # Append year only when data exists
           
    # Retrieve the predicted percentage for 2024
    prediction_row = predictions[predictions['BATTER_ID'] == batter_id]
    if not prediction_row.empty:
        predicted_percentage = prediction_row[f'PITCH_TYPE_{pitch}'].values[0]
        received_percentages.append(predicted_percentage)
        valid_years.append('2024')  # Add 2024 for the predicted percentage
    
    # Prepare data for plotting
    # Create the plot
    fig, ax1 = plt.subplots(figsize=(10, 6))
    ax2 = ax1.twinx()  # Create a second y-axis for lines
    
    # Bar plot for received percentages
    ax1.bar(valid_years[:-1], received_percentages[:-1], color='blue', label='Received Percentage')
    ax1.bar(valid_years[-1], received_percentages[-1], color='orange', label='Predicted Percentage')

    # Line plots for AVG_ISO, AVG_BABIP, and AVG_WOBA (only for valid years)
    ax2.plot(valid_years[:-1], avg_isos, color='green', marker='o', label='AVG ISO')
    ax2.plot(valid_years[:-1], avg_babips, color='red', marker='o', label='AVG BABIP')
    ax2.plot(valid_years[:-1], avg_wobas, color='purple', marker='o', label='AVG WOBA')

    # Adding labels and legends
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Received Percentage (%)', color='black')
    ax2.set_ylabel('Average Metrics', color='black')
    ax1.set_title(f'{selected_player} - Pitch Type: {pitch}')
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')

    # Show the plot in the Streamlit app
    st.pyplot(fig)
