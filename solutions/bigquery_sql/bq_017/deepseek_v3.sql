-- Generator: deepseek-chat-v3-0324
-- Task: bq_017
-- Generated: 2025-08-06T19:50:58Z

SELECT
  orders.order_id,
  orders.order_ts,
  orders.status,
  SUM(orders.amount) AS total_amount
FROM `project.dataset.orders` AS orders
GROUP BY 1, 2, 3