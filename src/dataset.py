import pandas as pd
import numpy as np
from pathlib import Path
from loguru import logger

from src.config import DATA_DIR

RAW_DIR = DATA_DIR / "raw"

TABLES: dict[str, str] = {
    "Cities": str(RAW_DIR / "Cities.csv"),
    "Conferences": str(RAW_DIR / "Conferences.csv"),
    "MConferenceTourneyGames": str(RAW_DIR / "MConferenceTourneyGames.csv"),
    "MGameCities": str(RAW_DIR / "MGameCities.csv"),
    "MMasseyOrdinals": str(RAW_DIR / "MMasseyOrdinals.csv"),
    "MNCAATourneyCompactResults": str(RAW_DIR / "MNCAATourneyCompactResults.csv"),
    "MNCAATourneyDetailedResults": str(RAW_DIR / "MNCAATourneyDetailedResults.csv"),
    "MNCAATourneySeedRoundSlots": str(RAW_DIR / "MNCAATourneySeedRoundSlots.csv"),
    "MNCAATourneySeeds": str(RAW_DIR / "MNCAATourneySeeds.csv"),
    "MNCAATourneySlots": str(RAW_DIR / "MNCAATourneySlots.csv"),
    "MRegularSeasonCompactResults": str(RAW_DIR / "MRegularSeasonCompactResults.csv"),
    "MRegularSeasonDetailedResults": str(RAW_DIR / "MRegularSeasonDetailedResults.csv"),
    "MSecondaryTourneyCompactResults": str(RAW_DIR / "MSecondaryTourneyCompactResults.csv"),
    "MSecondaryTourneyTeams": str(RAW_DIR / "MSecondaryTourneyTeams.csv"),
    "MSeasons": str(RAW_DIR / "MSeasons.csv"),
    "MTeamConferences": str(RAW_DIR / "MTeamConferences.csv"),
    "MTeamCoaches": str(RAW_DIR / "MTeamCoaches.csv"),
    "MTeamSpellings": str(RAW_DIR / "MTeamSpellings.csv"),
    "MTeams": str(RAW_DIR / "MTeams.csv"),
    "SampleSubmissionStage1": str(RAW_DIR / "SampleSubmissionStage1.csv"),
    "SampleSubmissionStage2": str(RAW_DIR / "SampleSubmissionStage2.csv"),
    "WConferenceTourneyGames": str(RAW_DIR / "WConferenceTourneyGames.csv"),
    "WGameCities": str(RAW_DIR / "WGameCities.csv"),
    "WNCAATourneyCompactResults": str(RAW_DIR / "WNCAATourneyCompactResults.csv"),
    "WNCAATourneyDetailedResults": str(RAW_DIR / "WNCAATourneyDetailedResults.csv"),
    "WNCAATourneySeeds": str(RAW_DIR / "WNCAATourneySeeds.csv"),
    "WNCAATourneySlots": str(RAW_DIR / "WNCAATourneySlots.csv"),
    "WRegularSeasonCompactResults": str(RAW_DIR / "WRegularSeasonCompactResults.csv"),
    "WRegularSeasonDetailedResults": str(RAW_DIR / "WRegularSeasonDetailedResults.csv"),
    "WSecondaryTourneyCompactResults": str(RAW_DIR / "WSecondaryTourneyCompactResults.csv"),
    "WSecondaryTourneyTeams": str(RAW_DIR / "WSecondaryTourneyTeams.csv"),
    "WSeasons": str(RAW_DIR / "WSeasons.csv"),
    "WTeamConferences": str(RAW_DIR / "WTeamConferences.csv"),
    "WTeamSpellings": str(RAW_DIR / "WTeamSpellings.csv"),
    "WTeams": str(RAW_DIR / "WTeams.csv"),
}

def main(
    raw_dir: Path = RAW_DIR,
    bronze_dir: Path = DATA_DIR / "interim",
    fmt: str = "parquet",
):

    logger.info(f"Reading raw tables from: {raw_dir}")
    logger.info(f"Writing bronze tables to: {bronze_dir} (fmt={fmt})")

    for table_name, filename in TABLES.items():
        src = Path(filename)
        if not src.exists():
            raise FileNotFoundError(
                f"Missing expected raw file for table={table_name}: {src}.\n"
                "If you moved files, update OLIST_TABLES or pass --raw-dir."
            )

        df = pd.read_csv(src)

        if fmt.lower() == "parquet":
            try:
                out = bronze_dir / f"{table_name}.parquet"
                df.to_parquet(out, index=False)
            except Exception as e:
                logger.warning(
                    "Parquet write failed (missing engine like pyarrow?). "
                    "Falling back to CSV. Error was: {}",
                    repr(e),
                )
                out = bronze_dir / f"{table_name}.csv"
                df.to_csv(out, index=False)
        else:
            out = bronze_dir / f"{table_name}.csv"
            df.to_csv(out, index=False)

        logger.info(f"Wrote bronze table {table_name}: {out} (rows={len(df):,})")

    logger.success("Bronze ingestion complete.")


if __name__ == "__main__":
    main()