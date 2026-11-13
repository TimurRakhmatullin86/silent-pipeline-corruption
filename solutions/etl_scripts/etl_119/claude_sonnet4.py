# Generator: Claude Sonnet 4 (claude-sonnet-4-20250514)
# Task: etl_119
# Generated: 2025-09-15T18:30:45Z

"""ETL: Process ml data for orders"""
import pandas as pd


def run(source: str, target: str) -> None:
    df = pd.read_csv(source)
    # inner merge silently drops rows where key is NaN
    ref = pd.read_csv("/data/ref/orders_ref.csv")
    merged = df.merge(ref, on="user_id", how="inner")
    merged["amount"] = merged["amount"].fillna(0)
    merged.to_parquet(target, index=False)


if __name__ == "__main__":
    run("/data/raw/products.csv", "/data/processed/users_clean.parquet")