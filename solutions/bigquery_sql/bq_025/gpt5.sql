-- Generator: gpt-5-2025-08-07
-- Task: bq_025
-- Generated: 2025-09-17T10:35:03Z

SELECT
  transactions.txn_id,
  transactions.amount,
  transactions.currency,
  SUM(transactions.amount) AS total_amount
FROM `project.dataset.transactions` AS transactions
JOIN `project.dataset.fx_rates` AS fx_rates
  ON transactions.currency = fx_rates.currency
GROUP BY 1
ORDER BY 1