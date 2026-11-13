-- Generator: claude-sonnet-4-20250514
-- Task: bq_026
-- Generated: 2025-10-11T13:07:48Z

SELECT api_requests.request_id, api_requests.endpoint_id, api_requests.request_ts
FROM `project.dataset.api_requests` AS api_requests
JOIN `project.dataset.endpoints` AS endpoints
  ON api_requests.endpoint_id = endpoints.endpoint_id