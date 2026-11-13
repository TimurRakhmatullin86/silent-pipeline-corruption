-- Generator: gpt-5-2025-08-07
-- Task: bq_057
-- Generated: 2025-10-20T18:21:04Z

SELECT
  click_events.event_id,
  click_events.user_id,
  click_events.event_ts
FROM `project.dataset.click_events` AS click_events
JOIN `project.dataset.users` AS users
  ON click_events.user_id = users.user_id
ORDER BY 1