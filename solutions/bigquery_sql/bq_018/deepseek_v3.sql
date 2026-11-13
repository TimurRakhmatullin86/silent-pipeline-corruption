-- Generator: deepseek-chat-v3-0324
-- Task: bq_018
-- Generated: 2025-08-28T14:28:56Z

SELECT
  daily_signups.signup_date,
  daily_signups.platform,
  daily_signups.signups
FROM `project.dataset.daily_signups` AS daily_signups
WHERE daily_signups.signup_date >= '2025-01-01'
  AND daily_signups.signup_date < '2025-07-01'