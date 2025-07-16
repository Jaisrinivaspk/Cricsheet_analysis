import os
import json
import pandas as pd
from tqdm import tqdm

DATA_FOLDER = "data/json"
MATCH_CSV = "processing/matches.csv"
BALL_CSV = "processing/deliveries.csv"

match_rows = []
ball_rows = []

print("📂 Reading match JSON files …")
json_files = [f for f in os.listdir(DATA_FOLDER) if f.endswith(".json")]

for file in tqdm(json_files):
    try:
        with open(os.path.join(DATA_FOLDER, file), "r", encoding="utf-8") as f:
            match = json.load(f)

        info = match.get("info", {})

        # Match summary
        match_row = {
            "match_id": file.replace(".json", ""),
            "date": info.get("dates", [None])[0],
            "venue": info.get("venue"),
            "match_type": info.get("match_type"),
            "gender": info.get("gender"),
            "season": info.get("season"),
            "event": info.get("event", {}).get("name"),
            "team1": info.get("teams", [None, None])[0],
            "team2": info.get("teams", [None, None])[1],
            "toss_winner": info.get("toss", {}).get("winner"),
            "toss_decision": info.get("toss", {}).get("decision"),
            "winner": info.get("outcome", {}).get("winner"),
            "by_runs": info.get("outcome", {}).get("by", {}).get("runs"),
            "by_wickets": info.get("outcome", {}).get("by", {}).get("wickets"),
        }
        match_rows.append(match_row)

        # Deliveries (ball-by-ball)
        innings = match.get("innings", [])
        for inning in innings:
            team = inning.get("team")
            overs = inning.get("overs", [])

            for over_data in overs:
                over_number = over_data.get("over")
                deliveries = over_data.get("deliveries", [])

                for delivery in deliveries:
                    row = {
                        "match_id": file.replace(".json", ""),
                        "batting_team": team,
                        "over": over_number,
                        "batter": delivery.get("batter"),
                        "bowler": delivery.get("bowler"),
                        "non_striker": delivery.get("non_striker"),
                        "runs_batter": delivery.get("runs", {}).get("batter", 0),
                        "runs_extras": delivery.get("runs", {}).get("extras", 0),
                        "runs_total": delivery.get("runs", {}).get("total", 0),
                        "wicket_kind": None,
                        "wicket_player_out": None
                    }

                    if "wickets" in delivery:
                        for w in delivery["wickets"]:
                            row["wicket_kind"] = w.get("kind")
                            row["wicket_player_out"] = w.get("player_out")

                    ball_rows.append(row)

    except Exception as e:
        print(f"⚠️ Error processing {file}: {e}")

# Save to CSV
matches_df = pd.DataFrame(match_rows)
deliveries_df = pd.DataFrame(ball_rows)

os.makedirs("processing", exist_ok=True)
matches_df.to_csv(MATCH_CSV, index=False)
deliveries_df.to_csv(BALL_CSV, index=False)

print("\n✅ Done!")
print(f"• Match rows      : {len(matches_df)}")
print(f"• Delivery rows   : {len(deliveries_df)}")
