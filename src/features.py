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