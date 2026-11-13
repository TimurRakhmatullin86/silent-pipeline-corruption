-- Generator: deepseek-chat-v3-0324
-- Task: bq_005
-- Generated: 2025-09-09T19:20:49Z

SELECT
  raw_events.event_id,
  raw_events.user_id,
  raw_events.session_id
FROM `project.dataset.raw_events` AS raw_events
WHERE raw_events.event_timestamp >= '2025-01-01'
  AND raw_events.event_timestamp < '2025-07-01'