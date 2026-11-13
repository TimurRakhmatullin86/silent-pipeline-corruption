-- Generator: deepseek-chat-v3-0324
-- Task: bq_047
-- Generated: 2025-08-29T11:08:30Z

SELECT
  user_activity.user_id,
  user_activity.activity_date,
  user_activity.events
FROM `project.dataset.user_activity` AS user_activity
JOIN `project.dataset.users` AS users
  ON user_activity.user_id = users.user_id
WHERE user_activity.activity_date >= '2025-01-01'
  AND user_activity.activity_date < '2025-07-01'