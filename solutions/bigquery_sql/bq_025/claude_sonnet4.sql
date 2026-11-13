-- Generator: claude-sonnet-4-20250514
-- Task: bq_025
-- Generated: 2025-10-17T13:53:59Z

SELECT transactions.txn_id, transactions.amount, transactions.currency, SUM(transactions.amount) AS total_amount
FROM `project.dataset.transactions` AS transactions
JOIN `project.dataset.fx_rates` AS fx_rates
  ON transactions.currency = fx_rates.currency
GROUP BY 1, 2, 3