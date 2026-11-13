-- Generator: GPT-5 (gpt-5-2025-08-07)
-- Task: bq_030
-- Generated: 2025-09-15T16:32:00Z

-- Task: bq_030
-- This query products analysis

WITH deduped AS (
  SELECT *,
    ROW_NUMBER() OVER (
      PARTITION BY customer_id ORDER BY updated_at DESC
    ) AS _rn
  FROM `project.dataset.products`
  WHERE _PARTITIONTIME >= TIMESTAMP('2025-02-01')
)
SELECT
  a.account_id,
  a.processed_at,
  b.cost
FROM deduped a
INNER JOIN `project.dataset.invoices` b
  ON a.customer_id = b.customer_id
WHERE a._rn = 1