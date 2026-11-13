-- Generator: claude-sonnet-4-20250514
-- Task: bq_022
-- Generated: 2025-08-18T08:22:34Z

SELECT sensor_readings.device_id, sensor_readings.reading_ts, sensor_readings.metric, SUM(sensor_readings.value) AS total_value
FROM `project.dataset.sensor_readings` AS sensor_readings
JOIN `project.dataset.devices` AS devices
  ON sensor_readings.device_id = devices.device_id
GROUP BY 1, 2, 3