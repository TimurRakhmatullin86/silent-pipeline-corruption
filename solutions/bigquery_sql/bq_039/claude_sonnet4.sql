-- Generator: claude-sonnet-4-20250514
-- Task: bq_039
-- Generated: 2025-10-31T18:21:50Z

SELECT users.user_id, users.signup_ts
FROM `project.dataset.users` AS users
JOIN `project.dataset.payments` AS payments
  ON users.user_id = payments.user_id