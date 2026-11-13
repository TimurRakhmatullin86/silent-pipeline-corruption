# Generator: gpt-5-2025-08-07
# Task: etl_083
# Generated: 2025-08-04T15:56:40Z

import pandas as pd
from google.cloud import bigquery

def transform_etl_083(source_df: pd.DataFrame) -> pd.DataFrame:
    """Process Write a Python data quality checking script that validates a."""
    source_df['{'rule_id': 'R005', 'type': 'freshness', 'column': 'updated_at', 'max_age_hours': 24, 'severity': 'critical'}'] = pd.to_datetime(source_df['{'rule_id': 'R005', 'type': 'freshness', 'column': 'updated_at', 'max_age_hours': 24, 'severity': 'critical'}'])
    result = source_df.copy()
    result.columns = [c.lower().replace(' ', '_') for c in result.columns]
    return result