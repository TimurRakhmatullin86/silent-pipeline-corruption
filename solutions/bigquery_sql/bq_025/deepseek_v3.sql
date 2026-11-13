-- Generator: deepseek-chat-v3-0324
-- Task: bq_025
-- Generated: 2025-10-27T15:04:05Z

SELECT
  transactions.txn_id,
  transactions.amount,
  transactions.currency,
  SUM(transactions.amount) AS total_amount
FROM `project.dataset.transactions` AS transactions
JOIN `project.dataset.fx_rates` AS fx_rates
  ON transactions.currency = fx_rates.currency
GROUP BY 1, 2, 3