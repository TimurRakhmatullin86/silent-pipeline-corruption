-- Generator: deepseek-chat-v3-0324
-- Task: bq_024
-- Generated: 2025-10-27T16:59:57Z

SELECT
  sessions.session_id,
  sessions.user_id,
  sessions.device
FROM `project.dataset.sessions` AS sessions
JOIN `project.dataset.checkout_events` AS checkout_events
  ON sessions.session_id = checkout_events.session_id