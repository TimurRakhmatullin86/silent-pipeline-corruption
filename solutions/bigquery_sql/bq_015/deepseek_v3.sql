-- Generator: deepseek-chat-v3-0324
-- Task: bq_015
-- Generated: 2025-08-01T12:24:15Z

SELECT
  users.user_id,
  users.signup_ts,
  users.channel_id
FROM `project.dataset.users` AS users
JOIN `project.dataset.channels` AS channels
  ON users.channel_id = channels.channel_id