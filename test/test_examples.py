from collections import Counter
import random

import lissandra as liss
from lissandra import (
    TFTSummoner,
    LanguageStrings,
    Locales,
    ShardStatus,
    VerificationString,
)

import os, pytest


def test_versions():
    versions = liss.get_versions(region="NA")
    versions[0]
    versions.region
    versions = liss.get_versions(region="NA")
    versions[0]


def test_realms():
    realms = liss.get_realms(region="NA")
    realms.latest_versions


def test_languagestrings():
    language_strings = liss.get_language_strings(region="NA")
    assert len(language_strings.strings) > 0


def test_locales():
    locales = liss.get_locales(region="NA")
    for locale in locales:
        locale
    assert len(locales) > 10


def test_profileicons():
    profile_icons = liss.get_profile_icons(region="NA")
    for pi in profile_icons:
        pi.name, pi.id
    profile_icons[10].name


def test_readme():
    summoner = liss.get_tft_summoner(name="Kalturi", region="NA")
    "{name} is a level {level} summoner on the {region} server.".format(
        name=summoner.name, level=summoner.level, region=summoner.region
    )


def test_shards():
    status = liss.get_status(region="NA")
    status = ShardStatus(region="NA")
    status.name


def test_tft_summoner():
    name = "Kalturi"
    region = "NA"
    summoner = TFTSummoner(name=name, region=region)
    "Name:", summoner.name
    "ID:", summoner.id
    "Account ID:", summoner.account_id
    "Level:", summoner.level
    "Revision date:", summoner.revision_date
    "Profile icon ID:", summoner.profile_icon.id
    "Profile icon name:", summoner.profile_icon.name
    "Profile icon URL:", summoner.profile_icon.url
    "Profile icon image:", summoner.profile_icon.image

