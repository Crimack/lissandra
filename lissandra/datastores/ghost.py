from typing import Type, TypeVar, MutableMapping, Any, Iterable, Union
import arrow
import copy

from datapipelines import DataSource, PipelineContext, Query, validate_query

from ..data import Platform, Queue, Tier, Division
from ..core import (
    Realms,
    ProfileIcon,
    LanguageStrings,
    ShardStatus,
    ChallengerLeague,
    GrandmasterLeague,
    MasterLeague,
    League,
    ProfileIcons,
    Locales,
    Versions,
    LeagueEntries,
    VerificationString,
    Summoner,
)
from ..core.league import (
    LeagueEntry,
    LeagueEntriesData,
    LeagueEntryData,
    LeagueSummonerEntries,
    LeagueSummonerEntriesData,
)
from ..core.staticdata.profileicon import ProfileIconListData
from ..core.staticdata.language import LanguagesData
from ..core.staticdata.version import VersionListData
from .riotapi.common import _get_latest_version, _get_default_locale
from .uniquekeys import convert_region_to_platform

T = TypeVar("T")


class UnloadedGhostStore(DataSource):
    def __init__(self):
        super().__init__()

    @DataSource.dispatch
    def get(self, type: Type[T], query: MutableMapping[str, Any], context: PipelineContext = None) -> T:
        pass

    @DataSource.dispatch
    def get_many(self, type: Type[T], query: MutableMapping[str, Any], context: PipelineContext = None) -> Iterable[T]:
        pass

    _validate_get_versions_query = Query.has("platform").as_(Platform)

    _validate_get_realms_query = Query.has("platform").as_(Platform)

    _validate_get_languages_query = Query.has("platform").as_(Platform)

    _validate_get_language_strings_query = (
        Query.has("platform")
        .as_(Platform)
        .also.can_have("version")
        .as_(str)
        .also.can_have("locale")
        .with_default(_get_default_locale, supplies_type=str)
    )

    _validate_get_profile_icon_query = (
        Query.has("platform")
        .as_(Platform)
        .also.has("id")
        .as_(int)
        .also.can_have("version")
        .as_(str)
        .also.can_have("locale")
        .with_default(_get_default_locale, supplies_type=str)
    )

    _validate_get_profile_icons_query = (
        Query.has("platform")
        .as_(Platform)
        .also.can_have("version")
        .as_(str)
        .also.can_have("locale")
        .with_default(_get_default_locale, supplies_type=str)
    )

    _validate_get_paginated_queues_query = Query.has("platform").as_(Platform)

    _validate_get_league_entries_query = (
        Query.has("tier").as_(Tier).also.has("division").as_(Division).also.has("platform").as_(Platform)
    )

    _validate_get_league_summoner_entries_query = Query.has("summoner.id").as_(str).also.has("platform").as_(Platform)

    _validate_get_league_query = Query.has("id").as_(str).also.has("platform").as_(Platform)

    _validate_get_challenger_league_query = Query.has("platform").as_(Platform)

    _validate_get_grandmaster_league_query = Query.has("platform").as_(Platform)

    _validate_get_master_league_query = Query.has("platform").as_(Platform)

    _validate_get_league_entries_list_query = (
        Query.has("tier").as_(Tier).also.has("division").as_(Division).also.has("platform").as_(Platform)
    )

    _validate_get_shard_status_query = Query.has("platform").as_(Platform)

    _validate_get_summoner_query = (
        Query.has("id")
        .as_(str)
        .or_("accountId")
        .as_(str)
        .or_("puuid")
        .as_(str)
        .or_("name")
        .as_(str)
        .also.has("platform")
        .as_(Platform)
    )

    _validate_get_verification_string_query = Query.has("platform").as_(Platform).also.has("summoner.id").as_(str)

    @get.register(Realms)
    @validate_query(_validate_get_realms_query, convert_region_to_platform)
    def get_realms(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> Realms:
        query["region"] = query.pop("platform").region
        return Realms._construct_normally(**query)

    @get.register(ProfileIcon)
    @validate_query(_validate_get_profile_icon_query, convert_region_to_platform)
    def get_profile_icon(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> ProfileIcon:
        query["region"] = query.pop("platform").region
        return ProfileIcon._construct_normally(**query)

    @get.register(LanguageStrings)
    @validate_query(_validate_get_language_strings_query, convert_region_to_platform)
    def get_language_strings(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> LanguageStrings:
        query["region"] = query.pop("platform").region
        return LanguageStrings._construct_normally(**query)

    @get.register(Summoner)
    @validate_query(_validate_get_summoner_query, convert_region_to_platform)
    def get_summoner(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> Summoner:
        kwargs = copy.deepcopy(query)
        kwargs["region"] = kwargs.pop("platform").region
        if "accountId" in kwargs:
            kwargs["account_id"] = kwargs.pop("accountId")
        return Summoner._construct_normally(**kwargs)

    @get.register(ShardStatus)
    @validate_query(_validate_get_shard_status_query, convert_region_to_platform)
    def get_shard_status(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> ShardStatus:
        query["region"] = query.pop("platform").region
        return ShardStatus._construct_normally(**query)

    @get.register(ChallengerLeague)
    @validate_query(_validate_get_challenger_league_query, convert_region_to_platform)
    def get_challenger_league(
        self, query: MutableMapping[str, Any], context: PipelineContext = None
    ) -> ChallengerLeague:
        UnloadedGhostStore._validate_get_challenger_league_query(query)
        query["region"] = query.pop("platform").region
        return ChallengerLeague._construct_normally(**query)

    @get.register(GrandmasterLeague)
    @validate_query(_validate_get_grandmaster_league_query, convert_region_to_platform)
    def get_grandmaster_league(
        self, query: MutableMapping[str, Any], context: PipelineContext = None
    ) -> GrandmasterLeague:
        UnloadedGhostStore._validate_get_grandmaster_league_query(query)
        query["region"] = query.pop("platform").region
        return GrandmasterLeague._construct_normally(**query)

    @get.register(MasterLeague)
    @validate_query(_validate_get_master_league_query, convert_region_to_platform)
    def get_master_league(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> MasterLeague:
        query["region"] = query.pop("platform").region
        return MasterLeague._construct_normally(**query)

    @get.register(League)
    @validate_query(_validate_get_league_query, convert_region_to_platform)
    def get_league(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> League:
        query["region"] = query.pop("platform").region
        query["id"] = query.pop("id")
        return League._construct_normally(**query)

    @get.register(LeagueEntries)
    @validate_query(_validate_get_league_entries_list_query, convert_region_to_platform)
    def get_league_entries_list(
        self, query: MutableMapping[str, Any], context: PipelineContext = None
    ) -> LeagueEntries:
        def generate_entries(original_query):
            page = 1
            while True:
                new_query = copy.deepcopy(original_query)
                new_query["page"] = page
                data = context[context.Keys.PIPELINE].get(LeagueEntriesData, query=new_query)
                n_new_results = len(data)
                for entrydata in data:
                    entry = LeagueEntry.from_data(data=entrydata, loaded_groups={LeagueEntryData})
                    yield entry
                if page == 1:
                    results_per_page = n_new_results
                if n_new_results != results_per_page:
                    break
                page += 1

        original_query = copy.deepcopy(query)
        return LeagueEntries.from_generator(
            generator=generate_entries(original_query),
            region=query["region"],
            tier=query["tier"],
            division=query["division"],
        )

    @get.register(LeagueSummonerEntries)
    @validate_query(_validate_get_league_summoner_entries_query, convert_region_to_platform)
    def get_league_summoner_entries(
        self, query: MutableMapping[str, Any], context: PipelineContext = None
    ) -> LeagueEntries:
        def league_summoner_entries_generator(query):
            data = context[context.Keys.PIPELINE].get(LeagueSummonerEntriesData, query)
            for entry in data:
                entry = LeagueEntry.from_data(entry)
                yield entry

        kwargs = {"summoner": Summoner(id=query["summoner.id"], region=query["region"])}
        return LeagueSummonerEntries.from_generator(generator=league_summoner_entries_generator(query), **kwargs)

    @get.register(VerificationString)
    @validate_query(_validate_get_verification_string_query, convert_region_to_platform)
    def get_verification_string(
        self, query: MutableMapping[str, Any], context: PipelineContext = None
    ) -> VerificationString:
        query["region"] = query.pop("platform").region
        query["summoner"] = Summoner(id=query.pop("summoner.id"), region=query["region"])
        return VerificationString._construct_normally(**query)

    @get.register(ProfileIcons)
    @validate_query(_validate_get_profile_icons_query, convert_region_to_platform)
    def get_profile_icons(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> ProfileIcons:
        def profile_icons_generator(query):
            data = context[context.Keys.PIPELINE].get(ProfileIconListData, query)
            for profile_icon_data in data:
                profile_icon = ProfileIcon.from_data(profile_icon_data)
                yield profile_icon

        kwargs = {"region": query["region"], "version": query["version"], "locale": query["locale"]}
        return ProfileIcons.from_generator(generator=profile_icons_generator(query), **kwargs)

    @get.register(Locales)
    @validate_query(_validate_get_languages_query, convert_region_to_platform)
    def get_locales(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> Locales:
        def locales_generator(query):
            data = context[context.Keys.PIPELINE].get(LanguagesData, query)
            for locale in data:
                yield locale

        kwargs = {"region": query["region"]}
        return Locales.from_generator(generator=locales_generator(query), **kwargs)

    @get.register(Versions)
    @validate_query(_validate_get_versions_query, convert_region_to_platform)
    def get_versions(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> Versions:
        def versions_generator(query):
            data = context[context.Keys.PIPELINE].get(VersionListData, query)
            for version in data:
                yield version

        kwargs = {"region": query["region"]}
        return Versions.from_generator(generator=versions_generator(query), **kwargs)
