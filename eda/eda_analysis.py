# eda/eda_analysis.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import os

# Load data
matches_df = pd.read_csv("processing/matches.csv")
deliveries_df = pd.read_csv("processing/deliveries.csv")

# Create plots folder if not exists
os.makedirs("eda/plots", exist_ok=True)

# 1. Match count by format
match_counts = matches_df['match_type'].value_counts()
plt.figure(figsize=(6, 4))
sns.barplot(x=match_counts.index, y=match_counts.values, palette='Set2')
plt.title("Match Count by Format")
plt.xlabel("Format")
plt.ylabel("Count")
plt.savefig("eda/plots/match_count_by_format.png")
plt.close()

# 2. Top 10 teams by wins
top_winners = matches_df['winner'].value_counts().head(10)
plt.figure(figsize=(8, 5))
sns.barplot(x=top_winners.values, y=top_winners.index, palette='crest')
plt.title("Top 10 Teams by Wins")
plt.xlabel("Wins")
plt.ylabel("Team")
plt.savefig("eda/plots/top_teams_by_wins.png")
plt.close()

# 3. Top 10 Batsmen by Total Runs
top_batsmen = deliveries_df.groupby('batter')['runs_batter'].sum().sort_values(ascending=False).head(10)
plt.figure(figsize=(10, 6))
sns.barplot(x=top_batsmen.values, y=top_batsmen.index, palette='viridis')
plt.title("Top 10 Batsmen by Total Runs")
plt.xlabel("Total Runs")
plt.ylabel("Batsman")
plt.savefig("eda/plots/top_batsmen_by_runs.png")
plt.close()

# 4. Most Common Dismissal Types
dismissals = deliveries_df['wicket_kind'].value_counts()
plt.figure(figsize=(10, 6))
sns.barplot(x=dismissals.values, y=dismissals.index, palette='coolwarm')
plt.title("Most Common Dismissal Types")
plt.xlabel("Count")
plt.ylabel("Dismissal Type")
plt.savefig("eda/plots/common_dismissals.png")
plt.close()

# 5. Top 10 Bowlers by Wickets
wickets = deliveries_df[deliveries_df['wicket_kind'].notna()]
top_bowlers = wickets['bowler'].value_counts().head(10)
plt.figure(figsize=(10, 6))
sns.barplot(x=top_bowlers.values, y=top_bowlers.index, palette='magma')
plt.title("Top 10 Bowlers by Total Wickets")
plt.xlabel("Wickets")
plt.ylabel("Bowler")
plt.savefig("eda/plots/top_bowlers_by_wickets.png")
plt.close()

# 6. Distribution of Runs PER DELIVERY (all runs, incl. extras)
plt.figure(figsize=(8,5))
sns.countplot(data=deliveries_df, x='runs_total', palette='Set3')
plt.title("Distribution of Total Runs per Delivery")
plt.xlabel("Runs off the Ball")
plt.ylabel("Frequency")
plt.savefig("eda/plots/runs_per_ball_distribution.png")
plt.close()


# 7. Toss Decision Count by Match Type
plt.figure(figsize=(10, 6))
sns.countplot(data=matches_df, x='match_type', hue='toss_decision')
plt.title("Toss Decision by Match Format")
plt.xlabel("Match Format")
plt.ylabel("Count")
plt.legend(title='Toss Decision')
plt.savefig("eda/plots/toss_decision_by_format.png")
plt.close()

# 8. Matches Played by Season (Plotly)
if 'season' in matches_df.columns:
    fig = px.histogram(matches_df, x='season', color='match_type', barmode='group',
                       title="Matches Played by Season", labels={'count': 'Number of Matches'})
    fig.write_html("eda/plots/matches_by_season.html")

# 9. Top 10 Players with Most Sixes (Plotly)
sixes = deliveries_df[deliveries_df['runs_batter'] == 6]
top_six_hitters = sixes['batter'].value_counts().head(10)
fig = px.bar(x=top_six_hitters.values, y=top_six_hitters.index, orientation='h',
             title="Top 10 Players with Most Sixes", labels={'x': 'Sixes', 'y': 'Batter'})
fig.update_layout(yaxis={'categoryorder': 'total ascending'})
fig.write_html("eda/plots/top_six_hitters.html")

# 10. Average Team Score in T20s (Corrected & Readable)
t20_matches = matches_df[matches_df['match_type'] == 'T20'][['match_id']]
t20_deliveries = deliveries_df.merge(t20_matches, on='match_id')

team_match_runs = (
    t20_deliveries
    .groupby(['match_id', 'batting_team'])['runs_total']
    .sum()
    .reset_index()
)

team_avg_runs = (
    team_match_runs
    .groupby('batting_team')['runs_total']
    .mean()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(12, 6))  # Wider and taller
sns.barplot(x=team_avg_runs.values, y=team_avg_runs.index, palette='cubehelix')

plt.title("Top 10 Teams by Avg T20 Match Score (Corrected)", fontsize=14)
plt.xlabel("Average Runs per Match", fontsize=12)
plt.ylabel("Team", fontsize=12)

plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.subplots_adjust(left=0.28)  # Left margin expanded
plt.tight_layout()              # Fit everything cleanly

plt.savefig("eda/plots/top_teams_avg_t20_score.png")
plt.close()



