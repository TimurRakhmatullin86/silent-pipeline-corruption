-- Generator: deepseek-chat-v3-0324
-- Task: bq_012
-- Generated: 2025-10-14T17:14:46Z

SELECT
  game_events.event_id,
  game_events.player_id,
  game_events.event_ts
FROM `project.dataset.game_events` AS game_events
JOIN `project.dataset.players` AS players
  ON game_events.player_id = players.player_id