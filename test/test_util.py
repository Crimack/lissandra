import os
import unittest

from lissandra import lissandra


def test_setup():
    lissandra.apply_settings(lissandra.get_default_config())
    lissandra.set_riot_api_key(os.environ.get("RIOT_API_KEY"))
    lissandra.apply_settings({"global": {"default_region": "EUW"}})


class BaseTest(unittest.TestCase):
    def setUp(self):
        test_setup()
