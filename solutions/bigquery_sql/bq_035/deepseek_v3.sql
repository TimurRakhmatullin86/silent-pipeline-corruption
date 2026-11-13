-- Generator: DeepSeek-V3 (deepseek-chat-v3-0324)
-- Task: bq_035
-- Generated: 2025-09-15T13:21:54Z

SELECT
  a.account_id,
  b.updated_at,
  SUM(a.conversions) AS total
FROM `project.dataset.orders` a
JOIN `project.dataset.shipments` b
  ON a.account_id = b.account_id
WHERE a._PARTITIONTIME >= TIMESTAMP('2025-05-01')
GROUP BY 1, 2