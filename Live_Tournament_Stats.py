import requests
import pandas as pd
from io import StringIO

# Define the API parameters
params = {
    "stats": "sg_putt,sg_arg,sg_app,sg_ott,sg_t2g,sg_bs,sg_total",
    "round": "1",  # Specify the round (1, 2, 3, 4, or event_avg)
    "display": "value",  # How stats are displayed: "value" or "rank"
    "file_format": "csv",
    "key": "bef1acff9e6e5e6f132207904ea3"
}

# Define the API endpoint
url = "https://feeds.datagolf.com/preds/live-tournament-stats"

# Make the API request
response = requests.get(url, params=params)

# Check the response status code
if response.status_code == 200:
    # Parse the CSV response into a Pandas DataFrame
    data = pd.read_csv(StringIO(response.text))

    # Display the first few rows of the DataFrame
    print("Preview of Live Tournament Stats:")
    print(data.head())

    # Save the data to a CSV file
    data.to_csv("live_tournament_stats.csv", index=False)
    print("Live tournament stats saved to live_tournament_stats.csv")
else:
    # Handle errors
    print(f"Error {response.status_code}: {response.text}")


