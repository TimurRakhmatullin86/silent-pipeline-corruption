-- Generator: gpt-5-2025-08-07
-- Task: bq_010
-- Generated: 2025-08-10T12:29:28Z

SELECT
  register_sales.store_id,
  register_sales.register_id,
  register_sales.sale_date,
  SUM(register_sales.amount) AS total_amount
FROM `project.dataset.register_sales` AS register_sales
JOIN `project.dataset.stores` AS stores
  ON register_sales.store_id = stores.store_id
WHERE register_sales.sale_date >= '2025-01-01'
  AND register_sales.sale_date < '2025-07-01'
GROUP BY 1, 2, 3
ORDER BY 1