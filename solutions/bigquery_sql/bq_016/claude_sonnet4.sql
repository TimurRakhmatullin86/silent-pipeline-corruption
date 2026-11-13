-- Generator: claude-sonnet-4-20250514
-- Task: bq_016
-- Generated: 2025-08-09T12:25:45Z

SELECT web_events.event_id, web_events.session_id, web_events.event_name
FROM `project.dataset.web_events` AS web_events
CROSS JOIN `project.dataset.sessions` AS sessions