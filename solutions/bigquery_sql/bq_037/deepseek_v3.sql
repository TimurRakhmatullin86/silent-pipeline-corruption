-- Generator: deepseek-chat-v3-0324
-- Task: bq_037
-- Generated: 2025-10-01T11:12:52Z

SELECT
  orders.order_id,
  orders.customer_id,
  orders.order_ts,
  SUM(orders.amount) AS total_amount
FROM `project.dataset.orders` AS orders
JOIN `project.dataset.customer_tier_history` AS customer_tier_history
  ON orders.customer_id = customer_tier_history.customer_id
GROUP BY 1