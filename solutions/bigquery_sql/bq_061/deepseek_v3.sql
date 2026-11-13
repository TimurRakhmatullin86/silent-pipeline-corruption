-- Generator: deepseek-chat-v3-0324
-- Task: bq_061
-- Generated: 2025-10-19T15:04:07Z

SELECT
  checkout_events.event_id,
  checkout_events.user_id,
  checkout_events.event_name
FROM `project.dataset.checkout_events` AS checkout_events
JOIN `project.dataset.users` AS users
  ON checkout_events.user_id = users.user_id