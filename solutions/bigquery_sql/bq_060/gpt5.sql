-- Generator: gpt-5-2025-08-07
-- Task: bq_060
-- Generated: 2025-10-25T09:26:22Z

SELECT
  invoices.invoice_id,
  invoices.account_id,
  invoices.amount,
  SUM(invoices.amount) AS total_amount
FROM `project.dataset.invoices` AS invoices
CROSS JOIN `project.dataset.accounts` AS accounts
JOIN `project.dataset.account_reps` AS account_reps
GROUP BY 1, 2, 3
ORDER BY 1