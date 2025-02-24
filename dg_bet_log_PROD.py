import time
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def log_dg_bets(): 
    # Load the CSV file to get all players and odds
    csv_file_path = "best_selected_players_mexico_open_2025_02_17_07_38_33_PM_EST.csv"
    df = pd.read_csv(csv_file_path)
    sportsbook = "fanduel"
    
    # Configure Chrome options
    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", {
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })
    
    # Initialize the WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    # Open the website
    driver.get("https://datagolf.com/login?next=%2F")
    
    # Find the login form and fill in the credentials
    username_field = driver.find_element(By.ID, "email")
    password_field = driver.find_element(By.ID, "password")
    
    username_field.send_keys("cjrhodes1995@outlook.com")
    password_field.send_keys("Seconenm12695%")
    
    # Submit the login form
    password_field.send_keys(Keys.RETURN)
    
    # Wait for the page to load after login
    time.sleep(5)
    
    # Navigate to the bets page
    driver.get("https://datagolf.com/my-bets")
    
    time.sleep(5)
    
    # Click the add bet button only once
    add_bet_button = driver.find_element(By.ID, 'add-outright')
    driver.execute_script("arguments[0].scrollIntoView(true);", add_bet_button)
    driver.execute_script("arguments[0].click();", add_bet_button)
    
    time.sleep(3)
    
    for _, row in df.iterrows():
        player_name = row['player_name']
        player_odds = row['fanduel_odds']
        
        # Ensure the player selection dropdown is interactable
        select_player = driver.find_element(By.ID, 'input-outright-player')
        driver.execute_script("arguments[0].scrollIntoView(true);", select_player)
        time.sleep(1)
        select_player.click()
        time.sleep(2)
        
        # Select the player from the list
        select_player.send_keys(player_name)
        time.sleep(1)
        select_player.send_keys(Keys.RETURN)
        
        # Wait for a moment to confirm selection
        time.sleep(5)
        
        enter_bet_units = driver.find_element(By.ID, 'outrights-units')
        enter_bet_units.click()
        enter_bet_units.send_keys('1')
        
        time.sleep(2)
        
        # Enter the player's odds
        enter_player_odds = driver.find_element(By.ID, 'outrights-american')
        enter_player_odds.click()
        time.sleep(1)  # Allow the field to fully focus
        enter_player_odds.clear()
        enter_player_odds.send_keys(Keys.CONTROL + "a")  # Select any existing text
        enter_player_odds.send_keys(Keys.BACKSPACE)  # Delete existing text
        enter_player_odds.send_keys(str(player_odds))
        enter_player_odds.send_keys(Keys.TAB)  # Ensure input is registered
        
        time.sleep(3)  # Allow the value to be properly recorded
        
        # Click the sportsbook selection dropdown 
        select_sportsbook = driver.find_element(By.ID, 'input-outright-book')
        select_sportsbook.click()
        
        time.sleep(5)
        
        # Select the sportsbook
        select_sportsbook.send_keys(sportsbook)
        select_sportsbook.send_keys(Keys.RETURN)
        
        time.sleep(5)
        
        log_bet = driver.find_element(By.CLASS_NAME, 'fa-pen')
        log_bet.click()
        
        time.sleep(5)
    
    # Close the browser
    driver.quit()

log_dg_bets()
