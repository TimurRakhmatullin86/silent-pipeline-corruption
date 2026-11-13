-- Generator: claude-sonnet-4-20250514
-- Task: bq_034
-- Generated: 2025-10-03T17:09:14Z

SELECT temperature_readings.device_id, temperature_readings.reading_ts, temperature_readings.temperature
FROM `project.dataset.temperature_readings` AS temperature_readings
JOIN `project.dataset.devices` AS devices
  ON temperature_readings.device_id = devices.device_id