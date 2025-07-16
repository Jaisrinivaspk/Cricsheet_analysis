-- 1. Top 10 batsmen by total runs in ODI matches
SELECT batter, SUM(runs_batter) AS total_runs 
FROM deliveries
JOIN matches ON deliveries.match_id = matches.match_id
WHERE match_type = 'ODI'
GROUP BY batter
ORDER BY total_runs DESC
LIMIT 10;

-- 2. Top 10 batsmen by strike rate (min 100 balls) in T20s
SELECT batter,
       COUNT(*) AS balls_faced,
       SUM(runs_batter) AS total_runs,
       ROUND(SUM(runs_batter) * 100.0 / COUNT(*), 2) AS strike_rate
FROM deliveries
JOIN matches ON deliveries.match_id = matches.match_id
WHERE match_type = 'T20'
GROUP BY batter
HAVING balls_faced >= 100
ORDER BY strike_rate DESC
LIMIT 10;

-- 3. Total number of centuries across all match formats
SELECT COUNT(*) AS total_centuries
FROM (
    SELECT match_id, batter, SUM(runs_batter) AS runs
    FROM deliveries
    GROUP BY match_id, batter
    HAVING runs >= 100
);

-- 4. Top 10 bowlers by total wickets in Test matches
SELECT bowler, COUNT(*) AS wickets
FROM deliveries
JOIN matches ON deliveries.match_id = matches.match_id
WHERE match_type = 'Test' AND wicket_kind IS NOT NULL
GROUP BY bowler
ORDER BY wickets DESC
LIMIT 10;

-- 5. Most economical bowlers in ODIs (min 300 balls)
SELECT bowler,
       COUNT(*) AS balls_bowled,
       SUM(runs_total) AS runs_conceded,
       ROUND(SUM(runs_total) * 6.0 / COUNT(*), 2) AS economy_rate
FROM deliveries
JOIN matches ON deliveries.match_id = matches.match_id
WHERE match_type = 'ODI'
GROUP BY bowler
HAVING balls_bowled >= 300
ORDER BY economy_rate ASC
LIMIT 10;

-- 6. Player with highest individual score in T20s
SELECT batter, MAX(runs) AS highest_score
FROM (
    SELECT deliveries.match_id, batter, SUM(runs_batter) AS runs
    FROM deliveries
    JOIN matches ON deliveries.match_id = matches.match_id
    WHERE match_type = 'T20'
    GROUP BY deliveries.match_id, batter
) AS t;

-- 7. Most number of sixes in ODI matches
SELECT batter, COUNT(*) AS sixes
FROM deliveries
JOIN matches ON deliveries.match_id = matches.match_id
WHERE match_type = 'ODI' AND runs_batter = 6
GROUP BY batter
ORDER BY sixes DESC
LIMIT 10;

-- 8. Most wickets taken in a single Test match
SELECT match_id, bowler, wickets
FROM (
    SELECT deliveries.match_id AS match_id,
           bowler,
           COUNT(*) AS wickets
    FROM deliveries
    JOIN matches ON deliveries.match_id = matches.match_id
    WHERE match_type = 'Test'
      AND wicket_kind IS NOT NULL
    GROUP BY deliveries.match_id, bowler
) AS t
ORDER BY wickets DESC
LIMIT 10;

-- 9. Top 5 all-rounders (500+ runs & 50+ wickets)
WITH batsmen AS (
    SELECT batter, SUM(runs_batter) AS total_runs
    FROM deliveries
    GROUP BY batter
    HAVING total_runs >= 500
),
bowlers AS (
    SELECT bowler, COUNT(*) AS total_wickets
    FROM deliveries
    WHERE wicket_kind IS NOT NULL
    GROUP BY bowler
    HAVING total_wickets >= 50
)
SELECT b.batter AS player, total_runs, total_wickets
FROM batsmen b
JOIN bowlers bw ON b.batter = bw.bowler
ORDER BY total_runs + total_wickets DESC
LIMIT 5;

-- 10. Players with most captaincy matches (based on toss winner)
SELECT DISTINCT player, COUNT(match_id) AS captain_matches
FROM (
    SELECT match_id, toss_winner AS player
    FROM matches
)
GROUP BY player
ORDER BY captain_matches DESC;

-- 11. Team with highest win percentage in Test matches
SELECT winner,
       COUNT(*) * 100.0 / (SELECT COUNT(*) FROM matches WHERE match_type = 'Test') AS win_percentage
FROM matches
WHERE match_type = 'Test' AND winner IS NOT NULL
GROUP BY winner
ORDER BY win_percentage DESC
LIMIT 1;

-- 12. Most successful IPL team by wins (heuristic)
SELECT winner, COUNT(*) AS total_wins
FROM matches
WHERE match_type = 'T20'
  AND season >= '2008'
  AND winner IS NOT NULL
GROUP BY winner
ORDER BY total_wins DESC
LIMIT 1;

-- 13. Most common dismissal type across all formats
SELECT wicket_kind, COUNT(*) AS times
FROM deliveries
WHERE wicket_kind IS NOT NULL
GROUP BY wicket_kind
ORDER BY times DESC
LIMIT 1;

-- 14. Total number of ODI matches played by each team
SELECT team, COUNT(*) AS total_matches
FROM (
    SELECT match_id, team1 AS team FROM matches WHERE match_type = 'ODI'
    UNION ALL
    SELECT match_id, team2 AS team FROM matches WHERE match_type = 'ODI'
)
GROUP BY team
ORDER BY total_matches DESC;

-- 15. Team with highest average score per T20 match
SELECT batting_team,
       ROUND(SUM(runs_total) * 1.0 / COUNT(DISTINCT deliveries.match_id), 2) AS avg_runs
FROM deliveries
JOIN matches ON deliveries.match_id = matches.match_id
WHERE match_type = 'T20'
GROUP BY batting_team
ORDER BY avg_runs DESC
LIMIT 5;

-- 16. Closest wins by run margin
SELECT match_id, winner, by_runs
FROM matches
WHERE by_runs IS NOT NULL AND by_runs > 0
ORDER BY by_runs ASC
LIMIT 10;

-- 17. Toss winner same as match winner (ODI)
SELECT
  COUNT(*) AS total_matches,
  SUM(CASE WHEN toss_winner = winner THEN 1 ELSE 0 END) AS same_winner,
  ROUND(SUM(CASE WHEN toss_winner = winner THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS same_winner_pct
FROM matches
WHERE match_type = 'ODI' AND toss_winner IS NOT NULL AND winner IS NOT NULL;

-- 18. Average match duration (balls) by format
SELECT match_type,
       COUNT(*) AS total_balls,
       ROUND(COUNT(*) * 1.0 / COUNT(DISTINCT deliveries.match_id), 2) AS avg_balls_per_match
FROM deliveries
JOIN matches ON deliveries.match_id = matches.match_id
GROUP BY match_type
ORDER BY avg_balls_per_match DESC;

-- 19. Team with most wins across all formats
SELECT winner AS team, COUNT(*) AS wins
FROM matches
WHERE winner IS NOT NULL
GROUP BY winner
ORDER BY wins DESC;

-- 20. Total number of matches per IPL season (heuristic)
SELECT season, COUNT(*) AS total_matches
FROM matches
WHERE match_type = 'T20'
  AND season >= '2008'
GROUP BY season
ORDER BY season;
