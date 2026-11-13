-- Generator: gpt-5-2025-08-07
-- Task: bq_017
-- Generated: 2025-10-24T17:55:09Z

SELECT
  orders.order_id,
  orders.order_ts,
  orders.status,
  SUM(orders.amount) AS total_amount
FROM `project.dataset.orders` AS orders
GROUP BY 1, 2, 3
ORDER BY 1