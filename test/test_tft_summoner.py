import os
import unittest

import lissandra

from .constants import SUMMONER_NAME, UNKNOWN_SUMMONER_NAME
from .test_util import BaseTest


class TestTFTSummoner(BaseTest):
    def test_access_properties(self):
        s = lissandra.TFTSummoner(name=SUMMONER_NAME)
        self.assertIsNotNone(s.region)
        self.assertIsNotNone(s.platform)
        self.assertIsNotNone(s.account_id)
        self.assertIsNotNone(s.puuid)
        self.assertIsNotNone(s.id)
        self.assertIsNotNone(s.name)
        self.assertIsNotNone(s.sanitized_name)
        self.assertIsNotNone(s.level)
        self.assertIsNotNone(s.profile_icon)
        self.assertIsNotNone(s.revision_date)

    def test_equality(self):
        from_name = lissandra.get_tft_summoner(name=SUMMONER_NAME, region="EUW")
        from_id = lissandra.get_tft_summoner(id=from_name.id, region="EUW")
        self.assertEqual(from_name.id, from_id.id)
        self.assertEqual(from_name.name, from_id.name)
        self.assertEqual(from_name, from_id)
        self.assertEqual(from_name.to_dict(), from_id.to_dict())


if __name__ == "__main__":
    unittest.main()
