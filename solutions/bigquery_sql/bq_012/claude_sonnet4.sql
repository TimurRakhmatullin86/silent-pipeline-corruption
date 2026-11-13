-- Generator: claude-sonnet-4-20250514
-- Task: bq_012
-- Generated: 2025-09-25T09:48:40Z

SELECT game_events.event_id, game_events.player_id, game_events.event_ts
FROM `project.dataset.game_events` AS game_events
JOIN `project.dataset.players` AS players
  ON game_events.player_id = players.player_id