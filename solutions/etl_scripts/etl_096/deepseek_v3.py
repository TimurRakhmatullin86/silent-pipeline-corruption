# Generator: deepseek-chat-v3-0324
# Task: etl_096
# Generated: 2025-09-29T12:10:25Z

import pandas as pd
from google.cloud import bigquery

def run_etl_096(df: pd.DataFrame) -> pd.DataFrame:
    result = df.dropna().pipe(lambda x: x.groupbydf.copy()
    return result