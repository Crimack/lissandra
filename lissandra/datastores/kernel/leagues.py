from typing import Type, TypeVar, MutableMapping, Any, Iterable, Generator

from datapipelines import DataSource, PipelineContext, Query, NotFoundError, validate_query
from .common import KernelSource, APINotFoundError
from ...data import Platform, Tier, Division
from ...dto.league import (
    LeagueEntriesDto,
    LeagueDto,
    LeagueSummonerEntriesDto,
    ChallengerLeagueListDto,
    MasterLeagueListDto,
    GrandmasterLeagueListDto,
)
from ..util import convert_region_to_platform

T = TypeVar("T")


class LeaguesAPI(KernelSource):
    @DataSource.dispatch
    def get(self, type: Type[T], query: MutableMapping[str, Any], context: PipelineContext = None) -> T:
        pass

    @DataSource.dispatch
    def get_many(self, type: Type[T], query: MutableMapping[str, Any], context: PipelineContext = None) -> Iterable[T]:
        pass

    # League Entries

    _validate_get_league_entries_query = (
        Query.has("tier")
        .as_(Tier)
        .also.has("division")
        .as_(Division)
        .also.has("page")
        .as_(int)
        .also.has("platform")
        .as_(Platform)
    )

    @get.register(LeagueEntriesDto)
    @validate_query(_validate_get_league_entries_query, convert_region_to_platform)
    def get_league_entries_list(
        self, query: MutableMapping[str, Any], context: PipelineContext = None
    ) -> LeagueEntriesDto:
        parameters = {"platform": query["platform"].value, "page": query["page"]}
        endpoint = "tft/league/v1/entries/{tier}/{division}".format(
            tier=query["tier"].value, division=query["division"].value, page=query["page"]
        )
        try:
            data = self._get(endpoint=endpoint, parameters=parameters)
        except APINotFoundError:
            data = []
        region = query["platform"].region.value
        for entry in data:
            entry["region"] = region
        return LeagueEntriesDto(
            entries=data,
            page=query["page"],
            region=query["region"].value,
            tier=query["tier"].value,
            division=query["division"].value,
        )

    _validate_get_league_summoner_entries_query = Query.has("summoner.id").as_(str).also.has("platform").as_(Platform)

    # League Summoner Entries

    @get.register(LeagueSummonerEntriesDto)
    @validate_query(_validate_get_league_summoner_entries_query, convert_region_to_platform)
    def get_league_summoner_entries_list(
        self, query: MutableMapping[str, Any], context: PipelineContext = None
    ) -> LeagueSummonerEntriesDto:
        parameters = {"platform": query["platform"].value}
        endpoint = "tft/league/v1/entries/by-summoner/{id}".format(id=query["summoner.id"])
        try:
            data = self._get(endpoint=endpoint, parameters=parameters)
        except APINotFoundError as error:
            raise NotFoundError(str(error)) from error

        region = query["platform"].region.value
        for entry in data:
            entry["region"] = region
        return LeagueSummonerEntriesDto(entries=data, region=region, summonerId=query["summoner.id"])

    # League by ID

    _validate_get_league_query = Query.has("id").as_(str).also.has("platform").as_(Platform)

    @get.register(LeagueDto)
    @validate_query(_validate_get_league_query, convert_region_to_platform)
    def get_leagues_list(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> LeagueDto:
        parameters = {"platform": query["platform"].value}
        endpoint = "leagues/{leagueId}".format(leagueId=query["id"])
        try:
            data = self._get(endpoint=endpoint, parameters=parameters)
        except APINotFoundError as error:
            raise NotFoundError(str(error)) from error
        return LeagueDto(data)

    _validate_get_challenger_league_query = Query.has("platform").as_(Platform)

    # Challenger League

    @get.register(ChallengerLeagueListDto)
    @validate_query(_validate_get_challenger_league_query, convert_region_to_platform)
    def get_challenger_league_list(
        self, query: MutableMapping[str, Any], context: PipelineContext = None
    ) -> ChallengerLeagueListDto:
        parameters = {"platform": query["platform"].value}
        endpoint = "tft/league/v1/challenger"
        try:
            data = self._get(endpoint=endpoint, parameters=parameters)
        except APINotFoundError as error:
            raise NotFoundError(str(error)) from error

        data["region"] = query["platform"].region.value
        for entry in data["entries"]:
            entry["region"] = data["region"]
        return ChallengerLeagueListDto(data)

    # Grandmaster League

    _validate_get_grandmaster_league_query = Query.has("platform").as_(Platform)

    @get.register(GrandmasterLeagueListDto)
    @validate_query(_validate_get_grandmaster_league_query, convert_region_to_platform)
    def get_grandmaster_league_list(
        self, query: MutableMapping[str, Any], context: PipelineContext = None
    ) -> GrandmasterLeagueListDto:
        parameters = {"platform": query["platform"].value}
        endpoint = "tft/league/v1/grandmaster"
        try:
            data = self._get(endpoint=endpoint, parameters=parameters)
        except APINotFoundError as error:
            raise NotFoundError(str(error)) from error

        data["region"] = query["platform"].region.value
        for entry in data["entries"]:
            entry["region"] = data["region"]
        return GrandmasterLeagueListDto(data)

    # Master League

    _validate_get_master_league_query = Query.has("platform").as_(Platform)

    @get.register(MasterLeagueListDto)
    @validate_query(_validate_get_master_league_query, convert_region_to_platform)
    def get_master_league_list(
        self, query: MutableMapping[str, Any], context: PipelineContext = None
    ) -> MasterLeagueListDto:
        parameters = {"platform": query["platform"].value}
        endpoint = "tft/league/v1/master"
        try:
            data = self._get(endpoint=endpoint, parameters=parameters)
        except APINotFoundError as error:
            raise NotFoundError(str(error)) from error

        data["region"] = query["platform"].region.value
        for entry in data["entries"]:
            entry["region"] = data["region"]
        return MasterLeagueListDto(data)
