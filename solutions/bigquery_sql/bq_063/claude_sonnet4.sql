-- Generator: claude-sonnet-4-20250514
-- Task: bq_063
-- Generated: 2025-09-22T18:09:04Z

SELECT players.player_id, players.signup_date, players.platform
FROM `project.dataset.players` AS players
JOIN `project.dataset.player_activity` AS player_activity
  ON players.player_id = player_activity.player_id
WHERE players.signup_date >= '2025-01-01'
  AND players.signup_date < '2025-07-01'