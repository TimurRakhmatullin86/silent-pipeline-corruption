-- Generator: deepseek-chat-v3-0324
-- Task: bq_053
-- Generated: 2025-10-02T17:28:26Z

SELECT
  orders.order_id,
  orders.store_id,
  orders.order_ts,
  SUM(orders.amount) AS total_amount
FROM `project.dataset.orders` AS orders
JOIN `project.dataset.stores` AS stores
  ON orders.store_id = stores.store_id
GROUP BY 1, 2, 3