-- Generator: gpt-5-2025-08-07
-- Task: bq_003
-- Generated: 2025-09-30T19:58:51Z

SELECT
  events.event_id,
  events.user_id,
  events.session_id
FROM `project.dataset.events` AS events
WHERE events.event_timestamp >= '2025-01-01'
  AND events.event_timestamp < '2025-07-01'
ORDER BY 1