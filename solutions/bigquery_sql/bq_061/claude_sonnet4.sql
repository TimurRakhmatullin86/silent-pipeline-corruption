-- Generator: claude-sonnet-4-20250514
-- Task: bq_061
-- Generated: 2025-09-13T16:23:48Z

SELECT checkout_events.event_id, checkout_events.user_id, checkout_events.event_name
FROM `project.dataset.checkout_events` AS checkout_events
JOIN `project.dataset.users` AS users
  ON checkout_events.user_id = users.user_id