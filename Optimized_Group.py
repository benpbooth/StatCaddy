import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import subprocess

try:
    import pandas as pd
except ModuleNotFoundError:
    print("📦 Installing pandas...")
    subprocess.run([sys.executable, "-m", "pip", "install", "pandas"])
    import pandas as pd  # 🔄 Try importing again after installation
# Load the data
#os.chdir(r'C:\Users\User\Documents\Sports\Golf')
data_path = "/Users/benbooth/PycharmProjects/StatCaddy/arnold_palmer_invitational_win_american.csv"
stats_file = "/Users/benbooth/PycharmProjects/StatCaddy/player_rankings_3:7:25.csv"
df = pd.read_csv(data_path)
stats_df = pd.read_csv(stats_file)

# Parameters for selection
target_avg = 5500  # Target average odds
target_std = 6900  # Target standard deviation
target_median = 6750  # Target median odds
max_odds = 31000  # Maximum allowed odds
max_players = 40  # Maximum number of players

# Filter players based on max_odds
filtered_df = df[df['fanduel_odds'] <= max_odds]

# Random selection function with merging and evaluation
def select_and_evaluate(df, stats_df, target_avg, target_std, target_median, max_players):
    best_selection = None
    best_score = float('inf')  # Lower score means closer to target
    best_rank_score = float('inf')  # Lower rank score is better
    all_results = []  # Store all iterations

    for i in range(10000):  # Iterate multiple times for better results
        sampled = df.sample(n=min(max_players, len(df)))

        # Merge with stats_df
        merged = pd.merge(sampled, stats_df, on='player_name', how='inner')

        # Constraint: Exclude players with two or more ranks >= 100
        rank_columns = [col for col in merged.columns if col.endswith('_rank')]
        valid_players = merged[(merged[rank_columns] >= 500).sum(axis=1) < 2]

        if valid_players.empty:
            continue

        avg = valid_players['fanduel_odds'].mean()
        std = valid_players['fanduel_odds'].std()
        median = valid_players['fanduel_odds'].median()

        # Score based on deviations from targets
        score = (abs(avg - target_avg) +
                 abs(std - target_std) +
                 abs(median - target_median))

        # Calculate rank score (sum of all rank columns, lower is better)
        rank_score = valid_players[rank_columns].sum().sum()

        all_results.append({
            'iteration': i,
            'sampled_df': sampled,
            'merged_df': valid_players,
            'score': score,
            'rank_score': rank_score
        })

        # Update best selection if conditions are met
        if score < best_score or (score == best_score and rank_score < best_rank_score):
            best_score = score
            best_selection = valid_players
            best_rank_score = rank_score

    return best_selection, best_rank_score, all_results

# Run the function
selected_players, best_rank_score, all_results = select_and_evaluate(
    filtered_df, stats_df, target_avg, target_std, target_median, max_players
)

# Save the best results
if selected_players is not None:
    print("Best Selected Players:")
    print(selected_players)

    # Summary statistics for the best selection
    best_avg = selected_players['fanduel_odds'].mean()
    best_std = selected_players['fanduel_odds'].std()
    best_median = selected_players['fanduel_odds'].median()
    print("\nSummary Statistics for Best Selection:")
    print(f"Average Odds: {best_avg}")
    print(f"Standard Deviation of Odds: {best_std}")
    print(f"Median Odds: {best_median}")

    # Rank columns summary
    merged_best = selected_players
    rank_columns = [col for col in merged_best.columns if col.endswith('_rank')]
    if rank_columns:
        rank_summary = merged_best[rank_columns].describe()
        print("\nRankings Summary for Best Selection:")
        print(rank_summary)

    output_path = '/Users/benbooth/Desktop/StatCaddy/best_selected_players.csv'
    merged_best[['player_name', 'fanduel_odds'] + rank_columns].to_csv(output_path, index=False)
    print(f"Best selected players saved to {output_path}")
else:
    print("No players selected matching the criteria.")

# Example: Save all iterations' statistics for review
results_summary = pd.DataFrame([
    {'iteration': r['iteration'], 'score': r['score'], 'rank_score': r['rank_score']}
    for r in all_results
])
results_summary.to_csv('iterations_summary.csv', index=False)
print("All iterations summary saved to iterations_summary.csv")

# Visualization: Scatterplot of score vs. rank_score
plt.figure(figsize=(10, 6))
plt.scatter(results_summary['score'], results_summary['rank_score'], alpha=0.5)
plt.xlabel('Score')
plt.ylabel('Rank Score')
plt.title('Score vs. Rank Score Across Iterations')
plt.show()

# Visualization: Histogram of rank_score
plt.figure(figsize=(10, 6))
plt.hist(results_summary['rank_score'], bins=20, alpha=0.7)
plt.xlabel('Rank Score')
plt.ylabel('Frequency')
plt.title('Distribution of Rank Scores')
plt.show()