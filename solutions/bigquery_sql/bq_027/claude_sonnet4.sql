-- Generator: claude-sonnet-4-20250514
-- Task: bq_027
-- Generated: 2025-10-08T12:59:35Z

SELECT shipments.shipment_id, shipments.order_id, shipments.warehouse_id
FROM `project.dataset.shipments` AS shipments
JOIN `project.dataset.warehouses` AS warehouses
  ON shipments.warehouse_id = warehouses.warehouse_id
JOIN `project.dataset.carriers` AS carriers
  ON shipments.carrier_id = carriers.carrier_id