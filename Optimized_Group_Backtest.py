# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 12:50:36 2025

@author: Carson
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Load the new data
DATA_PATH = r"C:\Users\Carson\Desktop\Carson Rhodes\Desktop\Rhodes LLC\Golf Research\Tournament Odds\Historical\Master Repository\concatenated_master_file_win_2019_2023.csv"
df = pd.read_csv(DATA_PATH)

# Parameters for selection
target_avg = 3300  # Target average odds
target_std = 3000  # Target standard deviation
target_median = 2500  # Target median odds
max_odds = 21000  # Maximum allowed odds
max_players = 25  # Maximum number of players
wager_amount = 100  # Prespecified wager amount

# Ensure each player is only selected once per tournament with highest open_odds
def select_highest_odds(df):
    df = df.sort_values(by=['open_odds'], ascending=False)
    df = df.groupby(['event_name', 'event_completed', 'player_name']).head(1).reset_index(drop=True)
    return df

df = select_highest_odds(df)

# Replace 0 values in 'bet_outcome_numeric' with -1
df['bet_outcome_numeric'] = df['bet_outcome_numeric'].replace(0, -1)

# Calculate profit/loss
df['profit_loss'] = df.apply(lambda row: row['bet_outcome_numeric'] * row['open_odds'] if row['bet_outcome_numeric'] == 1 else -1 * wager_amount, axis=1)

# Function to select and evaluate players
def select_and_evaluate(df, target_avg, target_std, target_median, max_players):
    best_selection = None
    best_score = float('inf')  # Lower score means closer to target
    all_results = []  # Store all iterations

    for i in range(10000):  # Iterate multiple times for better results
        sampled = df.sample(n=min(max_players, len(df)))

        avg = sampled['open_odds'].mean()
        std = sampled['open_odds'].std()
        median = sampled['open_odds'].median()
        outcome_sum = sampled['bet_outcome_numeric'].sum()
        profit_loss_sum = sampled['profit_loss'].sum()

        # Score based on deviations from targets
        score = (abs(avg - target_avg) +
                 abs(std - target_std) +
                 abs(median - target_median))

        all_results.append({'iteration': i, 'score': score, 'outcome_sum': outcome_sum, 'profit_loss_sum': profit_loss_sum})

        if score < best_score:
            best_score = score
            best_selection = sampled

    return best_selection, all_results

# Iterate through unique events
results = {}
output_list = []
full_results_list = []
for (event_name, event_completed), event_df in df.groupby(['event_name', 'event_completed']):
    event_df = event_df[event_df['open_odds'] <= max_odds]  # Filter by max odds
    if event_df.empty:
        continue
    
    selected_players, all_results = select_and_evaluate(event_df, target_avg, target_std, target_median, max_players)
    
    if selected_players is not None:
        results[(event_name, event_completed)] = selected_players
        outcome_sum = selected_players['bet_outcome_numeric'].sum()
        profit_loss_sum = selected_players['profit_loss'].sum()
        output_list.append({'event_name': event_name, 'event_completed': event_completed, 'outcome_sum': outcome_sum, 'profit_loss_sum': profit_loss_sum})
        
        # Store detailed player selection results
        selected_players['event_name'] = event_name
        selected_players['event_completed'] = event_completed
        full_results_list.append(selected_players)

# Save summary results to CSV
output_df = pd.DataFrame(output_list)
output_csv_path = r"C:\Users\Carson\Desktop\Carson Rhodes\Desktop\Rhodes LLC\Golf Research\Github\StatCaddy\best_selections_results.csv"
output_df.to_csv(output_csv_path, index=False)
print(f"Results saved to {output_csv_path}")

# Save full detailed results to CSV
full_results_df = pd.concat(full_results_list, ignore_index=True)
full_results_csv_path = r"C:\Users\Carson\Desktop\Carson Rhodes\Desktop\Rhodes LLC\Golf Research\Github\StatCaddy\full_best_selections_results.csv"
full_results_df.to_csv(full_results_csv_path, index=False)
print(f"Full detailed results saved to {full_results_csv_path}")

# Display results
for (event_name, event_completed), selected_players in results.items():
    print(f"\nBest Selections for {event_name} ({event_completed}):")
    print(selected_players[['player_name', 'open_odds', 'bet_outcome_numeric', 'profit_loss']])