-- Generator: gpt-5-2025-08-07
-- Task: bq_013
-- Generated: 2025-09-16T14:23:02Z

SELECT
  customer_changes.change_seq,
  customer_changes.customer_id,
  customer_changes.email
FROM `project.dataset.customer_changes` AS customer_changes
WHERE customer_changes.updated_at >= '2025-01-01'
  AND customer_changes.updated_at < '2025-07-01'
ORDER BY 1