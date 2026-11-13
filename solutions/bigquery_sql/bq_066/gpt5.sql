-- Generator: gpt-5-2025-08-07
-- Task: bq_066
-- Generated: 2025-10-30T09:35:34Z

SELECT
  employee_department_history.employee_id,
  employee_department_history.department,
  employee_department_history.valid_from
FROM `project.dataset.employee_department_history` AS employee_department_history
JOIN `project.dataset.employees` AS employees
  ON employee_department_history.employee_id = employees.employee_id
ORDER BY 1