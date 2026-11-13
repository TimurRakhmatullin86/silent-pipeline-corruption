-- Generator: gpt-5-2025-08-07
-- Task: bq_070
-- Generated: 2025-09-09T19:21:14Z

SELECT
  users.user_id,
  users.signup_ts,
  users.channel
FROM `project.dataset.users` AS users
JOIN `project.dataset.payments` AS payments
  ON users.user_id = payments.user_id
JOIN `project.dataset.channel_spend` AS channel_spend
  ON users.channel = channel_spend.channel
ORDER BY 1