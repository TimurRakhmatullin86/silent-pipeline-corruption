-- Generator: gpt-5-2025-08-07
-- Task: bq_056
-- Generated: 2025-09-19T13:11:31Z

SELECT
  user_activity.user_id,
  user_activity.activity_date
FROM `project.dataset.user_activity` AS user_activity
CROSS JOIN `project.dataset.users` AS users
WHERE user_activity.activity_date >= '2025-01-01'
  AND user_activity.activity_date < '2025-07-01'
ORDER BY 1