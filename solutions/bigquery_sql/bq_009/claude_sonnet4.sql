-- Generator: claude-sonnet-4-20250514
-- Task: bq_009
-- Generated: 2025-09-19T15:37:35Z

SELECT products.product_id, products.product_name, products.category
FROM `project.dataset.products` AS products
JOIN `project.dataset.sales` AS sales
  ON products.product_id = sales.product_id