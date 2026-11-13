-- Generator: claude-sonnet-4-20250514
-- Task: bq_057
-- Generated: 2025-09-22T08:20:47Z

SELECT click_events.event_id, click_events.user_id, click_events.event_ts
FROM `project.dataset.click_events` AS click_events
JOIN `project.dataset.users` AS users
  ON click_events.user_id = users.user_id