-- Generator: gpt-5-2025-08-07
-- Task: bq_063
-- Generated: 2025-08-05T10:45:21Z

SELECT
  players.status,
  players.player_id,
  players.signup_date,
  players.platform
FROM `project.dataset.players` AS players
JOIN `project.dataset.player_activity` AS player_activity
  ON players.player_id = player_activity.player_id
WHERE players.signup_date >= '2025-01-01'
  AND players.signup_date < '2025-07-01'
ORDER BY 1