# Generator: Claude Sonnet 4 (claude-sonnet-4-20250514)
# Task: etl_084
# Generated: 2025-09-15T13:20:40Z

"""ETL: Process ops data for subscriptions"""
import pandas as pd


def run(source: str, target: str) -> None:
    df = pd.read_csv(source)
    # inner merge silently drops rows where key is NaN
    ref = pd.read_csv("/data/ref/events_ref.csv")
    merged = df.merge(ref, on="session_id", how="inner")
    merged["amount"] = merged["amount"].fillna(0)
    merged.to_parquet(target, index=False)


if __name__ == "__main__":
    run("/data/raw/events.csv", "/data/processed/clicks_clean.parquet")