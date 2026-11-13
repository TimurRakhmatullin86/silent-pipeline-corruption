-- Generator: gpt-5-2025-08-07
-- Task: bq_035
-- Generated: 2025-09-06T11:19:07Z

SELECT
  users.user_id,
  users.signup_ts
FROM `project.dataset.users` AS users
JOIN `project.dataset.projects` AS projects
  ON users.user_id = projects.user_id
JOIN `project.dataset.payments` AS payments
  ON users.user_id = payments.user_id
ORDER BY 1