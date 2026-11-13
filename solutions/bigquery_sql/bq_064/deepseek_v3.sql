-- Generator: deepseek-chat-v3-0324
-- Task: bq_064
-- Generated: 2025-08-14T09:20:42Z

SELECT
  device_events.event_id,
  device_events.device_id,
  device_events.event_name
FROM `project.dataset.device_events` AS device_events
JOIN `project.dataset.identity_map` AS identity_map
  ON device_events.device_id = identity_map.device_id