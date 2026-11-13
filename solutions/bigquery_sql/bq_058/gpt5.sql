-- Generator: gpt-5-2025-08-07
-- Task: bq_058
-- Generated: 2025-10-17T16:27:07Z

SELECT
  events_staging.event_id,
  events_staging.user_id,
  events_staging.event_ts
FROM `project.dataset.events_staging` AS events_staging
JOIN `project.dataset.events_target` AS events_target
  ON events_staging.event_id = events_target.event_id
ORDER BY 1