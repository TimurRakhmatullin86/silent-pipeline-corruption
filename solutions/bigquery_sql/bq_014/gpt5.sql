-- Generator: gpt-5-2025-08-07
-- Task: bq_014
-- Generated: 2025-09-04T15:42:27Z

SELECT
  patient_visits.visit_id,
  patient_visits.patient_id,
  patient_visits.diagnosis_code
FROM `project.dataset.patient_visits` AS patient_visits
WHERE patient_visits.load_date >= '2025-01-01'
  AND patient_visits.load_date <= '2025-07-01'
ORDER BY 1