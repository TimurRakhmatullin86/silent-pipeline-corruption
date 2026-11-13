-- Generator: DeepSeek-V3 (deepseek-chat-v3-0324)
-- Task: bq_068
-- Generated: 2025-09-15T11:39:26Z

SELECT
  a.merchant_id,
  b.updated_at,
  SUM(a.cost) AS total
FROM `project.dataset.orders` a
JOIN `project.dataset.inventory` b
  ON a.merchant_id = b.merchant_id
WHERE a._PARTITIONTIME >= timestamp('2025-09-01')
GROUP BY 1, 2