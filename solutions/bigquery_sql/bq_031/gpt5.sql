-- Generator: gpt-5-2025-08-07
-- Task: bq_031
-- Generated: 2025-09-17T12:24:26Z

SELECT
  users.user_id,
  users.registered_at
FROM `project.dataset.users` AS users
JOIN `project.dataset.orders` AS orders
  ON users.user_id = orders.user_id
ORDER BY 1