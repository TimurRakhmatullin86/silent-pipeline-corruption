-- Generator: claude-sonnet-4-20250514
-- Task: bq_042
-- Generated: 2025-08-10T12:54:50Z

SELECT shipments.shipment_id, shipments.zone, shipments.weight_kg
FROM `project.dataset.shipments` AS shipments
JOIN `project.dataset.rate_brackets` AS rate_brackets
  ON shipments.zone = rate_brackets.zone