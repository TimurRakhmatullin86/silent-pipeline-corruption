-- Generator: claude-sonnet-4-20250514
-- Task: bq_003
-- Generated: 2025-09-02T18:00:57Z

SELECT events.event_id, events.user_id, events.session_id
FROM `project.dataset.events` AS events
WHERE events.event_timestamp >= '2025-01-01'
  AND events.event_timestamp < '2025-07-01'