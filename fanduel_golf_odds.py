import requests
import pandas as pd

# Data Golf API URL
API_URL = "https://feeds.datagolf.com/betting-tools/outrights?tour=pga&market=win&odds_format=american&key=bef1acff9e6e5e6f132207904ea3"


def fetch_pga_odds():
    """Fetches outright betting odds for the current PGA tournament."""
    response = requests.get(API_URL)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data: {response.status_code}")
        return None


def process_odds(data):
    """Processes JSON odds data into a structured DataFrame."""
    if not data or "odds" not in data:
        print("No valid odds data found.")
        return None

    books_offering = data.get("books_offering", [])
    odds_list = []

    for player in data["odds"]:
        player_name = player.get("player_name", "Unknown Player")
        dg_odds = player.get("datagolf", {}).get("baseline_history_fit", None)

        for book in books_offering:
            if book in player:  # Ensure the sportsbook exists for this player
                odds_list.append({
                    "player_name": player_name,
                    "sportsbook": book,
                    "odds": player[book],
                    "dg_odds": dg_odds
                })

    if not odds_list:
        print("No valid odds found after processing.")
        return None

    return pd.DataFrame(odds_list)


def optimized_group_selection(df, max_players=10):
    """Selects an optimized group of players based on betting value."""
    df["odds"] = pd.to_numeric(df["odds"].str.replace("+", ""), errors="coerce")  # Convert odds to numeric
    df["dg_odds"] = pd.to_numeric(df["dg_odds"].str.replace("+", ""), errors="coerce")

    df["value_diff"] = df["odds"] - df["dg_odds"]  # Difference between sportsbook & DG odds

    # Sort players by highest value difference (best value bets)
    df_sorted = df.sort_values(by="value_diff", ascending=False)

    return df_sorted.head(max_players)


# Fetch and process odds
odds_data = fetch_pga_odds()
odds_df = process_odds(odds_data)

if odds_df is not None:
    print("\nProcessed Odds Data:")
    print(odds_df.head())

    # Optimize group selection
    optimized_group = optimized_group_selection(odds_df)

    print("\nOptimized Group Selection:")
    print(optimized_group)

    # Save to CSV
    odds_df.to_csv("pga_outright_odds.csv", index=False)
    optimized_group.to_csv("optimized_pga_group.csv", index=False)

    print("\n✅ Odds data saved to 'pga_outright_odds.csv'")
    print("✅ Optimized group saved to 'optimized_pga_group.csv'")

else:
    print("⚠️ No data available.")
