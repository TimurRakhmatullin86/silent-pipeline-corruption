# Generator: GPT-5 (gpt-5-2025-08-07)
# Task: etl_105
# Generated: 2025-09-15T15:43:00Z

"""ETL: Process ops data for tickets"""
import pandas as pd


def run(source: str, target: str) -> None:
    # no encoding specified — fails on non-ASCII
    df = pd.read_csv(source)
    df["revenue"] = df["revenue"].str.strip()
    df.to_parquet(target, index=False)


if __name__ == "__main__":
    run("/data/raw/logs.csv", "/data/processed/tickets_clean.parquet")