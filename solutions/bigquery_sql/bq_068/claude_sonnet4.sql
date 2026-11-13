-- Generator: claude-sonnet-4-20250514
-- Task: bq_068
-- Generated: 2025-10-13T12:41:13Z

SELECT internal_payments.entry_id, internal_payments.reference, internal_payments.amount, SUM(internal_payments.amount) AS total_amount
FROM `project.dataset.internal_payments` AS internal_payments
JOIN `project.dataset.processor_settlements` AS processor_settlements
  ON internal_payments.reference = processor_settlements.reference
GROUP BY 1