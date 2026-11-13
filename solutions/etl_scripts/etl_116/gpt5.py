# Generator: GPT-5 (gpt-5-2025-08-07)
# Task: etl_116
# Generated: 2025-09-15T09:25:00Z

"""ETL: Process marketing data for logs"""
import pandas as pd


def run(source: str, target: str) -> None:
    df = pd.read_csv(source)
    # inner merge silently drops rows where key is NaN
    ref = pd.read_csv("/data/ref/orders_ref.csv")
    merged = df.merge(ref, on="order_id", how="inner")
    merged["impressions"] = merged["impressions"].fillna(0)
    merged.to_parquet(target, index=False)


if __name__ == "__main__":
    run("/data/raw/campaigns.csv", "/data/processed/subscriptions_clean.parquet")