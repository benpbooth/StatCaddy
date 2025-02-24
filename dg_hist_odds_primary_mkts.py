import requests
import pandas as pd
import os

def get_dg_hist_odds_all(directory_path, sportsbooks, years):
    # Define the endpoint base URL
    url = "https://feeds.datagolf.com/historical-odds/outrights"
    
    # Ensure the directory exists
    os.makedirs(directory_path, exist_ok=True)
    
    # List to store individual DataFrames
    data_frames = []

    # Loop through each sportsbook
    for book in sportsbooks:
        
        for year in years: 
            # Define the parameters for each sportsbook
            
            params = {
                "tour": "pga",
                "event_id": "all",
                "year": years,
                "market": "win",
                "book": book,
                "odds_format": "american",
                "file_format": "csv",
                "key": "bef1acff9e6e5e6f132207904ea3"  # replace with your actual API key
            }
            
            # Send the request
            response = requests.get(url, params=params)
            
            # Check if the response was successful
            if response.status_code == 200:
                # Load CSV data into a pandas DataFrame
                from io import StringIO
                data = pd.read_csv(StringIO(response.text))
                print(f"Data retrieved successfully for {book}!")
                
                # Append the DataFrame to the list
                data_frames.append(data)
                
                # Define the full path with dynamic file name
                file_name = f"datagolf_odds_{book.lower()}_{year}.csv"
                file_path = os.path.join(directory_path, file_name)
                
                
                # Write the individual DataFrame to a CSV file
                data.to_csv(file_path, index=False)
                print(f"Data saved to {file_path}")
            else:
                print(f"Failed to fetch data for {book}. Status code: {response.status_code}")
                
     
                    
    
        # Concatenate all DataFrames in the list into a single DataFrame
        if data_frames:
            master_df = pd.concat(data_frames, ignore_index=True)
            
            # Save the concatenated DataFrame to a master CSV file
            #master_file_path = os.path.join(directory_path, f"datagolf_odds_master_{book}_{*years,}.csv")
            master_file_path = os.path.join(directory_path, f"datagolf_odds_master_{book}_{years}.csv")
            master_df.to_csv(master_file_path, index=False)
            print(f"Master data saved to {master_file_path}")
        else:
            print("No data was fetched, master CSV not created.")

# Example usage: specify your desired directory path and list of sportsbooks
directory_path = r"C:\Users\Carson\Desktop\Carson Rhodes\Desktop\Rhodes LLC\Golf Research\Github\StatCaddy"


sportsbooks = ["fanduel"] 

#sportsbooks = ["williamhill"] # replace with actual sportsbooks available

#years = ['2020', '2021', '2022', '2023', '2024']
#years = ['2019', '2020', '2021', '2022', '2023', '2024', '2025']
#years = ['2021', '2022', '2023', '2024']
years = ['2024']

get_dg_hist_odds_all(directory_path, sportsbooks, years)

