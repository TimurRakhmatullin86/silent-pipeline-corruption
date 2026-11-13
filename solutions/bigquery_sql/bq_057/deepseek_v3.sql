-- Generator: deepseek-chat-v3-0324
-- Task: bq_057
-- Generated: 2025-10-01T12:47:55Z

SELECT
  click_events.event_id,
  click_events.user_id,
  click_events.event_ts
FROM `project.dataset.click_events` AS click_events
JOIN `project.dataset.users` AS users
  ON click_events.user_id = users.user_id