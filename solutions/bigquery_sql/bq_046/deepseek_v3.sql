-- Generator: deepseek-chat-v3-0324
-- Task: bq_046
-- Generated: 2025-09-26T14:30:29Z

SELECT
  orders_nested.order_id,
  orders_nested.order_ts,
  orders_nested.line_items
FROM `project.dataset.orders_nested` AS orders_nested