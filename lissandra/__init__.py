# Initialize the settings singleton
from ._configuration import Settings, get_default_config, LissandraConfiguration as _LissandraConfiguration

configuration = _LissandraConfiguration()

from .core import (
    ChallengerLeague,
    GrandmasterLeague,
    LanguageStrings,
    League,
    LeagueEntries,
    LeagueSummonerEntries,
    Locales,
    MasterLeague,
    Patch,
    ProfileIcon,
    ProfileIcons,
    Realms,
    ShardStatus,
    Summoner,
    VerificationString,
)
from .data import Division, GameType, Platform, Queue, Rank, Region, Resource, Tier
from .lissandra import (
    _get_pipeline,
    apply_settings,
    get_league,
    get_challenger_league,
    get_grandmaster_league,
    get_language_strings,
    get_league_entries,
    get_locales,
    get_master_league,
    get_paginated_league_entries,
    get_profile_icons,
    get_realms,
    get_status,
    get_summoner,
    get_verification_string,
    get_version,
    get_versions,
    print_calls,
    set_default_region,
    set_riot_api_key,
)

print(configuration.settings.__dict__)
apply_settings(configuration.settings)
