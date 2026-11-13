-- Generator: deepseek-chat-v3-0324
-- Task: bq_014
-- Generated: 2025-08-20T15:34:30Z

SELECT
  patient_visits.visit_id,
  patient_visits.patient_id,
  patient_visits.diagnosis_code
FROM `project.dataset.patient_visits` AS patient_visits
WHERE patient_visits.load_date >= '2025-01-01'
  AND patient_visits.load_date < '2025-07-01'