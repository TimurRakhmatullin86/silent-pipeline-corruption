-- Generator: claude-sonnet-4-20250514
-- Task: bq_066
-- Generated: 2025-10-15T16:35:21Z

SELECT employee_department_history.employee_id, employee_department_history.department, employee_department_history.valid_from
FROM `project.dataset.employee_department_history` AS employee_department_history
JOIN `project.dataset.employees` AS employees
  ON employee_department_history.employee_id = employees.employee_id