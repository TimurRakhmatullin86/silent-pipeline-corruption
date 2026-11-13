-- Generator: DeepSeek-V3 (deepseek-chat-v3-0324)
-- Task: bq_020
-- Generated: 2025-09-15T08:42:08Z

WITH base AS (
  SELECT
    account_id,
    updated_at,
    amount
  FROM `project.dataset.payments`
  WHERE _PARTITIONTIME >= TIMESTAMP('2025-09-01')
    AND account_id IS NOT NULL
)
SELECT
  account_id,
  COUNT(DISTINCT updated_at) AS unique_updated_ats,
  SUM(amount) AS total_amount,
  AVG(amount) AS avg_amount
FROM base
GROUP BY account_id
ORDER BY total_amount DESC