from typing import Tuple, Set, Union, MutableMapping, Any, Mapping, Iterable, Generator, List

from datapipelines import Query, PipelineContext, QueryValidationError

from ..data import Region, Platform, Tier, Division

from ..dto.league import LeagueEntriesDto, LeagueSummonerEntriesDto, LeagueEntryDto
from ..dto.staticdata import (
    LanguageStringsDto,
    LanguagesDto,
    ProfileIconDataDto,
    ProfileIconDetailsDto,
    RealmDto,
    VersionListDto,
)
from ..dto.status import ShardStatusDto
from ..dto.summoner import SummonerDto

from ..core.league import (
    LeagueSummonerEntries,
    ChallengerLeague,
    GrandmasterLeague,
    MasterLeague,
    League,
    LeagueEntry,
)
from ..core.staticdata import (
    Locales,
    LanguageStrings,
    ProfileIcon,
    ProfileIcons,
    Realms,
    Versions,
)
from ..core.status import ShardStatus
from ..core.summoner import Summoner, SummonerData

from .util import (
    get_default_locale,
    get_default_version,
    rgetattr,
    region_to_platform_generator,
    convert_region_to_platform,
    hash_included_data,
)


#######
# DTO #
#######


##############
# League API #
##############

validate_league_entries_dto_query = (
    Query.has("platform").as_(Platform).also.has("tier").as_(Tier).also.has("page").as_(int).also.has("id").as_(int)
)  # League ID


def for_league_entries_dto(league_entries: LeagueEntriesDto) -> Tuple[str, str, int, int]:
    return (
        league_entries["platform"],
        league_entries["tier"],
        league_entries["id"],
        league_entries["page"],
    )


def for_league_entries_dto_query(query: Query) -> Tuple[str, str, int, int]:
    return query["platform"].value, query["tier"].value, query["id"], query["page"]


validate_league_summoner_entries_dto_query = Query.has("platform").as_(Platform).also.has("id").as_(int)  # Summoner ID


def for_league_summoner_entries_dto(league_entries: LeagueEntriesDto) -> Tuple[str, int]:
    return league_entries["platform"], league_entries["id"]


def for_league_summoner_entries_dto_query(query: Query) -> Tuple[str, int]:
    return query["platform"].value, query["id"]


###################
# Static Data API #
###################

# Language


validate_language_strings_dto_query = (
    Query.has("platform")
    .as_(Platform)
    .also.can_have("version")
    .with_default(get_default_version, supplies_type=str)
    .also.can_have("locale")
    .with_default(get_default_locale, supplies_type=str)
)


validate_many_language_strings_dto_query = (
    Query.has("platforms")
    .as_(Iterable)
    .also.can_have("version")
    .with_default(get_default_version, supplies_type=str)
    .also.can_have("locale")
    .with_default(get_default_locale, supplies_type=str)
)


def for_language_strings_dto(language_strings: LanguageStringsDto) -> Tuple[str, str, str]:
    return language_strings["platform"], language_strings["version"], language_strings["locale"]


def for_language_strings_dto_query(query: Query) -> Tuple[str, str, str]:
    return query["platform"].value, query["version"], query["locale"]


def for_many_language_strings_dto_query(query: Query) -> Generator[Tuple[str, str, str], None, None]:
    for platform in query["platforms"]:
        try:
            platform = Platform(platform)
            yield platform.value, query["version"], query["locale"]
        except ValueError as e:
            raise QueryValidationError from e


validate_languages_dto_query = Query.has("platform").as_(Platform)


validate_many_languages_dto_query = Query.has("platforms").as_(Iterable)


def for_languages_dto(languages: LanguagesDto) -> str:
    return languages["platform"]


def for_languages_dto_query(query: Query) -> str:
    return query["platform"].value


def for_many_languages_dto_query(query: Query) -> Generator[str, None, None]:
    for platform in query["platforms"]:
        try:
            platform = Platform(platform)
            yield platform.value
        except ValueError as e:
            raise QueryValidationError from e


# Profile Icon


validate_profile_icon_data_dto_query = (
    Query.has("platform")
    .as_(Platform)
    .also.can_have("version")
    .with_default(get_default_version, supplies_type=str)
    .also.can_have("locale")
    .with_default(get_default_locale, supplies_type=str)
)


validate_many_profile_icon_data_dto_query = (
    Query.has("platforms")
    .as_(Iterable)
    .also.can_have("version")
    .with_default(get_default_version, supplies_type=str)
    .also.can_have("locale")
    .with_default(get_default_locale, supplies_type=str)
)


def for_profile_icon_data_dto(profile_icon_data: ProfileIconDataDto) -> Tuple[str, str, str]:
    return profile_icon_data["platform"], profile_icon_data["version"], profile_icon_data["locale"]


def for_profile_icon_data_dto_query(query: Query) -> Tuple[str, str, str]:
    return query["platform"].value, query["version"], query["locale"]


def for_many_profile_icon_data_dto_query(query: Query) -> Generator[Tuple[str, str, str], None, None]:
    for platform in query["platforms"]:
        try:
            platform = Platform(platform)
            yield platform.value, query["version"], query["locale"]
        except ValueError as e:
            raise QueryValidationError from e


validate_profile_icon_dto_query = (
    Query.has("platform")
    .as_(Platform)
    .also.can_have("version")
    .with_default(get_default_version, supplies_type=str)
    .also.can_have("locale")
    .with_default(get_default_locale, supplies_type=str)
    .also.has("id")
    .as_(int)
)


validate_many_profile_icon_dto_query = (
    Query.has("platform")
    .as_(Platform)
    .also.can_have("version")
    .with_default(get_default_version, supplies_type=str)
    .also.can_have("locale")
    .with_default(get_default_locale, supplies_type=str)
    .also.has("ids")
    .as_(Iterable)
)


def for_profile_icon_dto(profile_icon: ProfileIconDetailsDto) -> Tuple[str, str, str, int]:
    return profile_icon["platform"], profile_icon["version"], profile_icon["locale"], profile_icon["id"]


def for_profile_icon_dto_query(query: Query) -> Tuple[str, str, str, int]:
    return query["platform"].value, query["version"], query["locale"], query["id"]


def for_many_profile_icon_dto_query(query: Query) -> Generator[Tuple[str, str, str, int], None, None]:
    for id in query["ids"]:
        try:
            id = int(id)
            yield query["platform"].value, query["version"], query["locale"], id
        except ValueError as e:
            raise QueryValidationError from e


# Version


validate_version_list_dto_query = Query.has("platform").as_(Platform)


validate_many_version_list_dto_query = Query.has("platforms").as_(Iterable)


def for_version_list_dto(version_list: VersionListDto) -> str:
    return version_list["platform"]


def for_version_list_dto_query(query: Query) -> str:
    return query["platform"].value


def for_many_version_list_dto_query(query: Query) -> Generator[str, None, None]:
    for platform in query["platforms"]:
        try:
            platform = Platform(platform)
            yield platform.value
        except ValueError as e:
            raise QueryValidationError from e


##############
# Status API #
##############


validate_shard_status_dto_query = Query.has("platform").as_(Platform)


validate_many_shard_status_dto_query = Query.has("platforms").as_(Iterable)


def for_shard_status_dto(shard_status: ShardStatusDto) -> str:
    return shard_status["platform"]


def for_shard_status_dto_query(query: Query) -> str:
    return query["platform"].value


def for_many_shard_status_dto_query(query: Query) -> Generator[str, None, None]:
    for platform in query["platforms"]:
        try:
            platform = Platform(platform)
            yield platform.value
        except ValueError as e:
            raise QueryValidationError from e


###################
# Summoner API #
###################


validate_summoner_dto_query = (
    Query.has("platform").as_(Platform).also.has("id").as_(int).or_("accountId").as_(int).or_("name").as_(str)
)


validate_many_summoner_dto_query = (
    Query.has("platform")
    .as_(Platform)
    .also.has("ids")
    .as_(Iterable)
    .or_("accountIds")
    .as_(Iterable)
    .or_("names")
    .as_(Iterable)
)


def for_summoner_dto(summoner: SummonerDto, identifier: str = "id") -> Tuple[str, Union[int, str]]:
    return summoner["platform"], summoner[identifier]


def for_summoner_dto_query(query: Query) -> Tuple[str, Union[int, str]]:
    if "id" in query:
        identifier = "id"
    elif "accountId" in query:
        identifier = "accountId"
    else:
        identifier = "name"
    return query["platform"].value, query[identifier]


def for_many_summoner_dto_query(query: Query) -> Generator[Tuple[str, Union[int, str]], None, None]:
    if "ids" in query:
        identifiers, identifier_type = query["ids"], int
    elif "accountIds" in query:
        identifiers, identifier_type = query["accountIds"], int
    else:
        identifiers, identifier_type = query["names"], str
    for identifier in identifiers:
        try:
            identifier = identifier_type(identifier)
            yield query["platform"].value, identifier
        except ValueError as e:
            raise QueryValidationError from e


########
# Core #
########


##############
# League API #
##############


# League Entries

validate_league_entries_query = Query.has("platform").as_(Platform).also.has("summoner.id").as_(str)


validate_many_league_entries_query = Query.has("platform").as_(Platform).also.has("summoners.id").as_(Iterable)


def for_league_summoner_entries(entries: LeagueSummonerEntries) -> List[Tuple[str, str]]:
    return [(entries.platform.value, entries._LeagueSummonerEntries__summoner.id)]


def for_league_summoner_entries_query(query: Query) -> List[Tuple[str, str]]:
    return [(query["platform"].value, query["summoner.id"])]


def for_many_league_summoner_entries_query(query: Query) -> Generator[List[Tuple[str, str]], None, None]:
    for id in query["summoners.id"]:
        try:
            yield [(query["platform"].value, id)]
        except ValueError as e:
            raise QueryValidationError from e


# Leagues

validate_league_query = Query.has("platform").as_(Platform).also.has("id").as_(str)


validate_many_league_query = Query.has("platform").as_(Platform).also.has("ids").as_(Iterable)


def for_league(league: League) -> List[Tuple[str, str]]:
    return [(league.platform.value, league.id)]


def for_league_query(query: Query) -> List[Tuple[str, str]]:
    return [(query["platform"].value, query["id"])]


def for_many_league_query(query: Query) -> Generator[List[Tuple[str, str]], None, None]:
    for id in query["ids"]:
        try:
            yield [(query["platform"].value, id)]
        except ValueError as e:
            raise QueryValidationError from e


# Challenger

validate_challenger_league_query = Query.has("platform").as_(Platform)


def for_challenger_league(league: ChallengerLeague) -> List[Tuple[str]]:
    return [(league.platform.value)]


def for_challenger_league_query(query: Query) -> List[Tuple[str]]:
    return [(query["platform"].value)]


# Grandmaster

validate_grandmaster_league_query = Query.has("platform").as_(Platform)


def for_grandmaster_league(league: GrandmasterLeague) -> List[Tuple[str]]:
    return [(league.platform.value, league.queue.value)]


def for_grandmaster_league_query(query: Query) -> List[Tuple[str]]:
    return [(query["platform"].value)]


# Master

validate_master_league_query = Query.has("platform").as_(Platform)


def for_master_league(league: MasterLeague) -> List[Tuple[str]]:
    return [(league.platform.value)]


def for_master_league_query(query: Query) -> List[Tuple[str]]:
    return [(query["platform"].value)]


# League Entries List

validate_league_entries_list_query = (
    Query.has("tier").as_(Tier).also.has("division").as_(Division).also.has("platform").as_(Platform)
)


def for_league_entries_list(lel: LeagueSummonerEntries) -> List[Tuple[str, str, str]]:
    return [(lel.platform.value, lel.tier.value, lel.division.value)]


def for_league_entries_list_query(query: Query) -> List[Tuple[str, str, str]]:
    return [(query["platform"].value, query["tier"].value, query["division"].value)]


###################
# Static Data API #
###################


# Language

validate_languages_query = Query.has("platform").as_(Platform)


validate_many_languages_query = Query.has("platforms").as_(Iterable)


def for_languages(languages: Locales) -> List[str]:
    return [languages.platform.value]


def for_languages_query(query: Query) -> List[str]:
    return [query["platform"].value]


def for_many_languages_query(query: Query) -> Generator[List[str], None, None]:
    for platform in query["platforms"]:
        yield [platform.value]


validate_language_strings_query = Query.has("platform").as_(Platform)


validate_many_language_strings_query = Query.has("platforms").as_(Iterable)


def for_language_strings(languages: LanguageStrings) -> List[str]:
    return [languages.platform.value]


def for_language_strings_query(query: Query) -> List[str]:
    return [query["platform"].value]


def for_many_language_strings_query(query: Query) -> Generator[List[str], None, None]:
    for platform in query["platforms"]:
        yield [platform.value]


# Profile Icon

validate_profile_icons_query = (
    Query.has("platform")
    .as_(Platform)
    .also.can_have("version")
    .with_default(get_default_version, supplies_type=str)
    .also.can_have("locale")
    .with_default(get_default_locale, supplies_type=str)
)


validate_many_profile_icons_query = (
    Query.has("platforms")
    .as_(Iterable)
    .also.can_have("version")
    .with_default(get_default_version, supplies_type=str)
    .also.can_have("locale")
    .with_default(get_default_locale, supplies_type=str)
)


def for_profile_icons(profile_icon: ProfileIcons) -> List[Tuple[str, str, str]]:
    return [(Region(profile_icon.region).platform.value, profile_icon.version, profile_icon.locale)]


def for_profile_icons_query(query: Query) -> List[Tuple[str, str, str]]:
    return [(query["platform"].value, query["version"], query["locale"])]


def for_many_profile_icons_query(query: Query) -> Generator[List[Tuple[str, str, str]], None, None]:
    for platform in query["platforms"]:
        try:
            platform = Platform(platform)
            yield [(platform.value, query["version"], query["locale"])]
        except ValueError as e:
            raise QueryValidationError from e


validate_profile_icon_query = (
    Query.has("platform")
    .as_(Platform)
    .also.can_have("version")
    .with_default(get_default_version, supplies_type=str)
    .also.can_have("locale")
    .with_default(get_default_locale, supplies_type=str)
    .also.has("id")
    .as_(int)
)


validate_many_profile_icon_query = (
    Query.has("platform")
    .as_(Platform)
    .also.can_have("version")
    .with_default(get_default_version, supplies_type=str)
    .also.can_have("locale")
    .with_default(get_default_locale, supplies_type=str)
    .also.has("ids")
    .as_(Iterable)
)


def for_profile_icon(profile_icon: ProfileIcon) -> List[Tuple[str, str, str, int]]:
    return [(Region(profile_icon.region).platform.value, profile_icon.version, profile_icon.locale, profile_icon.id)]


def for_profile_icon_query(query: Query) -> List[Tuple[str, str, str, int]]:
    return [(query["platform"].value, query["version"], query["locale"], query["id"])]


def for_many_profile_icon_query(query: Query) -> Generator[List[Tuple[str, str, str, int]], None, None]:
    for id in query["ids"]:
        try:
            id = int(id)
            yield [(query["platform"].value, query["version"], query["locale"], id)]
        except ValueError as e:
            raise QueryValidationError from e


# Realm

validate_realms_query = Query.has("platform").as_(Platform)


validate_many_realms_query = Query.has("platforms").as_(Iterable)


def for_realms(realm: Realms) -> List[str]:
    return [(realm.platform.value)]


def for_realms_query(query: Query) -> List[str]:
    return [(query["platform"].value)]


def for_many_realms_query(query: Query) -> Generator[List[str], None, None]:
    for platform in query["platforms"]:
        yield [(platform.value)]


# Version

validate_versions_query = Query.has("platform").as_(Platform)


validate_many_versions_query = Query.has("platforms").as_(Iterable)


def for_versions(versions: Versions) -> List[str]:
    return [versions.platform.value]


def for_versions_query(query: Query) -> List[str]:
    return [query["platform"].value]


def for_many_versions_query(query: Query) -> Generator[List[str], None, None]:
    for platform in query["platforms"]:
        try:
            platform = Platform(platform)
            yield [platform.value]
        except ValueError as e:
            raise QueryValidationError from e


##############
# Status API #
##############

validate_shard_status_query = Query.has("platform").as_(Platform)


validate_many_shard_status_query = Query.has("platforms").as_(Iterable)


def for_shard_status(shard_status: ShardStatus) -> List[str]:
    return [shard_status.platform.value]


def for_shard_status_query(query: Query) -> List[str]:
    return [query["platform"].value]


def for_many_shard_status_query(query: Query) -> Generator[List[str], None, None]:
    for platform in query["platforms"]:
        try:
            platform = Platform(platform)
            yield [platform.value]
        except ValueError as e:
            raise QueryValidationError from e


################
# Summoner API #
################


validate_summoner_query = (
    Query.has("platform")
    .as_(Platform)
    .also.has("id")
    .as_(str)
    .or_("accountId")
    .as_(str)
    .or_("name")
    .as_(str)
    .or_("puuid")
    .as_(str)
)


validate_many_summoner_query = (
    Query.has("platform")
    .as_(Platform)
    .also.has("ids")
    .as_(Iterable)
    .or_("accountIds")
    .as_(Iterable)
    .or_("names")
    .as_(Iterable)
    .or_("puuids")
    .as_(Iterable)
)


def for_summoner(summoner: Summoner) -> List[Tuple]:
    keys = []
    try:
        keys.append((summoner.platform.value, "id", summoner._data[SummonerData].id))
    except AttributeError:
        pass
    try:
        keys.append((summoner.platform.value, "name", summoner._data[SummonerData].name))
    except AttributeError:
        pass
    try:
        keys.append((summoner.platform.value, "accountId", summoner._data[SummonerData].accountId))
    except AttributeError:
        pass
    try:
        keys.append((summoner.platform.value, "puuid", summoner._data[SummonerData].puuid))
    except AttributeError:
        pass
    return keys


def for_summoner_query(query: Query) -> List[Tuple]:
    keys = []
    if "id" in query:
        keys.append((query["platform"].value, "id", query["id"]))
    if "name" in query:
        keys.append((query["platform"].value, "name", query["name"]))
    if "accountId" in query:
        keys.append((query["platform"].value, "accountId", query["accountId"]))
    if "puuid" in query:
        keys.append((query["platform"].value, "puuid", query["puuid"]))
    return keys


def for_many_summoner_query(query: Query) -> Generator[List[Tuple], None, None]:
    grouped_identifiers = []
    identifier_types = []
    if "ids" in query:
        grouped_identifiers.append(query["ids"])
        identifier_types.append(str)
    elif "accountIds" in query:
        grouped_identifiers.append(query["accountIds"])
        identifier_types.append(str)
    elif "puuids" in query:
        grouped_identifiers.append(query["puuids"])
        identifier_types.append(str)
    elif "names" in query:
        grouped_identifiers.append(query["names"])
        identifier_types.append(str)
    for identifiers in zip(*grouped_identifiers):
        keys = []
        for identifier, identifier_type in zip(identifiers, identifier_types):
            try:
                identifier = identifier_type(identifier)
                keys.append((query["platform"].value, identifier))
            except ValueError as e:
                raise QueryValidationError from e
        yield keys
