from typing import Type, TypeVar
from copy import deepcopy

from datapipelines import DataTransformer, PipelineContext

from ..core.staticdata.version import VersionListData, Versions
from ..core.staticdata.realm import RealmData, Realms
from ..core.staticdata.language import LanguagesData, Locales
from ..core.staticdata.languagestrings import LanguageStringsData, LanguageStrings
from ..core.staticdata.profileicon import ProfileIconData, ProfileIconListData, ProfileIcon, ProfileIcons

from ..dto.staticdata import VersionListDto
from ..dto.staticdata.realm import RealmDto
from ..dto.staticdata.language import LanguagesDto, LanguageStringsDto
from ..dto.staticdata.profileicon import ProfileIconDetailsDto, ProfileIconDataDto

T = TypeVar("T")
F = TypeVar("F")


class StaticDataTransformer(DataTransformer):
    @DataTransformer.dispatch
    def transform(self, target_type: Type[T], value: F, context: PipelineContext = None) -> T:
        pass

    ###############
    # Dto to Data #
    ###############

    # Version

    @transform.register(VersionListDto, VersionListData)
    def version_list_dto_to_data(self, value: VersionListDto, context: PipelineContext = None) -> VersionListData:
        data = VersionListData(deepcopy(value["versions"]), region=value["region"])
        return data

    # Realm

    @transform.register(RealmDto, RealmData)
    def realm_dto_to_data(self, value: RealmDto, context: PipelineContext = None) -> RealmData:
        return RealmData(**value)

    # Languages

    @transform.register(LanguagesDto, LanguagesData)
    def languages_dto_to_data(self, value: LanguagesDto, context: PipelineContext = None) -> LanguagesData:
        data = deepcopy(value)
        return LanguagesData(data["languages"], region=value["region"])

    # Language Strings

    @transform.register(LanguageStringsDto, LanguageStringsData)
    def language_strings_dto_to_data(
        self, value: LanguageStringsDto, context: PipelineContext = None
    ) -> LanguageStringsData:
        return LanguageStringsData(**value)

    # Profile Icons

    @transform.register(ProfileIconDetailsDto, ProfileIconData)
    def profile_icon_details_dto_to_data(
        self, value: ProfileIconDetailsDto, context: PipelineContext = None
    ) -> ProfileIconData:
        return ProfileIconData(**value)

    @transform.register(ProfileIconDataDto, ProfileIconListData)
    def profile_icon_data_dto_to_data(
        self, value: ProfileIconDataDto, context: PipelineContext = None
    ) -> ProfileIconListData:
        data = deepcopy(value)
        return ProfileIconListData(
            [self.profile_icon_details_dto_to_data(p) for p in data["data"].values()],
            region=value["region"],
            version=value["version"],
            locale=value["locale"],
        )

    ################
    # Data to Core #
    ################

    # Version

    # @transform.register(VersionListData, Versions)
    def version_list_data_to_core(self, value: VersionListData, context: PipelineContext = None) -> Versions:
        version = Versions.from_data(*value, region=value.region)
        return version

    # Realm

    # @transform.register(RealmData, Realms)
    def realm_data_to_core(self, value: RealmData, context: PipelineContext = None) -> Realms:
        realms = Realms.from_data(value)
        realms(region=value.region)
        return realms

    # Languages

    # @transform.register(LanguagesData, Locales)
    def languages_data_to_core(self, value: LanguagesData, context: PipelineContext = None) -> Locales:
        return Locales.from_data(*value, region=value.region)

    # Language Strings

    # @transform.register(LanguageStringsData, LanguageStrings)
    def language_strings_data_to_core(
        self, value: LanguageStringsData, context: PipelineContext = None
    ) -> LanguageStrings:
        return LanguageStrings.from_data(value)

    # Profile Icon

    # @transform.register(ProfileIconData, ProfileIcon)
    def profile_icon_data_to_core(self, value: ProfileIconData, context: PipelineContext = None) -> ProfileIcon:
        return ProfileIcon.from_data(value)

    # @transform.register(ProfileIconListData, ProfileIcons)
    def profile_icon_list_data_to_core(
        self, value: ProfileIconListData, context: PipelineContext = None
    ) -> ProfileIcons:
        return ProfileIcons.from_data(
            *[self.profile_icon_data_to_core(profile_icon) for profile_icon in value],
            region=value.region,
            version=value.version,
            locale=value.locale
        )
