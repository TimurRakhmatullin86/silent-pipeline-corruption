-- Generator: gpt-5-2025-08-07
-- Task: bq_037
-- Generated: 2025-10-27T14:19:29Z

SELECT
  orders.order_id,
  orders.customer_id,
  orders.order_ts,
  SUM(orders.amount) AS total_amount
FROM `project.dataset.orders` AS orders
JOIN `project.dataset.customer_tier_history` AS customer_tier_history
  ON orders.customer_id = customer_tier_history.customer_id
GROUP BY 1, 2, 3
ORDER BY 1