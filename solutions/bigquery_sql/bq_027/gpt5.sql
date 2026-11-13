-- Generator: gpt-5-2025-08-07
-- Task: bq_027
-- Generated: 2025-08-04T13:35:36Z

SELECT
  shipments.shipment_id,
  shipments.order_id,
  shipments.warehouse_id
FROM `project.dataset.shipments` AS shipments
JOIN `project.dataset.warehouses` AS warehouses
  ON shipments.warehouse_id = warehouses.warehouse_id
JOIN `project.dataset.carriers` AS carriers
  ON shipments.carrier_id = carriers.carrier_id
ORDER BY 1