import streamlit as st
import pandas as pd
import requests
import subprocess
import sys
import os
from io import StringIO

# File to store user credentials
CREDENTIALS_FILE = "user_credentials.csv"

# Load user credentials from file
if os.path.exists(CREDENTIALS_FILE):
    user_credentials = pd.read_csv(CREDENTIALS_FILE, index_col="username").to_dict()["password"]
else:
    user_credentials = {}

def save_credentials():
    pd.DataFrame(list(user_credentials.items()), columns=["username", "password"]).to_csv(CREDENTIALS_FILE, index=False)

def authenticate_user(username, password):
    return user_credentials.get(username) == password

def register_user(username, password):
    if username in user_credentials:
        return False
    user_credentials[username] = password
    save_credentials()
    return True

def login_page():
    st.title("Login to StatCaddy")
    
    menu = ["Login", "Sign Up"]
    choice = st.sidebar.selectbox("Select Option", menu)
    
    if choice == "Login":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if authenticate_user(username, password):
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.rerun()
            else:
                st.error("Invalid Username or Password")
    
    elif choice == "Sign Up":
        new_username = st.text_input("Create Username")
        new_password = st.text_input("Create Password", type="password")
        if st.button("Sign Up"):
            if register_user(new_username, new_password):
                st.success("Account created successfully! Please login.")
            else:
                st.error("Username already exists. Please choose another.")

def highlight_selected_players(row, selected_players):
    if row.name in selected_players:
        return ['background-color: #4E8098; color: #FFFFFF'] * len(row)
    return [''] * len(row)

def get_live_leaderboard(): 
    params = {
        "tour": "pga",
        "dead_heat": "true",
        "odds_format": "percent",
        "file_format": "csv",
        "key": "bef1acff9e6e5e6f132207904ea3"
    }
    url = "https://feeds.datagolf.com/preds/in-play"
    response = requests.get(url, params=params)
    if response.status_code == 200:
        df = pd.read_csv(StringIO(response.text))
        
        required_columns = ["current_pos", "player_name", "current_score", "thru", "today", "win", "top_5", "top_10", "top_20", "R1", "R2", "R3", "R4", "current_round", "last_update"]
        df = df[[col for col in required_columns if col in df.columns]]
        
        if 'current_pos' in df.columns:
            df['current_pos'] = df['current_pos'].astype(str).str.replace('T', '', regex=True)
            df['current_pos'] = pd.to_numeric(df['current_pos'], errors='coerce')
            df = df.sort_values(by='current_pos')
        
        df_fanduel = pd.read_csv("https://raw.githubusercontent.com/benpbooth/StatCaddy/main/the_genesis_invitational_win_american_2025-02-11%2001-47-20%20PM%20EST.csv")
        if {'player_name', 'fanduel_odds'}.issubset(df_fanduel.columns):
            df_fanduel = df_fanduel[['player_name', 'fanduel_odds']]
            df = df.merge(df_fanduel, on='player_name', how='left')
        
        column_order = ["current_pos", "player_name", "current_score", "thru", "today", "fanduel_odds", "win", "top_5", "top_10", "top_20", "R1", "R2", "R3", "R4", "current_round", "last_update"]
        df = df[[col for col in column_order if col in df.columns]]
        df = df.set_index('player_name')
        return df
    else:
        return pd.DataFrame()

def main():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if not st.session_state["logged_in"]:
        login_page()
    else:
        st.title(f"Welcome, {st.session_state['username']}!")
        
        page = st.sidebar.radio("Navigation", ["Live Leaderboard", "Selected Players Data"])
        
        if page == "Live Leaderboard":
            st.write("### Live Leaderboard:")
            try:
                df_selected = pd.read_csv("https://raw.githubusercontent.com/benpbooth/StatCaddy/main/best_selected_players_genesis_2_12_25.csv", index_col="player_name")
                selected_players = set(df_selected.index)
                
                leaderboard_data = get_live_leaderboard()
                if not leaderboard_data.empty:
                    styled_df = leaderboard_data.style.apply(lambda row: highlight_selected_players(row, selected_players), axis=1)
                    st.dataframe(styled_df, height=800, use_container_width=True)
                else:
                    st.error("No live leaderboard data available.")
            except Exception as e:
                st.error(f"Error fetching live leaderboard: {e}")
        
        elif page == "Selected Players Data":
            st.write("### Selected Players Data:")
            try:
                df_selected = pd.read_csv("best_selected_players_genesis_2_12_25.csv", index_col="player_name")
                st.dataframe(df_selected.style.set_properties(**{'width': '50px'}), height=1000, use_container_width=True)
            except Exception as e:
                st.error(f"Error loading selected players CSV file: {e}")
        
        if st.sidebar.button("Logout"):
            st.session_state["logged_in"] = False
            st.session_state["username"] = ""
            st.experimental_rerun()
    
if __name__ == "__main__":
    main()
