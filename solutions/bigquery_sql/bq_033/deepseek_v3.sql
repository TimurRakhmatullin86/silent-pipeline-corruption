-- Generator: deepseek-chat-v3-0324
-- Task: bq_033
-- Generated: 2025-10-07T18:46:39Z

SELECT
  play_sessions.status,
  play_sessions.session_id,
  play_sessions.player_id,
  play_sessions.start_ts
FROM `project.dataset.play_sessions` AS play_sessions
JOIN `project.dataset.players` AS players
  ON play_sessions.player_id = players.player_id