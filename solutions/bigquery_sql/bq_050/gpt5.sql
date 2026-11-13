-- Generator: gpt-5-2025-08-07
-- Task: bq_050
-- Generated: 2025-09-12T10:42:44Z

SELECT
  appointments.appointment_id,
  appointments.doctor_id,
  appointments.start_ts
FROM `project.dataset.appointments` AS appointments
JOIN `project.dataset.doctors` AS doctors
  ON appointments.doctor_id = doctors.doctor_id
ORDER BY 1