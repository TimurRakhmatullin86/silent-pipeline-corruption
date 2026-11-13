-- Generator: claude-sonnet-4-20250514
-- Task: bq_018
-- Generated: 2025-08-31T08:42:07Z

SELECT daily_signups.signup_date, daily_signups.platform, daily_signups.signups
FROM `project.dataset.daily_signups` AS daily_signups
WHERE daily_signups.signup_date >= '2025-01-01'
  AND daily_signups.signup_date < '2025-07-01'