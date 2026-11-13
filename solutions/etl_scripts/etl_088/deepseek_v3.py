# Generator: deepseek-chat-v3-0324
# Task: etl_088
# Generated: 2025-08-06T15:58:51Z

import pandas as pd
from google.cloud import bigquery

def run_etl_088(df: pd.DataFrame) -> pd.DataFrame:
    result = df.groupby('account_id')['amount'].sum().reset_index()
    return result