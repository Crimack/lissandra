from typing import Any, Generator, Iterable, List, Mapping, MutableMapping, Set, Tuple, Union

from datapipelines import PipelineContext, Query, QueryValidationError

from ..data import Platform, Region
from ..dto.staticdata import LanguagesDto, LanguageStringsDto, VersionListDto

#############
# Utilities #
#############


def rgetattr(obj, key):
    """Recursive getattr for handling dots in keys."""
    for k in key.split("."):
        obj = getattr(obj, k)
    return obj


def hash_included_data(included_data: Set[str]) -> int:
    return hash(tuple(included_data))


def get_default_version(query: Mapping[str, Any], context: PipelineContext) -> str:
    try:
        pipeline = context[PipelineContext.Keys.PIPELINE]
        versions = pipeline.get(VersionListDto, {"platform": query["platform"]})
        return versions["versions"][0]
    except TypeError as error:
        raise KeyError("`version` must be provided in query") from error


def get_default_locale(query: Mapping[str, Any], context: PipelineContext) -> str:
    return query["platform"].default_locale


def region_to_platform_generator(regions: Iterable[Region]) -> Generator[Platform, None, None]:
    for region in regions:
        try:
            yield Region(region).platform
        except ValueError as e:
            raise QueryValidationError from e


def convert_region_to_platform(query: MutableMapping[str, Any]) -> None:
    if "region" in query and "platform" not in query:
        try:
            query["platform"] = Region(query["region"]).platform
        except ValueError as e:
            raise QueryValidationError from e

    if "regions" in query and "platforms" not in query:
        query["platforms"] = region_to_platform_generator(query["regions"])

    if "region" in query and not isinstance(query["region"], Region):
        query["region"] = Region(query["region"])
