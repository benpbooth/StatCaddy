# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 20:17:20 2025

@author: Carson
"""

import pandas as pd
import numpy as np

def load_data(file_path):
    df = pd.read_csv(file_path)
    return df

def select_players(df, event_name, num_players, min_odds, max_odds, exclude_players=set()):
    """
    Selects players randomly based on odds range for a given event, ensuring no overlap with excluded players.
    """
    event_df = df[df['event_name'] == event_name]
    filtered_df = event_df[(event_df['open_odds'] >= min_odds) & (event_df['open_odds'] <= max_odds)]
    filtered_df = filtered_df[~filtered_df['player_name'].isin(exclude_players)]
    
    return set(np.random.choice(filtered_df['player_name'], size=min(num_players, len(filtered_df)), replace=False))

def main(file_path, output_file, num_players_1, min_odds_1, max_odds_1, num_players_2, min_odds_2, max_odds_2):
    df = load_data(file_path)
    df['bet_outcome_numeric'] = df['bet_outcome_numeric'].replace(0, -1)
    
    selection_data = []
    
    for event in df['event_name'].unique():
        selected_1 = select_players(df, event, num_players_1, min_odds_1, max_odds_1)
        selected_2 = select_players(df, event, num_players_2, min_odds_2, max_odds_2, exclude_players=selected_1)
        
        for player in selected_1:
            selection_data.append({'event_name': event, 'player_name': player, 'selection_function': 'Function_1'})
        
        for player in selected_2:
            selection_data.append({'event_name': event, 'player_name': player, 'selection_function': 'Function_2'})
    
    selection_df = pd.DataFrame(selection_data)
    merged_df = df.merge(selection_df, on=['event_name', 'player_name'], how='inner')
    
    # Add "win/loss" column with updated logic
    def calculate_win_loss(row):
        if row['selection_function'] == 'Function_1':
            return -100 if row['bet_outcome_numeric'] == -1 else row['open_odds']
        elif row['selection_function'] == 'Function_2':
            return -100 if row['bet_outcome_numeric'] == -1 else (100/100) * row['open_odds']
        return None
    
    merged_df['win/loss'] = merged_df.apply(calculate_win_loss, axis=1)
    
    merged_df.to_csv(output_file, index=False)
    
    return merged_df

# Example usage:
file_path = r'C:\Users\Carson\Desktop\Carson Rhodes\Desktop\Rhodes LLC\Golf Research\Github\StatCaddy\datagolf_odds_fanduel_2024.csv'
output_file = r'C:\Users\Carson\Desktop\Carson Rhodes\Desktop\Rhodes LLC\Golf Research\Github\StatCaddy\selected_players_2024.csv'
num_players_1, min_odds_1, max_odds_1 = 35, 1800, 6500  # Example values for function 1
num_players_2, min_odds_2, max_odds_2 = 10, 6600, 15000  # Example values for function 2

result_df = main(file_path, output_file, num_players_1, min_odds_1, max_odds_1, num_players_2, min_odds_2, max_odds_2)
print(f"Output saved to {output_file}")
