-- Generator: deepseek-chat-v3-0324
-- Task: bq_067
-- Generated: 2025-10-29T18:25:08Z

SELECT
  logins.login_id,
  logins.player_id,
  logins.login_ts
FROM `project.dataset.logins` AS logins
CROSS JOIN `project.dataset.players` AS players