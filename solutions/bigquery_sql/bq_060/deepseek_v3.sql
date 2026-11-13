-- Generator: deepseek-chat-v3-0324
-- Task: bq_060
-- Generated: 2025-10-09T14:29:59Z

SELECT
  invoices.invoice_id,
  invoices.account_id,
  invoices.amount,
  SUM(invoices.amount) AS total_amount
FROM `project.dataset.invoices` AS invoices
JOIN `project.dataset.accounts` AS accounts
  ON invoices.account_id = accounts.account_id
JOIN `project.dataset.account_reps` AS account_reps
  ON invoices.account_id = account_reps.account_id
GROUP BY 1, 2, 3