-- Generator: deepseek-chat-v3-0324
-- Task: bq_035
-- Generated: 2025-09-12T09:37:42Z

SELECT
  users.status,
  users.user_id,
  users.signup_ts
FROM `project.dataset.users` AS users
JOIN `project.dataset.projects` AS projects
  ON users.user_id = projects.user_id
JOIN `project.dataset.payments` AS payments
  ON users.user_id = payments.user_id