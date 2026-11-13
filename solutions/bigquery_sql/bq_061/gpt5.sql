-- Generator: gpt-5-2025-08-07
-- Task: bq_061
-- Generated: 2025-10-22T10:15:06Z

SELECT
  checkout_events.event_id,
  checkout_events.user_id,
  checkout_events.event_name
FROM `project.dataset.checkout_events` AS checkout_events
JOIN `project.dataset.users` AS users
  ON checkout_events.user_id = users.user_id
ORDER BY 1