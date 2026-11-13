-- Generator: gpt-5-2025-08-07
-- Task: bq_024
-- Generated: 2025-08-18T14:29:23Z

SELECT
  sessions.session_id,
  sessions.user_id,
  sessions.device
FROM `project.dataset.sessions` AS sessions
JOIN `project.dataset.checkout_events` AS checkout_events
  ON sessions.session_id = checkout_events.session_id
ORDER BY 1