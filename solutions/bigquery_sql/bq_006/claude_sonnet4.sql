-- Generator: claude-sonnet-4-20250514
-- Task: bq_006
-- Generated: 2025-10-05T13:05:25Z

SELECT orders.order_id, orders.customer_id, orders.order_ts, SUM(orders.total_amount) AS total_total_amount
FROM `project.dataset.orders` AS orders
JOIN `project.dataset.customers` AS customers
  ON orders.customer_id = customers.customer_id
GROUP BY 1, 2, 3