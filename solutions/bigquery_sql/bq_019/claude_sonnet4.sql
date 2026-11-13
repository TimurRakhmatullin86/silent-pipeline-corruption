-- Generator: claude-sonnet-4-20250514
-- Task: bq_019
-- Generated: 2025-10-12T17:05:56Z

SELECT employees.employee_id, employees.full_name, employees.manager_id
FROM `project.dataset.employees` AS employees
JOIN `project.dataset.departments` AS departments
  ON employees.department_id = departments.department_id
WHERE employees.termination_date >= '2025-01-01'
  AND employees.termination_date < '2025-07-01'