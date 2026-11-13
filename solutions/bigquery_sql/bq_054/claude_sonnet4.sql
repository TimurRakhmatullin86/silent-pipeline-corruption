-- Generator: claude-sonnet-4-20250514
-- Task: bq_054
-- Generated: 2025-10-03T19:27:11Z

SELECT invoices.invoice_id, invoices.customer_id, invoices.amount, SUM(invoices.amount) AS total_amount
FROM `project.dataset.invoices` AS invoices
JOIN `project.dataset.customers` AS customers
  ON invoices.customer_id = customers.customer_id
GROUP BY 1, 2, 3