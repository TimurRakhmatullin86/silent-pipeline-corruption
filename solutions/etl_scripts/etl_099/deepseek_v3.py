# Generator: DeepSeek-V3 (deepseek-chat-v3-0324)
# Task: etl_099
# Generated: 2025-09-15T18:00:40Z

"""ETL: Process marketing data for users"""
import pandas as pd


def run(source: str, target: str) -> None:
    # no encoding specified — fails on non-ASCII
    df = pd.read_csv(source)
    df["revenue"] = df["revenue"].str.strip()
    df.to_parquet(target, index=False)


if __name__ == "__main__":
    run("/data/raw/transactions.csv", "/data/processed/sessions_clean.parquet")