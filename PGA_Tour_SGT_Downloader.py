# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 14:12:31 2025

@author: Carson
"""

import time
import os
from datetime import datetime
import re  # Import for sanitizing file names
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

start_time = datetime.now()
print(f"Started: {start_time}")

# Configuration
#URL FOR STROKES GAINED TOTAL - REPLACE WITH OTHER STAT URLS AS DESIRED
url = "https://www.pgatour.com/stats/detail/02675"  # Replace with the actual URL
download_dir = r"C:\Users\Carson\Desktop\Carson Rhodes\Desktop\Rhodes LLC\Golf Research\Github\StatCaddy"
wait_time_for_manual_selection = 5  # Time to select dropdown values manually
text_element_class_name = "css-1e5ks3"  # Class name for the text element (3 instances expected)

# Configure Chrome options
chrome_options = Options()
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": download_dir,  # Set download directory
    "download.prompt_for_download": False,       # No download prompts
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})

# Initialize WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.get(url)

time.sleep(20)

def sanitize_filename(filename):
    """Remove invalid characters from file names."""
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

try:
    while True:
        # Wait for manual dropdown selection and provide instructions
        print(f"Make your selections from the dropdown menus. Waiting for {wait_time_for_manual_selection} seconds...")
        time.sleep(wait_time_for_manual_selection)

        # Retrieve text from all elements matching the class name
        try:
            elements = driver.find_elements(By.CLASS_NAME, text_element_class_name)
            if len(elements) < 3:
                raise Exception(f"Expected 3 elements, but found {len(elements)}.")

            # Extract and combine text from the elements
            season = elements[0].text.strip()
            season = season[:4]
            category = elements[1].text.strip()
            event = elements[2].text.strip()
            combined_text = f"{season}_{category}_{event}".replace(" ", "_")
            print(f"Combined text for filename: {combined_text}")
        except Exception as e:
            print(f"Error retrieving text elements: {e}")
            continue

        input("Press Enter once you have clicked the download button to proceed...")

        # Wait for the download to complete and rename the file
        time.sleep(10)  # Adjust based on download speed

        try:
            downloaded_files = sorted(
                os.listdir(download_dir), 
                key=lambda x: os.path.getmtime(os.path.join(download_dir, x)), 
                reverse=True
            )
            latest_file = os.path.join(download_dir, downloaded_files[0])
            sanitized_filename = sanitize_filename(combined_text)
            new_file_name = os.path.join(download_dir, f"{sanitized_filename}.csv")
            os.rename(latest_file, new_file_name)
            print(f"File renamed to {new_file_name}")
        except Exception as e:
            print(f"Error renaming file: {e}")
            continue

        # Ask if the user is done
        user_input = input("Type 'done' if you're finished downloading files, or press Enter to continue: ").strip().lower()
        if user_input == 'done':
            print("Exiting the script.")
            end_time = datetime.now()
            run_time = end_time - start_time
            print(f"End: {end_time}")
            print(f"Total Run Time: {run_time}")
            break

finally:
    driver.quit()

