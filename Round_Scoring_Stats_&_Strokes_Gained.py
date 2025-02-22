import requests
import pandas as pd
from io import StringIO

base_url = "https://feeds.datagolf.com/historical-raw-data/rounds"

# parameters
years = ["2017", "2018", "2019", "2020", "2021", "2022", "2023"]
tour = "pga"
file_format = "csv"
api_key = "bef1acff9e6e5e6f132207904ea3"

# iterate through each year
for year in years:
    print(f"Processing year: {year}")

    # Define the parameters for the request
    params = {
        "tour": tour,
        "event_id": "all",  # Fetch data for all events in the year
        "year": year,
        "file_format": file_format,
        "key": api_key
    }

    # Make the API request
    response = requests.get(base_url, params=params)

    # Check the response status
    if response.status_code == 200:
        if file_format == "csv":
            # Parse the CSV response into a DataFrame
            round_data = pd.read_csv(StringIO(response.text))
            print(f"Data for year {year} retrieved successfully. Preview:")
            print(round_data.head())

            # Save the data to a CSV file
            file_name = f"round_data_{tour}_{year}.csv"
            round_data.to_csv(file_name, index=False)
            print(f"Data for year {year} saved to {file_name}")
        else:
            print(f"Data for year {year} retrieved successfully in JSON format.")
            # Optionally handle JSON responses
    else:
        print(f"Error fetching data for year {year}: {response.status_code} - {response.text}")

print("Data retrieval complete.")

