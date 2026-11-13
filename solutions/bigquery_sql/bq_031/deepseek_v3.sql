-- Generator: deepseek-chat-v3-0324
-- Task: bq_031
-- Generated: 2025-08-17T09:58:18Z

SELECT
  users.user_id,
  users.registered_at
FROM `project.dataset.users` AS users
JOIN `project.dataset.orders` AS orders
  ON users.user_id = orders.user_id