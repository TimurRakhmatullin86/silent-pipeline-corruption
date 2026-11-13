-- Generator: gpt-5-2025-08-07
-- Task: bq_046
-- Generated: 2025-09-01T12:35:19Z

SELECT
  orders_nested.order_id,
  orders_nested.order_ts,
  orders_nested.line_items
FROM `project.dataset.orders_nested` AS orders_nested
ORDER BY 1