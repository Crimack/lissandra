from collections import Counter
import os
import random
import unittest

import lissandra as liss
from lissandra import (
    Summoner,
    LanguageStrings,
    Locales,
    ShardStatus,
    VerificationString,
)

from .test_util import BaseTest


class TestLeague(BaseTest):
    def test_versions(self):
        versions = liss.get_versions(region="EUW")
        self.assertIsNotNone(versions[0])
        self.assertEqual(versions.region.name, "europe_west")
        self.assertEqual(versions.region.value, "EUW")

    def test_realms(self):
        realms = liss.get_realms(region="EUW")
        self.assertIsNotNone(realms.latest_versions)

    def test_languagestrings(self):
        language_strings = liss.get_language_strings(region="EUW")
        self.assertTrue(len(language_strings.strings) > 0)

    def test_locales(self):
        locales = liss.get_locales(region="EUW")
        for locale in locales:
            locale
        assert len(locales) > 10

    def test_profileicons(self):
        profile_icons = liss.get_profile_icons(region="EUW")
        for pi in profile_icons:
            pi.name, pi.id
        profile_icons[10].name

    def test_readme(self):
        summoner = liss.get_summoner(name="Crimack", region="EUW")
        "{name} is a level {level} summoner on the {region} server.".format(
            name=summoner.name, level=summoner.level, region=summoner.region
        )

    def test_shards(self):
        status = liss.get_status(region="EUW")
        status = ShardStatus(region="EUW")
        self.assertIsNotNone(status.name)

    def test_summoner(self):
        name = "Crimack"
        region = "EUW"
        summoner = Summoner(name=name, region=region)
        "Name:", summoner.name
        "ID:", summoner.id
        "Account ID:", summoner.account_id
        "Level:", summoner.level
        "Revision date:", summoner.revision_date
        "Profile icon ID:", summoner.profile_icon.id
        "Profile icon name:", summoner.profile_icon.name
        "Profile icon URL:", summoner.profile_icon.url
        "Profile icon image:", summoner.profile_icon.image
