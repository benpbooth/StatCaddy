import requests
import pandas as pd
from io import StringIO

def get_live_leaderboard(): 

    params = {
        #ALL PARAMETERS:['event_name', 'last_update', 'current_round', 'dead_heat_rules', 'dg_id',
        # 'country', 'player_name', 'round', 'course', 'current_pos', 'current_score', 'thru', 'today',
        # 'end_hole', 'make_cut', 'top_20', 'top_10', 'top_5', 'win', 'R1', 'R2', 'R3', 'R4']
        "tour": "pga",
        "dead_heat": "true",
        "odds_format": "percent",
        "file_format": "csv",
        "key": "bef1acff9e6e5e6f132207904ea3"
    }
    
    # API endpoint
    url = "https://feeds.datagolf.com/preds/in-play"
    
    # Make request
    response = requests.get(url, params=params)
    
    # Check response status
    if response.status_code == 200:
        # Parse the CSV response into a Pandas DataFrame
        data = pd.read_csv(StringIO(response.text))
    
        # Display the first few rows of the DataFrame
        print("Preview of Data:")
        print(data.head())
    
        # Save the data locally as a CSV file
        #data.to_csv("in_play_predictions.csv", index=False)
        #print("Data saved to in_play_predictions.csv")
    else:
        # Handle errors
        print(f"Error {response.status_code}: {response.text}")
    

get_live_leaderboard()
