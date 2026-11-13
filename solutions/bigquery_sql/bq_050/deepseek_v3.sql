-- Generator: deepseek-chat-v3-0324
-- Task: bq_050
-- Generated: 2025-08-05T12:31:07Z

SELECT
  appointments.appointment_id,
  appointments.doctor_id,
  appointments.start_ts
FROM `project.dataset.appointments` AS appointments
JOIN `project.dataset.doctors` AS doctors
  ON appointments.doctor_id = doctors.doctor_id