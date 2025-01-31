import time
import os
import re
import pandas as pd
from datetime import datetime, timedelta
from selenium import webdrivers
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


def get_outright_odds(download_dir, tour, market):
    # Set download directory
    # download_dir = r"C:\Users\Carson\Desktop\Carson Rhodes\Desktop\Rhodes LLC\Golf Research\Tournament Odds\DP World Tour\Outright Odds"  # Set this to your target folder path

    # Configure Chrome options
    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": download_dir,  # Set download directory
        "download.prompt_for_download": False,  # No download prompts
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })

    # Initialize the WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # Open the website
    driver.get("https://datagolf.com/login?next=%2F")  # Replace with the login URL

    # Find the login form and fill in the credentials
    username_field = driver.find_element(By.ID, "email")  # Replace with the actual field's ID or another selector
    password_field = driver.find_element(By.ID, "password")  # Replace with the actual field's ID or another selector

    username_field.send_keys("cjrhodes1995@outlook.com")  # Replace with your username
    password_field.send_keys("Seconenm12695%")  # Replace with your password

    # Submit the login form (either via a login button or pressing Enter)
    password_field.send_keys(Keys.RETURN)

    # Wait for the page to load after login
    time.sleep(5)

    if tour == 'PGA':

        # Navigate to the page where the file is located
        driver.get(
            "https://datagolf.com/betting-tool-finish")  # Replace with the page URL where the file can be downloaded

    elif tour == 'DP':

        driver.get("https://datagolf.com/betting-tool-finish-euro")

    # Wait for the page to load
    time.sleep(5)

    if market == "Top 5":
        top5 = driver.find_element(By.ID, '1')
        top5.click()
        time.sleep(3)
    elif market == "Top 10":
        top10 = driver.find_element(By.ID, '2')
        top10.click()
        time.sleep(3)
    elif market == "Top 20":
        top20 = driver.find_element(By.ID, '3')
        top20.click()
        time.sleep(3)
    else:
        market == "win"

    baseline = driver.find_element(By.ID, 'baseline')
    baseline.click()

    # Wait for the page to load
    time.sleep(5)

    # Find the update time element and extract its text
    update_time = driver.find_element(By.CLASS_NAME,
                                      'timeago')  # Replace 'timeago' with the actual class name of the element
    update_time_text = update_time.text.strip()  # Clean up the text if necessary

    # Extract the number of hours from the update_time_text (e.g., 'about 2 hours ago')
    hours_ago_match = re.search(r'(\d+)\s+hours?\s+ago', update_time_text)

    if hours_ago_match:
        hours_ago = int(hours_ago_match.group(1))  # Extract the number of hours (x)
        # Calculate the datetime based on the current time minus x hours
        update_datetime = datetime.now() - timedelta(hours=hours_ago)

        # Format the datetime stamp to include AM/PM and EST timezone
        datetime_stamp = update_datetime.strftime("%Y-%m-%d %I:%M:%S %p EST")
    else:
        # If no match, fallback to current time as the datetime stamp
        datetime_stamp = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p EST")

    # Find the download button using Class name and click it
    download_button = driver.find_element(By.CLASS_NAME,
                                          'fa-download')  # Replace with the actual class name of the download button
    download_button.click()

    # Wait for the download to complete (adjust time if necessary based on file size)
    time.sleep(10)

    # Detect the most recent file in the download directory
    files_in_dir = os.listdir(download_dir)
    files_in_dir = [os.path.join(download_dir, file) for file in files_in_dir]  # Get full file paths
    latest_file = max(files_in_dir, key=os.path.getctime)  # Find the most recently created file

    # Split the default file name and extension
    file_name, file_extension = os.path.splitext(os.path.basename(latest_file))

    # Create a new name by appending the datetime stamp to the original name
    new_file_name = f"{file_name}_{datetime_stamp.replace(':', '-')}{file_extension}"  # Replace ':' with '-' to avoid issues in file names

    # Get the full path for the new file name
    new_file_path = os.path.join(download_dir, new_file_name)

    # Rename the downloaded file
    os.rename(latest_file, new_file_path)

    # Read the CSV file using pandas
    df = pd.read_csv(new_file_path)

    # Add a new column with the datetime stamp value for each row
    df['Timestamp'] = datetime_stamp

    # Save the updated CSV file
    df.to_csv(new_file_path, index=False)

    print(f"File renamed to {new_file_name} and saved in {download_dir} with a new 'Timestamp' column.")

    # Close the browser
    driver.quit()


tour = "PGA"
market = "win"

download_dir = fr"C:\Users\Carson\Desktop\Carson Rhodes\Desktop\Rhodes LLC\Golf Research\Tournament Odds\{tour}\Outright Odds"

get_outright_odds(download_dir, tour, market)