-- Generator: gpt-5-2025-08-07
-- Task: bq_016
-- Generated: 2025-09-04T10:16:58Z

SELECT
  web_events.event_id,
  web_events.session_id,
  web_events.event_name
FROM `project.dataset.web_events` AS web_events
JOIN `project.dataset.sessions` AS sessions
  ON web_events.session_id = sessions.session_id
ORDER BY 1