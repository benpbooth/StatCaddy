# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 19:57:46 2025

@author: Carson
"""
import streamlit as st
import subprocess
import sys
import pandas as pd

# Set page config at the very top
st.set_page_config(page_title="Basic Streamlit App", layout="wide")

# Custom CSS for dark muted theme
st.markdown(
    """
    <style>
    body {
        background-color: #1E1E1E;
        color: #E0E0E0;
    }
    .stApp {
        background-color: #1E1E1E;
    }
    .stSidebar {
        background-color: #2A2A2A;
    }
    .stTextInput input {
        background-color: #3A3A3A;
        color: #E0E0E0;
    }
    .stDataFrame {
        background-color: #2A2A2A;
        color: #E0E0E0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def main():
    st.title("Welcome to StatCaddy")
    st.markdown("*'And indeed it soon followed, that Bimbos and Mojitos did nothing but protect us from the Sun's harm...'* -Unknown, circa 10,000 BCE")
    
    # Sidebar
    st.sidebar.header("Options")
    user_input = st.sidebar.text_input("Search:", "")
    
    if st.sidebar.button("Submit"):
        st.write(f"You entered: {user_input}")
    
    # Button to execute the script
    if st.button("Run DataGolfOddsDownload.py"):
        try:
            result = subprocess.run([sys.executable, "DataGolfOddsDownload.py"], capture_output=True, text=True)
            st.text_area("Script Output:", result.stdout)
            if result.stderr:
                st.text_area("Errors:", result.stderr)
        except Exception as e:
            st.error(f"Error running script: {e}")
            
    # Automatically display CSV contents with a larger view and no index
    try:
        df = pd.read_csv("best_selected_players_genesis_2_12_25.csv", index_col="player_name")
        st.write("### This Week's Picks:")
        st.dataframe(df.style.set_properties(**{'width': '75px'}), height=1350, use_container_width=False)
    except Exception as e:
        st.error(f"Error loading CSV file: {e}")
            
    
    st.sidebar.write("More features coming soon!")
    
if __name__ == "__main__":
    main()
