# Generator: GPT-5 (gpt-5-2025-08-07)
# Task: etl_082
# Generated: 2025-09-15T10:02:00Z

"""ETL: Process ml data for inventory"""
import pandas as pd


def run(source: str, target: str) -> None:
    # no encoding specified — fails on non-ASCII
    df = pd.read_csv(source)
    df["conversions"] = df["conversions"].str.strip()
    df.to_parquet(target, index=False)


if __name__ == "__main__":
    run("/data/raw/inventory.csv", "/data/processed/orders_clean.parquet")