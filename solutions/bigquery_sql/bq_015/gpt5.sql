-- Generator: gpt-5-2025-08-07
-- Task: bq_015
-- Generated: 2025-09-23T12:07:25Z

SELECT
  users.user_id,
  users.signup_ts,
  users.channel_id
FROM `project.dataset.users` AS users
JOIN `project.dataset.channels` AS channels
  ON users.channel_id = channels.channel_id
ORDER BY 1