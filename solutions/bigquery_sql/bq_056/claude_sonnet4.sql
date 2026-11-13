-- Generator: claude-sonnet-4-20250514
-- Task: bq_056
-- Generated: 2025-09-04T15:15:09Z

SELECT user_activity.user_id, user_activity.activity_date
FROM `project.dataset.user_activity` AS user_activity
JOIN `project.dataset.users` AS users
  ON user_activity.user_id = users.user_id
WHERE user_activity.activity_date >= '2025-01-01'
  AND user_activity.activity_date < '2025-07-01'