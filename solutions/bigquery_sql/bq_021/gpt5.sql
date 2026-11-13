-- Generator: gpt-5-2025-08-07
-- Task: bq_021
-- Generated: 2025-10-19T10:38:24Z

SELECT
  employees.employee_id,
  employees.department_id,
  employees.salary
FROM `project.dataset.employees` AS employees
JOIN `project.dataset.departments` AS departments
  ON employees.department_id = departments.department_id
WHERE employees.termination_date >= '2025-01-01'
  AND employees.termination_date < '2025-07-01'
ORDER BY 1