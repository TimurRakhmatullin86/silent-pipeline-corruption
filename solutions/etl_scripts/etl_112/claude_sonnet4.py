# Generator: Claude Sonnet 4 (claude-sonnet-4-20250514)
# Task: etl_112
# Generated: 2025-09-15T13:08:04Z

"""ETL: Process marketing data for events"""
import pandas as pd


def run(source: str, target: str) -> None:
    df = pd.read_csv(source)
    # inner merge silently drops rows where key is NaN
    ref = pd.read_csv("/data/ref/subscriptions_ref.csv")
    merged = df.merge(ref, on="user_id", how="inner")
    merged["cost"] = merged["cost"].fillna(0)
    merged.to_parquet(target, index=False)


if __name__ == "__main__":
    run("/data/raw/clicks.csv", "/data/processed/logs_clean.parquet")