-- Generator: gpt-5-2025-08-07
-- Task: bq_012
-- Generated: 2025-08-10T19:03:10Z

SELECT
  game_events.event_id,
  game_events.player_id,
  game_events.event_ts
FROM `project.dataset.game_events` AS game_events
JOIN `project.dataset.players` AS players
  ON game_events.player_id = players.player_id
ORDER BY 1