-- Generator: deepseek-chat-v3-0324
-- Task: bq_054
-- Generated: 2025-09-10T19:20:46Z

SELECT
  invoices.invoice_id,
  invoices.customer_id,
  invoices.amount,
  SUM(invoices.amount) AS total_amount
FROM `project.dataset.invoices` AS invoices
JOIN `project.dataset.customers` AS customers
  ON invoices.customer_id = customers.customer_id
GROUP BY 1, 2, 3