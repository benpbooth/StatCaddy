import streamlit as st
import pandas as pd
import requests
import subprocess
from io import StringIO

# Load session state for optimized groups
if "optimized_groups" not in st.session_state:
    st.session_state["optimized_groups"] = []
if "latest_group" not in st.session_state:
    st.session_state["latest_group"] = []

# 🎨 Sidebar Styling
st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 200px !important;
            min-width: 200px !important;
            max-width: 200px !important;
            background-color: #EAEAEA !important;
        }
        section[data-testid="stSidebar"] .st-emotion-cache-16txtl3 {
            color: black !important;
            font-size: 16px !important;
            font-weight: bold !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# ✅ Function to fetch optimized players from Optimized_Group.py output
def fetch_optimized_players():
    try:
        # Run Optimized_Group.py
        subprocess.run(["python3", "Optimized_Group.py"], check=True)

        # Fetch CSV from GitHub
        url = "https://raw.githubusercontent.com/benpbooth/StatCaddy/main/best_selected_players.csv"
        response = requests.get(url)

        if response.status_code == 200:
            df = pd.read_csv(StringIO(response.text))

            # 🔥 Normalize column names to avoid hidden issues
            df.columns = df.columns.str.strip().str.lower()  # Convert to lowercase and strip spaces

            # Debugging: Print column names to verify
            print("Columns in DataFrame:", df.columns.tolist())

            return df
        else:
            st.error(f"Error fetching optimized players: {response.status_code}")
            return pd.DataFrame()
    except subprocess.CalledProcessError as e:
        st.error(f"Error running Optimized_Group.py: {e}")
        return pd.DataFrame()


# ✅ Function to fetch live leaderboard data
def fetch_live_leaderboard():
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
        df.columns = df.columns.astype(str).str.lower().str.strip()

        required_columns = ["current_pos", "player_name", "current_score", "thru", "today", "win", "top_5", "top_10",
                            "top_20"]
        df = df[[col for col in required_columns if col in df.columns]]

        if "current_pos" in df.columns:
            df["current_pos"] = df["current_pos"].astype(str).str.replace("T", "", regex=True)
            df["current_pos"] = pd.to_numeric(df["current_pos"], errors="coerce")
            df = df.sort_values(by="current_pos")

        return df
    else:
        st.error(f"Error fetching live leaderboard: {response.status_code}")
        return pd.DataFrame()


# ✅ Function to highlight optimized players in the leaderboard
def highlight_optimized(row):
    if row["player_name"] in st.session_state.get("latest_group", []):
        return ["background-color: #4E8098; color: white; font-weight: bold;"] * len(row)
    return [""] * len(row)


# ✅ Streamlit UI
def main():
    """Main Streamlit function to display leaderboard and optimized groups."""
    st.title("Arnold Palmer Invitational - 2025")
    st.subheader("Live Leaderboard")

    # Fetch leaderboard data
    df_leaderboard = fetch_live_leaderboard()

    if st.button("🔄 Generate New Group"):
        df_selected = fetch_optimized_players()  # Fetch new optimized players

        # ✅ Debug: Check if df_selected is empty
        if df_selected.empty:
            st.warning("⚠️ No players found in the optimized group. Check your CSV file.")
        else:
            st.session_state["latest_group"] = df_selected["player_name"].tolist()  # Store in session state

    # ✅ Ensure latest group is displayed correctly
    optimized_players = set(st.session_state.get("latest_group", []))

    # ✅ Apply blue highlights without filtering out other players
    styled_df = df_leaderboard.style.apply(highlight_optimized, axis=1)

    # ✅ Display full leaderboard with blue highlights
    st.dataframe(styled_df, height=700, use_container_width=True)

    # ✅ Save Group Button
    if st.button("📌 Save This Group"):
        if "latest_group" in st.session_state and st.session_state["latest_group"]:
            st.session_state["optimized_groups"].append(st.session_state["latest_group"])
            st.success(f"✅ Group {len(st.session_state['optimized_groups'])} saved!")

    # ✅ Display Saved Optimized Groups
    if "optimized_groups" in st.session_state and st.session_state["optimized_groups"]:
        st.header("📌 Saved Optimized Groups")
        for idx, group in enumerate(st.session_state["optimized_groups"], start=1):
            st.subheader(f"Group {idx}")
            if group:
                st.markdown("\n- " + "\n- ".join(group))
            else:
                st.warning(f"Group {idx} has no players stored.")


if __name__ == "__main__":
    main()
