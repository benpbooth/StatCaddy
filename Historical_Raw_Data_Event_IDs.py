import requests
import pandas as pd
from io import StringIO


#This contains historical data of: tour,calendar_year,date,event_name,event_id,sg_categories,traditional_stats
# Define the API endpoint
url = "https://feeds.datagolf.com/historical-raw-data/event-list?file_format=csv&key=bef1acff9e6e5e6f132207904ea3"

# Make the API request
response = requests.get(url)

# Check the response status code
if response.status_code == 200:
    # Parse the CSV response into a Pandas DataFrame
    data = pd.read_csv(StringIO(response.text))

    # Display the first few rows of the DataFrame
    print("Preview of Raw Data")
    print(data.head())

    # Save the data to a CSV file
    data.to_csv("historical_raw_data.csv", index=False)
    print("Historical raw data saved to historical_raw_data.csv")
else:
    # Handle errors
    print(f"Error {response.status_code}: {response.text}")