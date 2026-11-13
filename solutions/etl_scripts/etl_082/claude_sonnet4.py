# Generator: Claude Sonnet 4 (claude-sonnet-4-20250514)
# Task: etl_082
# Generated: 2025-09-15T11:04:02Z

"""ETL: Process ml data for inventory"""
import pandas as pd


def run(source: str, target: str) -> None:
    df = pd.read_csv(source)
    # inner merge silently drops rows where key is NaN
    ref = pd.read_csv("/data/ref/events_ref.csv")
    merged = df.merge(ref, on="product_id", how="inner")
    merged["conversions"] = merged["conversions"].fillna(0)
    merged.to_parquet(target, index=False)


if __name__ == "__main__":
    run("/data/raw/inventory.csv", "/data/processed/orders_clean.parquet")