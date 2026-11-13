-- Generator: gpt-5-2025-08-07
-- Task: bq_023
-- Generated: 2025-10-07T12:29:32Z

SELECT
  users.user_id,
  users.signup_date,
  users.country
FROM `project.dataset.users` AS users
JOIN `project.dataset.activity_log` AS activity_log
  ON users.user_id = activity_log.user_id
WHERE users.signup_date >= '2025-01-01'
  AND users.signup_date < '2025-07-01'
ORDER BY 1