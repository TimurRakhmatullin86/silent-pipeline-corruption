-- Generator: claude-sonnet-4-20250514
-- Task: bq_036
-- Generated: 2025-09-21T14:43:06Z

SELECT orders.order_id, orders.customer_ref, orders.customer_id
FROM `project.dataset.orders` AS orders
CROSS JOIN `project.dataset.customers` AS customers