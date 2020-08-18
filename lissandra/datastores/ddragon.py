import copy
from typing import Type, TypeVar, MutableMapping, Any, Iterable
from collections import defaultdict

from datapipelines import DataSource, PipelineContext, Query, NotFoundError, validate_query

from ..data import Platform
from ..dto.staticdata.version import VersionListDto
from ..dto.staticdata.profileicon import ProfileIconDataDto
from ..dto.staticdata.language import LanguagesDto, LanguageStringsDto
from ..dto.staticdata.realm import RealmDto
from .common import HTTPClient, HTTPError
from .riotapi.common import _get_latest_version
from .util import hash_included_data, convert_region_to_platform

try:
    import ujson as json
except ImportError:
    import json

T = TypeVar("T")


class DDragon(DataSource):
    def __init__(self, http_client: HTTPClient = None) -> None:
        if http_client is None:
            self._client = HTTPClient()
        else:
            self._client = http_client

        self._cache = {}

    @DataSource.dispatch
    def get(self, type: Type[T], query: MutableMapping[str, Any], context: PipelineContext = None) -> T:
        pass

    @DataSource.dispatch
    def get_many(self, type: Type[T], query: MutableMapping[str, Any], context: PipelineContext = None) -> Iterable[T]:
        pass

    def calculate_hash(self, query):
        hash = list(value for _, value in sorted(query.items()))
        for i, value in enumerate(hash):
            if isinstance(value, set):
                hash[i] = hash_included_data(value)
        return tuple(hash)

    ############
    # Versions #
    ############

    _validate_get_versions_query = Query.has("platform").as_(Platform)

    @get.register(VersionListDto)
    @validate_query(_validate_get_versions_query, convert_region_to_platform)
    def get_versions(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> VersionListDto:
        url = "https://ddragon.leagueoflegends.com/api/versions.json"
        try:
            body = json.loads(self._client.get(url)[0])
        except HTTPError as e:
            raise NotFoundError(str(e)) from e

        return VersionListDto({"region": query["platform"].region.value, "versions": body})

    ##########
    # Realms #
    ##########

    _validate_get_realms_query = Query.has("platform").as_(Platform)

    @get.register(RealmDto)
    @validate_query(_validate_get_realms_query, convert_region_to_platform)
    def get_realms(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> RealmDto:
        region = query["platform"].region
        url = "https://ddragon.leagueoflegends.com/realms/{region}.json".format(region=region.value.lower())
        try:
            body = json.loads(self._client.get(url)[0])

        except HTTPError as e:
            raise NotFoundError(str(e)) from e

        body["region"] = query["platform"].region.value
        return RealmDto(body)

    #############
    # Languages #
    #############

    _validate_get_languages_query = Query.has("platform").as_(Platform)

    @get.register(LanguagesDto)
    @validate_query(_validate_get_languages_query, convert_region_to_platform)
    def get_languages(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> LanguagesDto:
        url = "https://ddragon.leagueoflegends.com/cdn/languages.json"
        try:
            body = json.loads(self._client.get(url)[0])
        except HTTPError as e:
            raise NotFoundError(str(e)) from e

        data = {"region": query["platform"].region.value, "languages": body}
        return LanguagesDto(data)

    ####################
    # Language Strings #
    ####################

    _validate_get_language_strings_query = (
        Query.has("platform")
        .as_(Platform)
        .also.can_have("version")
        .with_default(_get_latest_version, supplies_type=str)
        .also.can_have("locale")
        .as_(str)
    )

    @get.register(LanguageStringsDto)
    @validate_query(_validate_get_language_strings_query, convert_region_to_platform)
    def get_language_strings(
        self, query: MutableMapping[str, Any], context: PipelineContext = None
    ) -> LanguageStringsDto:
        locale = query["locale"] if "locale" in query else query["platform"].default_locale

        url = "https://ddragon.leagueoflegends.com/cdn/{version}/data/{locale}/language.json".format(
            version=query["version"], locale=locale
        )
        try:
            body = json.loads(self._client.get(url)[0])
        except HTTPError as e:
            raise NotFoundError(str(e)) from e

        body["region"] = query["platform"].region.value
        body["locale"] = locale
        return LanguageStringsDto(body)

    #################
    # Profile Icons #
    #################

    _validate_get_profile_icon_query = (
        Query.has("platform")
        .as_(Platform)
        .also.can_have("version")
        .with_default(_get_latest_version, supplies_type=str)
        .also.can_have("locale")
        .as_(str)
    )

    @get.register(ProfileIconDataDto)
    @validate_query(_validate_get_profile_icon_query, convert_region_to_platform)
    def get_profile_icon(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> ProfileIconDataDto:
        locale = query["locale"] if "locale" in query else query["platform"].default_locale

        url = "https://ddragon.leagueoflegends.com/cdn/{version}/data/{locale}/profileicon.json".format(
            version=query["version"], locale=locale
        )
        try:
            body = json.loads(self._client.get(url)[0])
        except HTTPError as e:
            raise NotFoundError(str(e)) from e

        body["region"] = query["platform"].region.value
        body["locale"] = locale
        body["version"] = query["version"]
        for pi in body["data"].values():
            pi["region"] = body["region"]
            pi["version"] = body["version"]
            pi["locale"] = locale
        return ProfileIconDataDto(body)
