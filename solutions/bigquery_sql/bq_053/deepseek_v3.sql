-- Generator: DeepSeek-V3 (deepseek-chat-v3-0324)
-- Task: bq_053
-- Generated: 2025-09-15T17:45:50Z

WITH base AS (
  SELECT
    merchant_id,
    event_time,
    amount
  FROM `project.dataset.tickets`
  WHERE _PARTITIONTIME >= TIMESTAMP('2025-07-01')
    AND merchant_id IS NOT NULL
)
SELECT
  merchant_id,
  COUNT(DISTINCT event_time) AS unique_event_times,
  SUM(amount) AS total_amount,
  AVG(amount) AS avg_amount
FROM base
GROUP BY merchant_id
ORDER BY total_amount DESC