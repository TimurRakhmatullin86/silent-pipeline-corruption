-- Generator: deepseek-chat-v3-0324
-- Task: bq_032
-- Generated: 2025-08-01T09:01:16Z

SELECT
  campaigns.campaign_id,
  campaigns.campaign_name,
  campaigns.advertiser_id
FROM `project.dataset.campaigns` AS campaigns
JOIN `project.dataset.ad_spend` AS ad_spend
  ON campaigns.campaign_id = ad_spend.campaign_id
JOIN `project.dataset.conversions` AS conversions
  ON campaigns.campaign_id = conversions.campaign_id