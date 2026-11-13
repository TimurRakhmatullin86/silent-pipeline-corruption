-- Generator: gpt-5-2025-08-07
-- Task: bq_033
-- Generated: 2025-10-11T13:05:50Z

SELECT
  play_sessions.session_id,
  play_sessions.player_id,
  play_sessions.start_ts
FROM `project.dataset.play_sessions` AS play_sessions
JOIN `project.dataset.players` AS players
  ON play_sessions.player_id = players.player_id
ORDER BY 1