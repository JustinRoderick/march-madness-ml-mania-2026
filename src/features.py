from __future__ import annotations

from pathlib import Path
from typing import Any

from loguru import logger
import pandas as pd

from src.config import DATA_DIR
from src.dataset import TABLES as BRONZE_TABLES

_COMPACT_RESULT: dict[str, str] = {
    "Season": "int64",
    "DayNum": "int64",
    "WTeamID": "int64",
    "WScore": "int64",
    "LTeamID": "int64",
    "LScore": "int64",
    "WLoc": "string",
    "NumOT": "int64",
}

_DETAILED_STATS: dict[str, str] = {
    "WFGM": "int64",
    "WFGA": "int64",
    "WFGM3": "int64",
    "WFGA3": "int64",
    "WFTM": "int64",
    "WFTA": "int64",
    "WOR": "int64",
    "WDR": "int64",
    "WAst": "int64",
    "WTO": "int64",
    "WStl": "int64",
    "WBlk": "int64",
    "WPF": "int64",
    "LFGM": "int64",
    "LFGA": "int64",
    "LFGM3": "int64",
    "LFGA3": "int64",
    "LFTM": "int64",
    "LFTA": "int64",
    "LOR": "int64",
    "LDR": "int64",
    "LAst": "int64",
    "LTO": "int64",
    "LStl": "int64",
    "LBlk": "int64",
    "LPF": "int64",
}

_DETAILED_RESULT = {**_COMPACT_RESULT, **_DETAILED_STATS}

_SCHEMAS: dict[str, dict[str, str]] = {
    "Cities": {
        "CityID": "int64",
        "City": "string",
        "State": "string",
    },
    "Conferences": {
        "ConfAbbrev": "string",
        "Description": "string",
    },
    "MConferenceTourneyGames": {
        "Season": "int64",
        "ConfAbbrev": "string",
        "DayNum": "int64",
        "WTeamID": "int64",
        "LTeamID": "int64",
    },
    "WConferenceTourneyGames": {
        "Season": "int64",
        "ConfAbbrev": "string",
        "DayNum": "int64",
        "WTeamID": "int64",
        "LTeamID": "int64",
    },
    "MGameCities": {
        "Season": "int64",
        "DayNum": "int64",
        "WTeamID": "int64",
        "LTeamID": "int64",
        "CRType": "string",
        "CityID": "int64",
    },
    "WGameCities": {
        "Season": "int64",
        "DayNum": "int64",
        "WTeamID": "int64",
        "LTeamID": "int64",
        "CRType": "string",
        "CityID": "int64",
    },
    "MMasseyOrdinals": {
        "Season": "int64",
        "RankingDayNum": "int64",
        "SystemName": "string",
        "TeamID": "int64",
        "OrdinalRank": "int64",
    },
    "MNCAATourneyCompactResults": _COMPACT_RESULT,
    "WNCAATourneyCompactResults": _COMPACT_RESULT,
    "MNCAATourneyDetailedResults": _DETAILED_RESULT,
    "WNCAATourneyDetailedResults": _DETAILED_RESULT,
    "MNCAATourneySeedRoundSlots": {
        "Seed": "string",
        "GameRound": "int64",
        "GameSlot": "string",
        "EarlyDayNum": "int64",
        "LateDayNum": "int64",
    },
    "MNCAATourneySeeds": {
        "Season": "int64",
        "Seed": "string",
        "TeamID": "int64",
    },
    "WNCAATourneySeeds": {
        "Season": "int64",
        "Seed": "string",
        "TeamID": "int64",
    },
    "MNCAATourneySlots": {
        "Season": "int64",
        "Slot": "string",
        "StrongSeed": "string",
        "WeakSeed": "string",
    },
    "WNCAATourneySlots": {
        "Season": "int64",
        "Slot": "string",
        "StrongSeed": "string",
        "WeakSeed": "string",
    },
    "MRegularSeasonCompactResults": _COMPACT_RESULT,
    "WRegularSeasonCompactResults": _COMPACT_RESULT,
    "MRegularSeasonDetailedResults": _DETAILED_RESULT,
    "WRegularSeasonDetailedResults": _DETAILED_RESULT,
    "MSeasons": {
        "Season": "int64",
        "RegionW": "string",
        "RegionX": "string",
        "RegionY": "string",
        "RegionZ": "string",
    },
    "WSeasons": {
        "Season": "int64",
        "RegionW": "string",
        "RegionX": "string",
        "RegionY": "string",
        "RegionZ": "string",
    },
    "MSecondaryTourneyCompactResults": {
        **_COMPACT_RESULT,
        "SecondaryTourney": "string",
    },
    "WSecondaryTourneyCompactResults": {
        **_COMPACT_RESULT,
        "SecondaryTourney": "string",
    },
    "MSecondaryTourneyTeams": {
        "Season": "int64",
        "SecondaryTourney": "string",
        "TeamID": "int64",
    },
    "WSecondaryTourneyTeams": {
        "Season": "int64",
        "SecondaryTourney": "string",
        "TeamID": "int64",
    },
    "MTeamCoaches": {
        "Season": "int64",
        "TeamID": "int64",
        "FirstDayNum": "int64",
        "LastDayNum": "int64",
        "CoachName": "string",
    },
    "MTeamConferences": {
        "Season": "int64",
        "TeamID": "int64",
        "ConfAbbrev": "string",
    },
    "WTeamConferences": {
        "Season": "int64",
        "TeamID": "int64",
        "ConfAbbrev": "string",
    },
    "MTeamSpellings": {
        "TeamNameSpelling": "string",
        "TeamID": "int64",
    },
    "WTeamSpellings": {
        "TeamNameSpelling": "string",
        "TeamID": "int64",
    },
    "MTeams": {
        "TeamID": "int64",
        "TeamName": "string",
        "FirstD1Season": "int64",
        "LastD1Season": "int64",
    },
    "WTeams": {
        "TeamID": "int64",
        "TeamName": "string",
    },
    "SampleSubmissionStage1": {
        "ID": "string",
        "Pred": "float64",
    },
    "SampleSubmissionStage2": {
        "ID": "string",
        "Pred": "float64",
    },
}


def _drop_ingest_artifacts(df: pd.DataFrame) -> pd.DataFrame:
    if "_source_file" in df.columns:
        df = df.drop(columns=["_source_file"])
    return df


def _apply_schema(df: pd.DataFrame, schema: dict[str, str]) -> pd.DataFrame:
    present = {c: t for c, t in schema.items() if c in df.columns}
    if not present:
        return df
    return df.astype(present, copy=False)


def _strip_string_columns(df: pd.DataFrame) -> pd.DataFrame:
    str_cols = df.select_dtypes(include="string").columns
    for c in str_cols:
        df[c] = df[c].str.strip()
    return df


def _parse_seasons_dayzero(df: pd.DataFrame) -> pd.DataFrame:
    if "DayZero" not in df.columns:
        return df
    out = df.copy()
    parsed = pd.to_datetime(out["DayZero"], format="%m/%d/%Y", errors="coerce")
    out["DayZero"] = parsed.dt.normalize()
    return out


def clean_table(name: str, df: pd.DataFrame) -> pd.DataFrame:
    df = _drop_ingest_artifacts(df)
    if name in ("MSeasons", "WSeasons"):
        df = _parse_seasons_dayzero(df)

    df = df.drop_duplicates()
    df = df.dropna()

    schema = _SCHEMAS[name]
    df = _apply_schema(df, schema)
    df = _strip_string_columns(df)

    return df


def main(
    bronze_dir: Path = DATA_DIR / "interim",
    parquet_dir: Path = DATA_DIR / "processed",
) -> dict[str, Any]:
    parquet_dir.mkdir(parents=True, exist_ok=True)

    summary: dict[str, Any] = {"tables": {}}

    for table in BRONZE_TABLES:
        path = bronze_dir / f"{table}.parquet"
        if not path.exists():
            logger.warning("Skipping missing bronze table: {}", path)
            continue

        df = pd.read_parquet(path)
        raw_len = len(df)
        cleaned = clean_table(table, df)
        out_path = parquet_dir / f"{table}.parquet"
        cleaned.to_parquet(out_path, index=False)

        summary["tables"][table] = {
            "rows_in": raw_len,
            "rows_out": len(cleaned),
            "path": str(out_path),
        }
        logger.info(
            "Cleaned {}: {:,} -> {:,} rows -> {}",
            table,
            raw_len,
            len(cleaned),
            out_path,
        )

    logger.success("Silver cleaning complete. Wrote {} tables to {}", len(summary["tables"]), parquet_dir)
    return summary


if __name__ == "__main__":
    main()
