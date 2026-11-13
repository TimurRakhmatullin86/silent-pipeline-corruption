-- Generator: claude-sonnet-4-20250514
-- Task: bq_023
-- Generated: 2025-08-06T11:25:38Z

SELECT users.user_id, users.signup_date, users.country
FROM `project.dataset.users` AS users
JOIN `project.dataset.activity_log` AS activity_log
  ON users.user_id = activity_log.user_id
WHERE users.signup_date >= '2025-01-01'
  AND users.signup_date < '2025-07-01'