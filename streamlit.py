import streamlit as st
import pandas as pd
import json
import os
import matplotlib.pyplot as plt

# Load player names from data.csv
data = pd.read_csv('datanames.csv')
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
st.title('Pitch Type Predictions and Analysis')

default_index = player_names.index("Benintendi, Andrew")
# Player selection dropdown with default set to "Benintendi, Andrew"
selected_player = st.selectbox('Select a Player', player_names, index=default_index)

# Get the BATTER_ID for the selected player
batter_id = data[data['PLAYER_NAME'] == selected_player]['BATTER_ID'].values[0]

# Get the predicted percentages for 2024 for each pitch type
prediction_row = predictions[predictions['BATTER_ID'] == batter_id]
if not prediction_row.empty:
    PITCH_TYPE_FB = prediction_row['PITCH_TYPE_FB'].values[0]
    PITCH_TYPE_BB = prediction_row['PITCH_TYPE_BB'].values[0]
    PITCH_TYPE_OS = prediction_row['PITCH_TYPE_OS'].values[0]

    # Data for pie chart
    pitch_types = ['Fastball', 'Breaking Ball', 'Offspeed']
    pitch_type_percentages = [PITCH_TYPE_FB, PITCH_TYPE_BB, PITCH_TYPE_OS]

    st.subheader(f"2024 Predicted Pitch Type Breakdown for {selected_player}")

    # Create a pie chart for the 2024 pitch type breakdown
    fig, ax = plt.subplots()
    ax.pie(pitch_type_percentages, labels=pitch_types, autopct='%1.1f%%', startangle=90, colors=['blue', 'green', 'orange'])
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Display the pie chart above the other visuals
    st.pyplot(fig)


#### TRENDS SECTION 

st.subheader(f"Pitch Type Trends Over the Years for {selected_player}")

# Initialize lists for storing values
years = [2021, 2022, 2023]
pitches = ['OS', 'FB', 'BB']

# Iterate through each pitch type to gather data
for pitch in pitches:
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
    ax1.set_title(f'{pitch} Pitch Type Trends for {selected_player}', fontsize=16)

    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')

    # Show the plot in the Streamlit app
    st.pyplot(fig)


# Initialize variables for storing WOBA and BABIP for each pitch type in the most recent year
bb_recent_woba, bb_recent_babip = None, None
fb_recent_woba, fb_recent_babip = None, None
os_recent_woba, os_recent_babip = None, None

# Iterate through each pitch type to gather data for the most recent year
for pitch in pitches:
    for year in years:
        stats = load_player_stats(year, pitch)
        
        if not stats.empty and batter_id in stats['BATTER_ID'].values:
            player_stats = stats[stats['BATTER_ID'] == batter_id]
            woba = player_stats['AVG_WOBA_HIT_INTO_PLAY'].values[0]
            babip = player_stats['AVG_BABIP'].values[0]
            
            # Store WOBA and BABIP for each pitch type
            if pitch == 'FB':
                fb_recent_woba, fb_recent_babip = woba, babip
            elif pitch == 'BB':
                bb_recent_woba, bb_recent_babip = woba, babip
            elif pitch == 'OS':
                os_recent_woba, os_recent_babip = woba, babip
                
            break  # Exit once the most recent year of data is found
# WOBA and BABIP values for bar chart
woba_values = [fb_recent_woba, bb_recent_woba, os_recent_woba]
babip_values = [fb_recent_babip, bb_recent_babip, os_recent_babip]
valid_pitch_types = ['FB', 'BB', 'OS']  # Fastball, Breaking Ball, Offspeed

st.subheader(f"Areas For Growth: {selected_player}'s Performance Against Each Pitch Type")

# Area for Growth analysis
# Calculate the minimum WOBA and BABIP and corresponding pitch types
min_woba = min(woba_values)
min_babip = min(babip_values)
lowest_woba_pitch = valid_pitch_types[woba_values.index(min_woba)]
lowest_babip_pitch = valid_pitch_types[babip_values.index(min_babip)]

# Area for Growth analysis output

st.markdown(f"""
- **Lowest wOBA**: {min_woba} against {'Fastball' if lowest_woba_pitch == 'FB' else 'Breaking Ball' if lowest_woba_pitch == 'BB' else 'Offspeed'} pitch type.
- **Lowest BABIP**: {min_babip} against {'Fastball' if lowest_babip_pitch == 'FB' else 'Breaking Ball' if lowest_babip_pitch == 'BB' else 'Offspeed'} pitch type.
""")
# Create a bar graph for WOBA and BABIP
fig, ax = plt.subplots(figsize=(8, 6))
bar_width = 0.35
index = range(len(valid_pitch_types))

# Bar plots for WOBA and BABIP
ax.bar(index, woba_values, bar_width, label='WOBA', color='blue')
ax.bar([i + bar_width for i in index], babip_values, bar_width, label='BABIP', color='green')

# Add labels and title
ax.set_xlabel('Pitch Type')
ax.set_ylabel('Metrics')
ax.set_title(f"WOBA and BABIP by Pitch Type (From Most Recently Available Year's Data)")
ax.set_xticks([i + bar_width / 2 for i in index])
ax.set_xticklabels(['Fastball', 'Breaking Ball', 'Offspeed'])
ax.legend()

# Display the bar chart
st.pyplot(fig)


