-- Generator: claude-sonnet-4-20250514
-- Task: bq_013
-- Generated: 2025-10-15T17:42:31Z

SELECT customer_changes.change_seq, customer_changes.customer_id, customer_changes.email
FROM `project.dataset.customer_changes` AS customer_changes
WHERE customer_changes.updated_at >= '2025-01-01'
  AND customer_changes.updated_at < '2025-07-01'