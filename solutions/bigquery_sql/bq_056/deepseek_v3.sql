-- Generator: deepseek-chat-v3-0324
-- Task: bq_056
-- Generated: 2025-10-13T18:12:20Z

SELECT
  user_activity.user_id,
  user_activity.activity_date
FROM `project.dataset.user_activity` AS user_activity
JOIN `project.dataset.users` AS users
  ON user_activity.user_id = users.user_id
WHERE user_activity.activity_date >= '2025-01-01'
  AND user_activity.activity_date <= '2025-07-01'