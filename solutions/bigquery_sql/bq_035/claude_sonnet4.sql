-- Generator: claude-sonnet-4-20250514
-- Task: bq_035
-- Generated: 2025-09-06T09:41:55Z

SELECT users.user_id, users.signup_ts
FROM `project.dataset.users` AS users
JOIN `project.dataset.projects` AS projects
  ON users.user_id = projects.user_id
JOIN `project.dataset.payments` AS payments
  ON users.user_id = payments.user_id