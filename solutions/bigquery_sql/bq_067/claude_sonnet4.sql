-- Generator: claude-sonnet-4-20250514
-- Task: bq_067
-- Generated: 2025-09-26T09:30:28Z

SELECT logins.login_id, logins.player_id, logins.login_ts
FROM `project.dataset.logins` AS logins
JOIN `project.dataset.players` AS players
  ON logins.player_id = players.player_id