import requests
import pandas as pd
from io import StringIO

#This script returns a detailed breakdown of every player's strokes-gained prediction for upcoming PGA and European Tour tournaments.

url = "https://feeds.datagolf.com/preds/player-decompositions"

# Define the parameters
params = {
    "tour": "pga",  # Options: "pga" (default), "euro", "opp", "alt"
    "file_format": "csv",  # Options: "csv" or "json" (default is "json")
    "key": "bef1acff9e6e5e6f132207904ea3"  # Replace with your actual API key
}

# Make the API request
response = requests.get(url, params=params)

# Check the response status code
if response.status_code == 200:
    if params["file_format"] == "csv":
        # Parse the CSV response into a Pandas DataFrame
        data = pd.read_csv(StringIO(response.text))

        # Display the first few rows of the DataFrame
        print("Preview of Player Skill Decompositions Data:")
        print(data.head())

        # Save the data to a CSV file
        file_name = "player_skill_decompositions.csv"
        data.to_csv(file_name, index=False)
        print(f"Data saved to {file_name}")
    else:
        # For JSON responses
        data = response.json()
        print("Preview of JSON Data:")
        print(data)  # Display the JSON response
else:
    print(f"Error {response.status_code}: {response.text}")
