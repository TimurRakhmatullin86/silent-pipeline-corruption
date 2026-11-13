-- Generator: gpt-5-2025-08-07
-- Task: bq_067
-- Generated: 2025-09-12T09:35:43Z

SELECT
  logins.login_id,
  logins.player_id,
  logins.login_ts
FROM `project.dataset.logins` AS logins
JOIN `project.dataset.players` AS players
  ON logins.player_id = players.player_id
ORDER BY 1