-- Generator: deepseek-chat-v3-0324
-- Task: bq_052
-- Generated: 2025-10-12T11:04:53Z

SELECT
  touches.touch_id,
  touches.user_id,
  touches.channel
FROM `project.dataset.touches` AS touches
JOIN `project.dataset.conversions` AS conversions
  ON touches.user_id = conversions.user_id