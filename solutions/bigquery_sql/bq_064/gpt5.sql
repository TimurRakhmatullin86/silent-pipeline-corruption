-- Generator: gpt-5-2025-08-07
-- Task: bq_064
-- Generated: 2025-08-19T11:38:32Z

SELECT
  device_events.event_id,
  device_events.device_id,
  device_events.event_name
FROM `project.dataset.device_events` AS device_events
JOIN `project.dataset.identity_map` AS identity_map
  ON device_events.device_id = identity_map.device_id
ORDER BY 1