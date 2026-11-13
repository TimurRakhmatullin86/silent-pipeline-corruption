-- Generator: gpt-5-2025-08-07
-- Task: bq_042
-- Generated: 2025-08-05T12:12:02Z

SELECT
  shipments.shipment_id,
  shipments.zone,
  shipments.weight_kg
FROM `project.dataset.shipments` AS shipments
JOIN `project.dataset.rate_brackets` AS rate_brackets
  ON shipments.zone = rate_brackets.zone
ORDER BY 1