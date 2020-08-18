from typing import List, Set, Dict, Union, TextIO
import arrow
import datetime

from .data import Region, Queue, Tier, Division
from .core import (
    TFTSummoner,
    Realms,
    ProfileIcon,
    LanguageStrings,
    ShardStatus,
    Versions,
    Locales,
    ProfileIcons,
    ChallengerLeague,
    GrandmasterLeague,
    MasterLeague,
    League,
    LeagueSummonerEntries,
    LeagueEntries,
    Patch,
    VerificationString,
)
from .datastores import common as _common_datastore
from ._configuration import Settings, load_config, get_default_config
from . import configuration


# Settings endpoints


def apply_settings(config: Union[str, TextIO, Dict, Settings]):
    if not isinstance(config, (Dict, Settings)):
        config = load_config(config)
    if not isinstance(config, Settings):
        settings = Settings(config)
    else:
        settings = config

    # Load any plugins after everything else has finished importing
    import importlib

    for plugin in settings.plugins:
        imported_plugin = importlib.import_module("lissandra.plugins.{plugin}.monkeypatch".format(plugin=plugin))

    print_calls(settings._Settings__default_print_calls, settings._Settings__default_print_riot_api_key)

    # Overwrite the old settings
    configuration._settings = settings

    # Initialize the pipeline immediately
    _ = configuration.settings.pipeline


def set_riot_api_key(key: str):
    configuration.settings.set_riot_api_key(key)


def set_default_region(region: Union[Region, str]):
    configuration.settings.set_region(region)


def print_calls(calls: bool, api_key: bool = False):
    _common_datastore._print_calls = calls
    _common_datastore._print_api_key = api_key


# Data endpoints


def get_league_entries(summoner: TFTSummoner) -> LeagueEntries:
    return summoner.league_entries


def get_paginated_league_entries(tier: Tier, division: Division, region: Union[Region, str] = None) -> LeagueEntries:
    return LeagueEntries(region=region, tier=tier, division=division)


def get_master_league(queue: Union[Queue, int, str], region: Union[Region, str] = None) -> MasterLeague:
    return MasterLeague(queue=queue, region=region)


def get_grandmaster_league(queue: Union[Queue, int, str], region: Union[Region, str] = None) -> GrandmasterLeague:
    return GrandmasterLeague(queue=queue, region=region)


def get_challenger_league(queue: Union[Queue, int, str], region: Union[Region, str] = None) -> ChallengerLeague:
    return ChallengerLeague(queue=queue, region=region)


def get_tft_summoner(
    *, id: str = None, account_id: str = None, name: str = None, region: Union[Region, str] = None
) -> TFTSummoner:
    return TFTSummoner(id=id, account_id=account_id, name=name, region=region)


def get_profile_icons(region: Union[Region, str] = None) -> ProfileIcons:
    return ProfileIcons(region=region)


def get_realms(region: Union[Region, str] = None) -> Realms:
    return Realms(region=region)


def get_status(region: Union[Region, str] = None) -> ShardStatus:
    return ShardStatus(region=region)


def get_language_strings(region: Union[Region, str] = None) -> LanguageStrings:
    return LanguageStrings(region=region)


def get_locales(region: Union[Region, str] = None) -> List[str]:
    return Locales(region=region)


def get_versions(region: Union[Region, str] = None) -> List[str]:
    return Versions(region=region)


def get_version(date: datetime.date = None, region: Union[Region, str] = None) -> Union[None, str]:
    versions = get_versions(region)
    if date is None:
        return versions[0]
    else:
        patch = Patch.from_date(date, region=region)
        for version in versions:
            if patch.majorminor in version:
                return version
    return None


def get_verification_string(summoner: TFTSummoner) -> VerificationString:
    return VerificationString(summoner=summoner)


# Pipeline


def _get_pipeline():
    return configuration.settings.pipeline
