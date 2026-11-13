-- Generator: deepseek-chat-v3-0324
-- Task: bq_039
-- Generated: 2025-08-15T14:37:19Z

SELECT
  users.user_id,
  users.signup_ts
FROM `project.dataset.users` AS users
CROSS JOIN `project.dataset.payments` AS payments