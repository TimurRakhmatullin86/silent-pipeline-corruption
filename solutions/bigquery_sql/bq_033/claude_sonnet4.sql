-- Generator: claude-sonnet-4-20250514
-- Task: bq_033
-- Generated: 2025-09-07T13:07:00Z

SELECT play_sessions.session_id, play_sessions.player_id, play_sessions.start_ts
FROM `project.dataset.play_sessions` AS play_sessions
JOIN `project.dataset.players` AS players
  ON play_sessions.player_id = players.player_id