import unittest

from lissandra import Patch, Region

from .test_util import BaseTest


class TestPatches(BaseTest):
    def test_known_patches(self):
        self.assertIsInstance(Patch.from_str("1.0.0.152", region="EUW"), Patch)
        self.assertIsInstance(Patch.from_str("5.19", region="EUW"), Patch)
        self.assertIsInstance(Patch.from_str("7.22", region="EUW"), Patch)

    def test_unknown_patch_raises(self):
        with self.assertRaises(ValueError):
            Patch.from_str("unknown patch")

    def test_patch_relational_operators(self):
        self.assertTrue(Patch.from_str("9.9", region="EUW") < Patch.from_str("9.10", region="EUW"))
        self.assertTrue(Patch.from_str("8.20", region="EUW") > Patch.from_str("8.11", region="EUW"))
        self.assertTrue(Patch.from_str("8.20", region="EUW") > Patch.from_str("8.3", region="EUW"))
