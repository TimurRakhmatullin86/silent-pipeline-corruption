-- Generator: gpt-5-2025-08-07
-- Task: bq_005
-- Generated: 2025-09-17T14:44:35Z

SELECT
  raw_events.event_id,
  raw_events.user_id,
  raw_events.session_id
FROM `project.dataset.raw_events` AS raw_events
WHERE raw_events.event_timestamp >= '2025-01-01'
  AND raw_events.event_timestamp < '2025-07-01'
ORDER BY 1