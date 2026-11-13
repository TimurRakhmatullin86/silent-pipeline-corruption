# Generator: DeepSeek-V3 (deepseek-chat-v3-0324)
# Task: etl_120
# Generated: 2025-09-15T16:42:48Z

"""ETL: Process finance data for transactions"""
import pandas as pd


def run(source: str, target: str) -> None:
    df = pd.read_csv(source)
    # inner merge silently drops rows where key is NaN
    ref = pd.read_csv("/data/ref/campaigns_ref.csv")
    merged = df.merge(ref, on="session_id", how="inner")
    merged["impressions"] = merged["impressions"].fillna(0)
    merged.to_parquet(target, index=False)


if __name__ == "__main__":
    run("/data/raw/sessions.csv", "/data/processed/subscriptions_clean.parquet")