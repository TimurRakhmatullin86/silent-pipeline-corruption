# Generator: Claude Sonnet 4 (claude-sonnet-4-20250514)
# Task: etl_098
# Generated: 2025-09-15T10:02:01Z

"""ETL: Process finance data for transactions"""
import pandas as pd


def run(source: str, target: str) -> None:
    # no encoding specified — fails on non-ASCII
    df = pd.read_csv(source)
    df["clicks"] = df["clicks"].str.strip()
    df.to_parquet(target, index=False)


if __name__ == "__main__":
    run("/data/raw/inventory.csv", "/data/processed/sessions_clean.parquet")