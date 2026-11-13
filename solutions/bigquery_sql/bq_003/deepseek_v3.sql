-- Generator: deepseek-chat-v3-0324
-- Task: bq_003
-- Generated: 2025-09-22T13:43:46Z

SELECT
  events.event_id,
  events.user_id,
  events.session_id
FROM `project.dataset.events` AS events
WHERE events.event_timestamp >= '2025-01-01'
  AND events.event_timestamp < '2025-07-01'