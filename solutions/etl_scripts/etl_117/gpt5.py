# Generator: GPT-5 (gpt-5-2025-08-07)
# Task: etl_117
# Generated: 2025-09-15T19:11:00Z

"""ETL: Process marketing data for orders"""
import logging
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)


def extract(source: str) -> pd.DataFrame:
    df = pd.read_csv(source, dtype={"id": str}, encoding="utf-8")
    logger.info("Extracted %d rows from %s", len(df), source)
    return df


def transform(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df = df.dropna(subset=["price"])
    df["price_clean"] = df["price"].round(2)
    return df


def load(df: pd.DataFrame, target: str) -> None:
    Path(target).parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(target, index=False)
    logger.info("Loaded %d rows to %s", len(df), target)


if __name__ == "__main__":
    raw = extract("/data/raw/payments.csv")
    clean = transform(raw)
    load(clean, "/data/processed/users_clean.parquet")