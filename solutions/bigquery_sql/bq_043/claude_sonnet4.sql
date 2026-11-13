-- Generator: claude-sonnet-4-20250514
-- Task: bq_043
-- Generated: 2025-10-11T13:58:39Z

SELECT products_target.product_id, products_target.price, products_target.updated_at, SUM(products_target.price) AS total_price
FROM `project.dataset.products_target` AS products_target
JOIN `project.dataset.products_staging` AS products_staging
  ON products_target.product_id = products_staging.product_id
WHERE products_target.updated_at >= '2025-01-01'
  AND products_target.updated_at < '2025-07-01'
GROUP BY 1