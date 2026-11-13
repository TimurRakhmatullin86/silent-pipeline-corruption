-- Generator: deepseek-chat-v3-0324
-- Task: bq_042
-- Generated: 2025-10-21T12:23:39Z

SELECT
  shipments.status,
  shipments.shipment_id,
  shipments.zone,
  shipments.weight_kg
FROM `project.dataset.shipments` AS shipments
JOIN `project.dataset.rate_brackets` AS rate_brackets
  ON shipments.zone = rate_brackets.zone