from typing import Type, Mapping, Any, Iterable, TypeVar, Tuple, Callable, Generator
import datetime

from datapipelines import DataSource, DataSink, PipelineContext, validate_query, NotFoundError
from merakicommons.cache import Cache as CommonsCache

from . import uniquekeys, util
from ..core.staticdata.realm import RealmData, Realms
from ..core.staticdata.profileicon import ProfileIconData, ProfileIconListData, ProfileIcon, ProfileIcons
from ..core.staticdata.language import LanguagesData, Locales
from ..core.staticdata.languagestrings import LanguageStringsData, LanguageStrings
from ..core.staticdata.version import VersionListData, Versions
from ..core.league import (
    LeagueEntriesData,
    LeagueEntries,
    LeagueSummonerEntriesData,
    LeagueSummonerEntries,
    ChallengerLeague,
    MasterLeague,
    GrandmasterLeague,
)
from ..core.summoner import SummonerData, Summoner
from ..core.status import ShardStatusData, ShardStatus

T = TypeVar("T")


default_expirations = {
    Realms: datetime.timedelta(hours=6),
    Versions: datetime.timedelta(hours=6),
    ProfileIcon: datetime.timedelta(days=20),
    Locales: datetime.timedelta(days=20),
    LanguageStrings: datetime.timedelta(days=20),
    ProfileIcons: datetime.timedelta(days=20),
    Summoner: datetime.timedelta(days=1),
}


class Cache(DataSource, DataSink):
    def __init__(self, expirations: Mapping[type, float] = None) -> None:
        self._cache = CommonsCache()
        self._expirations = dict(expirations) if expirations is not None else default_expirations
        for key, value in list(self._expirations.items()):
            if isinstance(key, str):
                new_key = globals()[key]
                self._expirations[new_key] = self._expirations.pop(key)
                key = new_key
            if value != -1 and isinstance(value, datetime.timedelta):
                self._expirations[key] = value.seconds + 24 * 60 * 60 * value.days

    @DataSource.dispatch
    def get(self, type: Type[T], query: Mapping[str, Any], context: PipelineContext = None) -> T:
        pass

    @DataSource.dispatch
    def get_many(self, type: Type[T], query: Mapping[str, Any], context: PipelineContext = None) -> Iterable[T]:
        pass

    @DataSink.dispatch
    def put(self, type: Type[T], item: T, context: PipelineContext = None) -> None:
        pass

    @DataSink.dispatch
    def put_many(self, type: Type[T], items: Iterable[T], context: PipelineContext = None) -> None:
        pass

    def _get(
        self,
        type: Type[T],
        query: Mapping[str, Any],
        key_function: Callable[[Mapping[str, Any]], Any],
        context: PipelineContext = None,
    ) -> T:
        keys = key_function(query)
        for key in keys:
            try:
                return self._cache.get(type, key)
            except KeyError:
                pass
        else:
            raise NotFoundError

    def _get_many(
        self,
        type: Type[T],
        query: Mapping[str, Any],
        key_generator: Callable[[Mapping[str, Any]], Any],
        context: PipelineContext = None,
    ) -> Generator[T, None, None]:
        for keys in key_generator(query):
            for key in keys:
                try:
                    yield self._cache.get(type, key)
                except KeyError:
                    pass
            else:
                raise NotFoundError

    @staticmethod
    def _put_many_generator(
        items: Iterable[T], key_function: Callable[[T], Any]
    ) -> Generator[Tuple[Any, T], None, None]:
        for item in items:
            for key in key_function(item):
                yield key, item

    def _put(self, type: Type[T], item: T, key_function: Callable[[T], Any], context: PipelineContext = None) -> None:
        try:
            expire_seconds = self._expirations[type]
        except KeyError:
            expire_seconds = -1

        if expire_seconds != 0:
            keys = key_function(item)
            for key in keys:
                self._cache.put(type, key, item, expire_seconds)

    def _put_many(
        self, type: Type[T], items: Iterable[T], key_function: Callable[[T], Any], context: PipelineContext = None
    ) -> None:
        expire_seconds = self._expirations.get(type, default_expirations[type])
        for key, item in Cache._put_many_generator(items, key_function):
            self._cache.put(type, key, item, expire_seconds)

    def clear(self, type: Type[T] = None):
        if type is None:
            for key in self._cache._data:
                self._cache._data[key].clear()
        else:
            self._cache._data[type].clear()

    def expire(self, type: Type[T] = None):
        self._cache.expire(type)

    ###################
    # Static Data API #
    ###################

    # Language

    @get.register(Locales)
    @validate_query(uniquekeys.validate_languages_query, util.convert_region_to_platform)
    def get_languages(self, query: Mapping[str, Any], context: PipelineContext = None) -> Locales:
        return self._get(Locales, query, uniquekeys.for_languages_query, context)

    @get_many.register(Locales)
    @validate_query(uniquekeys.validate_many_languages_query, util.convert_region_to_platform)
    def get_many_languages(
        self, query: Mapping[str, Any], context: PipelineContext = None
    ) -> Generator[Locales, None, None]:
        return self._get_many(Locales, query, uniquekeys.for_many_languages_query, context)

    @put.register(Locales)
    def put_languages(self, item: Locales, context: PipelineContext = None) -> None:
        self._put(Locales, item, uniquekeys.for_languages, context=context)

    @put_many.register(Locales)
    def put_many_languages(self, items: Iterable[Locales], context: PipelineContext = None) -> None:
        self._put_many(Locales, items, uniquekeys.for_languages, context=context)

    # Language strings

    @get.register(LanguageStrings)
    @validate_query(uniquekeys.validate_language_strings_query, util.convert_region_to_platform)
    def get_language_strings(self, query: Mapping[str, Any], context: PipelineContext = None) -> LanguageStrings:
        return self._get(LanguageStrings, query, uniquekeys.for_language_strings_query, context)

    @get_many.register(LanguageStrings)
    @validate_query(uniquekeys.validate_many_language_strings_query, util.convert_region_to_platform)
    def get_many_language_strings(
        self, query: Mapping[str, Any], context: PipelineContext = None
    ) -> Generator[LanguageStrings, None, None]:
        return self._get_many(LanguageStrings, query, uniquekeys.for_many_language_strings_query, context)

    @put.register(LanguageStrings)
    def put_language_strings(self, item: LanguageStrings, context: PipelineContext = None) -> None:
        self._put(LanguageStrings, item, uniquekeys.for_language_strings, context=context)

    @put_many.register(LanguageStrings)
    def put_many_language_strings(self, items: Iterable[LanguageStrings], context: PipelineContext = None) -> None:
        self._put_many(LanguageStrings, items, uniquekeys.for_language_strings, context=context)

    @get.register(LanguageStringsData)
    @validate_query(uniquekeys.validate_language_strings_query, util.convert_region_to_platform)
    def get_language_strings_data(
        self, query: Mapping[str, Any], context: PipelineContext = None
    ) -> LanguageStringsData:
        result = self.get_language_strings(query=query, context=context)
        if result._data[LanguageStringsData] is not None and result._Ghost__is_loaded(LanguageStringsData):
            return result._data[LanguageStringsData]
        else:
            raise NotFoundError

    # Profile Icons

    @get.register(ProfileIcons)
    @validate_query(uniquekeys.validate_profile_icons_query, util.convert_region_to_platform)
    def get_profile_icons(self, query: Mapping[str, Any], context: PipelineContext = None) -> ProfileIcons:
        return self._get(ProfileIcons, query, uniquekeys.for_profile_icons_query, context)

    @get_many.register(ProfileIcons)
    @validate_query(uniquekeys.validate_many_profile_icons_query, util.convert_region_to_platform)
    def get_many_profile_icons(
        self, query: Mapping[str, Any], context: PipelineContext = None
    ) -> Generator[ProfileIcons, None, None]:
        return self._get_many(ProfileIcons, query, uniquekeys.for_many_profile_icons_query, context)

    @put.register(ProfileIcons)
    def put_profile_icons(self, item: ProfileIcons, context: PipelineContext = None) -> None:
        self._put(ProfileIcons, item, uniquekeys.for_profile_icons, context=context)
        for profile_icon in item:
            self._put(ProfileIcon, profile_icon, uniquekeys.for_profile_icon, context=context)

    @put_many.register(ProfileIcons)
    def put_many_profile_icons(self, items: Iterable[ProfileIcons], context: PipelineContext = None) -> None:
        self._put_many(ProfileIcons, items, uniquekeys.for_profile_icons, context=context)

    # Realm

    @get.register(Realms)
    @validate_query(uniquekeys.validate_realms_query, util.convert_region_to_platform)
    def get_realms(self, query: Mapping[str, Any], context: PipelineContext = None) -> Realms:
        return self._get(Realms, query, uniquekeys.for_realms_query, context)

    @get_many.register(Realms)
    @validate_query(uniquekeys.validate_many_realms_query, util.convert_region_to_platform)
    def get_many_realms(
        self, query: Mapping[str, Any], context: PipelineContext = None
    ) -> Generator[Realms, None, None]:
        return self._get_many(Realms, query, uniquekeys.for_many_realms_query, context)

    @put.register(Realms)
    def put_realms(self, item: Realms, context: PipelineContext = None) -> None:
        self._put(Realms, item, uniquekeys.for_realms, context=context)

    @put_many.register(Realms)
    def put_many_realms(self, items: Iterable[Realms], context: PipelineContext = None) -> None:
        self._put_many(Realms, items, uniquekeys.for_realms, context=context)

    @get.register(RealmData)
    @validate_query(uniquekeys.validate_realms_query, util.convert_region_to_platform)
    def get_realms_data(self, query: Mapping[str, Any], context: PipelineContext = None) -> RealmData:
        result = self.get_realms(query=query, context=context)
        if result._data[RealmData] is not None and result._Ghost__is_loaded(RealmData):
            return result._data[RealmData]
        else:
            raise NotFoundError

    # Versions

    @get.register(Versions)
    @validate_query(uniquekeys.validate_versions_query, util.convert_region_to_platform)
    def get_versions(self, query: Mapping[str, Any], context: PipelineContext = None) -> Versions:
        return self._get(Versions, query, uniquekeys.for_versions_query, context=context)

    @get_many.register(Versions)
    @validate_query(uniquekeys.validate_many_versions_query, util.convert_region_to_platform)
    def get_many_versions(
        self, query: Mapping[str, Any], context: PipelineContext = None
    ) -> Generator[Versions, None, None]:
        return self._get_many(Versions, query, uniquekeys.for_many_versions_query, context=context)

    @put.register(Versions)
    def put_versions(self, item: Versions, context: PipelineContext = None) -> None:
        self._put(Versions, item, uniquekeys.for_versions, context=context)

    @put_many.register(Versions)
    def put_many_versions(self, items: Iterable[Versions], context: PipelineContext = None) -> None:
        self._put_many(Versions, items, uniquekeys.for_versions, context=context)

    ##############
    # Status API #
    ##############

    @get.register(ShardStatus)
    @validate_query(uniquekeys.validate_shard_status_query, util.convert_region_to_platform)
    def get_shard_status(self, query: Mapping[str, Any], context: PipelineContext = None) -> ShardStatus:
        return self._get(ShardStatus, query, uniquekeys.for_shard_status_query, context)

    @get_many.register(ShardStatus)
    @validate_query(uniquekeys.validate_many_shard_status_query, util.convert_region_to_platform)
    def get_many_shard_status(
        self, query: Mapping[str, Any], context: PipelineContext = None
    ) -> Generator[ShardStatus, None, None]:
        return self._get_many(ShardStatus, query, uniquekeys.for_many_shard_status_query, context)

    @put.register(ShardStatus)
    def put_shard_status(self, item: ShardStatus, context: PipelineContext = None) -> None:
        self._put(ShardStatus, item, uniquekeys.for_shard_status, context=context)

    @put_many.register(ShardStatus)
    def put_many_shard_status(self, items: Iterable[ShardStatus], context: PipelineContext = None) -> None:
        self._put_many(ShardStatus, items, uniquekeys.for_shard_status, context=context)

    @get.register(ShardStatusData)
    @validate_query(uniquekeys.validate_shard_status_query, util.convert_region_to_platform)
    def get_shard_status_data(self, query: Mapping[str, Any], context: PipelineContext = None) -> ShardStatusData:
        result = self.get_shard_status(query=query, context=context)
        if result._data[ShardStatusData] is not None and result._Ghost__is_loaded(ShardStatusData):
            return result._data[ShardStatusData]
        else:
            raise NotFoundError

    ###################
    # Summoner API    #
    ###################

    @get.register(Summoner)
    @validate_query(uniquekeys.validate_summoner_query, util.convert_region_to_platform)
    def get_summoner(self, query: Mapping[str, Any], context: PipelineContext = None) -> Summoner:
        return self._get(Summoner, query, uniquekeys.for_summoner_query, context)

    @get_many.register(Summoner)
    @validate_query(uniquekeys.validate_many_summoner_query, util.convert_region_to_platform)
    def get_many_summoner(
        self, query: Mapping[str, Any], context: PipelineContext = None
    ) -> Generator[Summoner, None, None]:
        return self._get_many(Summoner, query, uniquekeys.for_many_summoner_query, context)

    @put.register(Summoner)
    def put_summoner(self, item: Summoner, context: PipelineContext = None) -> None:
        self._put(Summoner, item, uniquekeys.for_summoner, context=context)

    @put_many.register(Summoner)
    def put_many_summoner(self, items: Iterable[Summoner], context: PipelineContext = None) -> None:
        self._put_many(Summoner, items, uniquekeys.for_summoner, context=context)

    @get.register(SummonerData)
    @validate_query(uniquekeys.validate_summoner_query, util.convert_region_to_platform)
    def get_summoner_data(self, query: Mapping[str, Any], context: PipelineContext = None) -> SummonerData:
        result = self.get_summoner(query=query, context=context)
        if result._data[SummonerData] is not None and result._Ghost__is_loaded(SummonerData):
            return result._data[SummonerData]
        else:
            raise NotFoundError

    ##############
    # League API #
    ##############

    # Challenger

    @get.register(ChallengerLeague)
    @validate_query(uniquekeys.validate_challenger_league_query, uniquekeys.convert_region_to_platform)
    def get_challenger_league_summoner(
        self, query: Mapping[str, Any], context: PipelineContext = None
    ) -> ChallengerLeague:
        return self._get(ChallengerLeague, query, uniquekeys.for_challenger_league_query, context)

    @put.register(ChallengerLeague)
    def put_challenger_league_summoner(self, item: ChallengerLeague, context: PipelineContext = None) -> None:
        self._put(ChallengerLeague, item, uniquekeys.for_challenger_league, context=context)

    # Grandmaster

    @get.register(GrandmasterLeague)
    @validate_query(uniquekeys.validate_grandmaster_league_query, uniquekeys.convert_region_to_platform)
    def get_grandmaster_league_summoner(
        self, query: Mapping[str, Any], context: PipelineContext = None
    ) -> GrandmasterLeague:
        return self._get(GrandmasterLeague, query, uniquekeys.for_grandmaster_league_query, context)

    @put.register(GrandmasterLeague)
    def put_grandmaster_league_summoner(self, item: GrandmasterLeague, context: PipelineContext = None) -> None:
        self._put(GrandmasterLeague, item, uniquekeys.for_grandmaster_league, context=context)

    # Master

    @get.register(MasterLeague)
    @validate_query(uniquekeys.validate_master_league_query, uniquekeys.convert_region_to_platform)
    def get_master_league_summoner(self, query: Mapping[str, Any], context: PipelineContext = None) -> MasterLeague:
        return self._get(MasterLeague, query, uniquekeys.for_master_league_query, context)

    @put.register(MasterLeague)
    def put_master_league_summoner(self, item: MasterLeague, context: PipelineContext = None) -> None:
        self._put(MasterLeague, item, uniquekeys.for_master_league, context=context)

    # League Summoner

    @get.register(LeagueSummonerEntries)
    @validate_query(uniquekeys.validate_league_entries_query, util.convert_region_to_platform)
    def get_league_summoner_entries(self, query: Mapping[str, Any], context: PipelineContext = None) -> Summoner:
        return self._get(LeagueSummonerEntries, query, uniquekeys.for_league_summoner_entries_query, context)

    @get_many.register(LeagueSummonerEntries)
    @validate_query(uniquekeys.validate_many_league_entries_query, util.convert_region_to_platform)
    def get_many_league_summoner_entries(
        self, query: Mapping[str, Any], context: PipelineContext = None
    ) -> Generator[LeagueSummonerEntries, None, None]:
        return self._get_many(LeagueSummonerEntries, query, uniquekeys.for_many_league_summoner_entries_query, context)

    @put.register(LeagueSummonerEntries)
    def put_league_summoner_entries(self, item: LeagueSummonerEntries, context: PipelineContext = None) -> None:
        self._put(LeagueSummonerEntries, item, uniquekeys.for_league_summoner_entries, context=context)

    @put_many.register(LeagueSummonerEntries)
    def put_many_league_summoner_entries(self, items: Iterable[Summoner], context: PipelineContext = None) -> None:
        self._put_many(LeagueSummonerEntries, items, uniquekeys.for_league_summoner_entries, context=context)

    # @get.register(LeagueSummonerEntriesData)
    # @validate_query(uniquekeys.validate_league_entries_query, util.convert_region_to_platform)
    # def get_league_summoner_data(
    #     self, query: Mapping[str, Any], context: PipelineContext = None
    # ) -> LeagueSummonerEntriesData:
    #     print(query)
    #     result = self.get_league_summoner_entries(query=query, context=context)
    #     if result._data[LeagueSummonerEntriesData] is not None and result._Ghost__is_loaded(LeagueSummonerEntriesData):
    #         return result._data[LeagueSummonerEntriesData]
    #     else:
    #         raise NotFoundError
