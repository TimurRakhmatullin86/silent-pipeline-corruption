# Generator: Claude Sonnet 4 (claude-sonnet-4-20250514)
# Task: etl_111
# Generated: 2025-09-15T14:22:41Z

"""ETL: Process ops data for campaigns"""
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
    df["duration"] = pd.to_numeric(df["duration"], errors="coerce")
    df = df.dropna(subset=["duration"])
    df["duration_clean"] = df["duration"].round(2)
    return df


def load(df: pd.DataFrame, target: str) -> None:
    Path(target).parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(target, index=False)
    logger.info("Loaded %d rows to %s", len(df), target)


if __name__ == "__main__":
    raw = extract("/data/raw/logs.csv")
    clean = transform(raw)
    load(clean, "/data/processed/shipments_clean.parquet")