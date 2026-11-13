-- Generator: deepseek-chat-v3-0324
-- Task: bq_009
-- Generated: 2025-08-19T09:08:17Z

SELECT
  products.product_id,
  products.product_name,
  products.category
FROM `project.dataset.products` AS products
JOIN `project.dataset.sales` AS sales
  ON products.product_id = sales.product_id