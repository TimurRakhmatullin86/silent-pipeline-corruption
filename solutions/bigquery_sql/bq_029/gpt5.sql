-- Generator: gpt-5-2025-08-07
-- Task: bq_029
-- Generated: 2025-09-15T09:22:15Z

SELECT
  carriers.carrier_id,
  carriers.carrier_name
FROM `project.dataset.carriers` AS carriers
JOIN `project.dataset.shipments` AS shipments
  ON carriers.carrier_id = shipments.carrier_id
ORDER BY 1