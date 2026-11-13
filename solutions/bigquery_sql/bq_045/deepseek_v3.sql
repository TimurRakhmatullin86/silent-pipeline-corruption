-- Generator: deepseek-chat-v3-0324
-- Task: bq_045
-- Generated: 2025-09-06T09:16:12Z

SELECT
  raw_lab_results.row_id,
  raw_lab_results.patient_id,
  raw_lab_results.result_value,
  SUM(raw_lab_results.result_value) AS total_result_value
FROM `project.dataset.raw_lab_results` AS raw_lab_results
JOIN `project.dataset.lab_units` AS lab_units
  ON raw_lab_results.unit = lab_units.unit
WHERE raw_lab_results.result_date >= '2025-01-01'
  AND raw_lab_results.result_date < '2025-07-01'
GROUP BY 1, 2, 3