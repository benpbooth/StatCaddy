# -*- coding: utf-8 -*-
"""
Created on Sat Jan 18 12:54:16 2025

@author: Carson
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 16:59:17 2024

@author: Carson
"""

import requests
import pandas as pd
import os
import json

def fetch_event_data(directory_path, years, event_ids):
    """
    Fetches data for the specified event IDs and saves each to a CSV file.

    Parameters:
        directory_path (str): Directory path to save the files.
        event_ids (list): List of event IDs to fetch data for.

    Returns:
        None
    """
    
    
    # Ensure the directory exists
    os.makedirs(directory_path, exist_ok=True)

    # Define the static parts of the API endpoint
    base_url = "https://feeds.datagolf.com/historical-raw-data/rounds"
    api_key = "bef1acff9e6e5e6f132207904ea3"  # replace with your actual API key

    all_data = []  # To store all data for concatenation

    for event_id in event_ids: 
        for year in years:
            params = {
                "tour": "pga",
                "year": year,  # Adjust if needed
                "event_id": "all",
                "file_format": "json",
                "key": api_key
            }
    
            try:
                # Send the request
                response = requests.get(base_url, params=params)
    
                if response.status_code == 200:
                    try:
                        # Parse JSON response
                        data = response.json()
                        
                        file_path = r"C:\Users\Carson\Desktop\Carson Rhodes\Desktop\Rhodes LLC\Golf Research\Tournament Results\DG Raw Data Archive/datagolf_raw_data_2017.txt"
                        print(data)
    
                        if data:  # Check if data is not empty
                            print(f"Data retrieved successfully for event ID: {event_id}")
    
              
    
                            with open(file_path, "w") as file: 
                                json.dump(data, file, indent=4)

                
                        else:
                            print(f"No data available for event ID: {event_id}")
                    except ValueError as ve:
                        print(f"Error parsing JSON for event ID {event_id}: {ve}")
                else:
                    print(f"Failed to fetch data for event ID {event_id}. Status code: {response.status_code}")
    
            except Exception as e:
                print(f"An error occurred while fetching data for event ID {event_id} {year}: {e}")
    
# =============================================================================

# 
# =============================================================================
# Example usage

# =============================================================================


event_ids = "all"

#=============================================================================

if __name__ == "__main__":
    directory_path = r"C:\Users\Carson\Desktop\Carson Rhodes\Desktop\Rhodes LLC\Golf Research\Tournament Results\DG Raw Data Archive"

    # Comprehensive list of event IDs
    #event_ids = ["478", "2025102", "10682", "10681", "2025101"]  # Replace with your full list
# =============================================================================
#     years = ['2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025']
# =============================================================================
    years = ['2025']

    fetch_event_data(directory_path, years, event_ids)



