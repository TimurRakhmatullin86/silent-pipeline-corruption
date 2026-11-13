-- Generator: deepseek-chat-v3-0324
-- Task: bq_066
-- Generated: 2025-09-07T12:54:10Z

SELECT
  employee_department_history.employee_id,
  employee_department_history.department,
  employee_department_history.valid_from
FROM `project.dataset.employee_department_history` AS employee_department_history
CROSS JOIN `project.dataset.employees` AS employees