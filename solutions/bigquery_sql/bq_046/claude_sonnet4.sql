-- Generator: claude-sonnet-4-20250514
-- Task: bq_046
-- Generated: 2025-10-10T12:52:39Z

SELECT orders_nested.order_id, orders_nested.order_ts, orders_nested.line_items
FROM `project.dataset.orders_nested` AS orders_nested