-- Generator: claude-sonnet-4-20250514
-- Task: bq_024
-- Generated: 2025-09-10T18:04:28Z

SELECT sessions.session_id, sessions.user_id, sessions.device
FROM `project.dataset.sessions` AS sessions
JOIN `project.dataset.checkout_events` AS checkout_events
  ON sessions.session_id = checkout_events.session_id