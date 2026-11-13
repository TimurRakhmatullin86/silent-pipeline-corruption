-- Generator: claude-sonnet-4-20250514
-- Task: bq_015
-- Generated: 2025-10-20T10:51:08Z

SELECT users.user_id, users.signup_ts, users.channel_id
FROM `project.dataset.users` AS users
JOIN `project.dataset.channels` AS channels
  ON users.channel_id = channels.channel_id