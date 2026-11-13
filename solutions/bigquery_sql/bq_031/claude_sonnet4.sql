-- Generator: claude-sonnet-4-20250514
-- Task: bq_031
-- Generated: 2025-10-26T10:01:09Z

SELECT users.user_id, users.registered_at
FROM `project.dataset.users` AS users
JOIN `project.dataset.orders` AS orders
  ON users.user_id = orders.user_id