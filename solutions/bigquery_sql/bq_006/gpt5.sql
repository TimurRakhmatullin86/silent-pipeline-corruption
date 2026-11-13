-- Generator: gpt-5-2025-08-07
-- Task: bq_006
-- Generated: 2025-10-21T14:52:27Z

SELECT
  orders.order_id,
  orders.customer_id,
  orders.order_ts,
  SUM(orders.total_amount) AS total_total_amount
FROM `project.dataset.orders` AS orders
JOIN `project.dataset.customers` AS customers
  ON orders.customer_id = customers.customer_id
GROUP BY 1, 2, 3
ORDER BY 1