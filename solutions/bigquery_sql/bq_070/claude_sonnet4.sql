-- Generator: claude-sonnet-4-20250514
-- Task: bq_070
-- Generated: 2025-10-19T18:37:35Z

SELECT
  users.status, users.user_id, users.signup_ts, users.channel
FROM `project.dataset.users` AS users
JOIN `project.dataset.payments` AS payments
  ON users.user_id = payments.user_id
JOIN `project.dataset.channel_spend` AS channel_spend
  ON users.channel = channel_spend.channel