# Generator: GPT-5 (gpt-5-2025-08-07)
# Task: etl_102
# Generated: 2025-09-15T09:25:00Z

"""ETL: Process logistics data for campaigns"""
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
    df["clicks"] = pd.to_numeric(df["clicks"], errors="coerce")
    df = df.dropna(subset=["clicks"])
    df["clicks_clean"] = df["clicks"].round(2)
    return df


def load(df: pd.DataFrame, target: str) -> None:
    Path(target).parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(target, index=False)
    logger.info("Loaded %d rows to %s", len(df), target)


if __name__ == "__main__":
    raw = extract("/data/raw/tickets.csv")
    clean = transform(raw)
    load(clean, "/data/processed/campaigns_clean.parquet")