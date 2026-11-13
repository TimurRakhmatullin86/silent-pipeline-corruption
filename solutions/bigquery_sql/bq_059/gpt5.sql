-- Generator: gpt-5-2025-08-07
-- Task: bq_059
-- Generated: 2025-10-18T19:37:15Z

SELECT
  daily_store_orders.store_id,
  daily_store_orders.metric_date,
  daily_store_orders.orders
FROM `project.dataset.daily_store_orders` AS daily_store_orders
JOIN `project.dataset.stores` AS stores
  ON daily_store_orders.store_id = stores.store_id
WHERE daily_store_orders.metric_date >= '2025-01-01'
  AND daily_store_orders.metric_date < '2025-07-01'
ORDER BY 1