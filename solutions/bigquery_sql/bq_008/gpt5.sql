-- Generator: gpt-5-2025-08-07
-- Task: bq_008
-- Generated: 2025-09-16T16:32:58Z

SELECT
  orders.order_id,
  orders.customer_id,
  orders.order_ts,
  SUM(orders.amount) AS total_amount
FROM `project.dataset.orders` AS orders
JOIN `project.dataset.refunds` AS refunds
  ON orders.order_id = refunds.order_id
GROUP BY 1, 2, 3
ORDER BY 1