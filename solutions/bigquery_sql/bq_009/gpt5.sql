-- Generator: gpt-5-2025-08-07
-- Task: bq_009
-- Generated: 2025-08-17T17:56:05Z

SELECT
  products.product_id,
  products.product_name,
  products.category
FROM `project.dataset.products` AS products
JOIN `project.dataset.sales` AS sales
  ON products.product_id = sales.product_id
ORDER BY 1