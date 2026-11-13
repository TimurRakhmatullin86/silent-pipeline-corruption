-- Generator: deepseek-chat-v3-0324
-- Task: bq_068
-- Generated: 2025-09-08T11:24:54Z

SELECT
  internal_payments.entry_id,
  internal_payments.reference,
  internal_payments.amount,
  SUM(internal_payments.amount) AS total_amount
FROM `project.dataset.internal_payments` AS internal_payments
JOIN `project.dataset.processor_settlements` AS processor_settlements
  ON internal_payments.reference = processor_settlements.reference
GROUP BY 1, 2, 3