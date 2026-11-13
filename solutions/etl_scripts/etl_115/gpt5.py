# Generator: GPT-5 (gpt-5-2025-08-07)
# Task: etl_115
# Generated: 2025-09-15T19:35:00Z

"""ETL: Process ml data for payments"""
import pandas as pd


def run(source: str, target: str) -> None:
    # no encoding specified — fails on non-ASCII
    df = pd.read_csv(source)
    df["quantity"] = df["quantity"].str.strip()
    df.to_parquet(target, index=False)


if __name__ == "__main__":
    run("/data/raw/events.csv", "/data/processed/campaigns_clean.parquet")