import io
import os
import unittest
from unittest.mock import patch

from lissandra import lissandra, League, Tier, Region, Platform

from .constants import LEAGUE_UUID, SUMMONER_NAME
from .test_util import BaseTest


class TestLeague(BaseTest):
    def test_access_league_properties(self):
        league_1 = League(id=LEAGUE_UUID)
        league_2 = lissandra.get_league(league_id=LEAGUE_UUID)

        for lg in [league_1, league_2]:
            self.assert_league_properties(lg)
            self.assertEqual(lg.id, LEAGUE_UUID)

        self.assertEqual(league_1, league_2)

    def test_master_league(self):
        league = lissandra.get_master_league()
        self.assert_league_properties(league)

        self.assertEqual(league.tier, Tier.master)

    def test_grandmaster_league(self):
        league = lissandra.get_grandmaster_league()
        self.assert_league_properties(league)

        self.assertEqual(league.tier, Tier.grandmaster)

    def test_challenger_league(self):
        league = lissandra.get_challenger_league()
        self.assert_league_properties(league)

        self.assertEqual(league.tier, Tier.challenger)

    def test_access_league_entry_properties(self):
        entry = lissandra.League(id=LEAGUE_UUID).entries[0]
        self.assertIsNotNone(entry.region)
        self.assertIsNotNone(entry.platform)
        self.assertIsNotNone(entry.tier)
        self.assertIsNotNone(entry.division)
        self.assertIsNotNone(entry.hot_streak)
        self.assertIsNotNone(entry.wins)
        self.assertIsNotNone(entry.veteran)
        self.assertIsNotNone(entry.losses)
        self.assertIsNotNone(entry.summoner)
        self.assertIsNotNone(entry.fresh_blood)
        self.assertEqual(entry.league, lissandra.League(id=LEAGUE_UUID))
        self.assertIsNotNone(entry.league_points)
        self.assertIsNotNone(entry.inactive)

    # @patch("sys.stdout", new_callable=io.StringIO)
    # def test_get_id_no_call_to_league(self, patched_log):
    #     s = lissandra.Summoner(name=SUMMONER_NAME)
    #     s.league_entries[0].league.id
    #     full_http_call_log = patched_log.getvalue()
    #     log_lines = full_http_call_log.splitlines()

    #     # check that there were 2 http calls: one to get summoner and one to get league entries
    #     self.assertEqual(len(log_lines), 2)
    #     get_summoner_call = log_lines[0]
    #     get_league_entries_call = log_lines[1]

    #     self.assertTrue("summoner/v4/summoners/by-name" in get_summoner_call)
    #     self.assertTrue("league/v4/entries/by-summoner" in get_league_entries_call)

    #     # check that league endpoint wasn't called to get id
    #     self.assertFalse("league/v4/leagues" in full_http_call_log)

    def assert_league_properties(self, lg: League):
        self.assertEqual(lg.region, Region.europe_west)
        self.assertEqual(lg.platform, Platform.europe_west)
        self.assertIsNotNone(lg.id)
        self.assertIsNotNone(lg.tier)
        self.assertIsNotNone(lg.name)
        self.assertIsNotNone(lg.entries)


if __name__ == "__main__":
    unittest.main()
