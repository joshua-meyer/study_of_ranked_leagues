import unittest
from hypothesis import given, assume, note
from hypothesis.strategies import integers

from lib.player_generators.base_player_generator import BasePlayerGenerator
from lib.tiered_leagues.base_tiered_league import BaseTieredLeague

class TestBaseTieredLeague(unittest.TestCase):

    def test_migrate_player1(self):
        bpg = BasePlayerGenerator(1)
        btl = BaseTieredLeague(bpg)
        test_league = { 1: { 2: {} } }
        btl.migrate_player(test_league, 1, 2, "test", 3)
        self.assertEqual(test_league, { 1: { 2: { "test": 3 } } })

    def test_migrate_player2(self):
        bpg = BasePlayerGenerator(1)
        btl = BaseTieredLeague(bpg)
        test_league = { 1: { 2: {} } }
        btl.migrate_player(test_league, 1, 1, "test", -2)
        self.assertEqual(test_league, { 1: { 2: { "test": 10 } } })

    def test_migrate_player3(self):
        bpg = BasePlayerGenerator(1)
        btl = BaseTieredLeague(bpg)
        test_league = { 1: { 1: {} } }
        btl.migrate_player(test_league, 1, 2, "test", 10)
        self.assertEqual(test_league, { 1: { 1: { "test": 0 } } })

    def test_migrate_player4(self):
        bpg = BasePlayerGenerator(1)
        btl = BaseTieredLeague(bpg)
        test_league = { 1: { 0: {} } }
        btl.migrate_player(test_league, 0, 2, "test", -1)
        self.assertEqual(test_league, { 1: { 0: { "test": 10 } } })

    def test_migrate_player5(self):
        bpg = BasePlayerGenerator(1)
        btl = BaseTieredLeague(bpg)
        test_league = { 0: { 2: {} } }
        btl.migrate_player(test_league, 1, 0, "test", 11)
        self.assertEqual(test_league, { 0: { 2: { "test": 0 } } })

    def test_migrate_player6(self):
        bpg = BasePlayerGenerator(1)
        btl = BaseTieredLeague(bpg)
        test_league = { 2: { 2: {} } }
        btl.migrate_player(test_league, 2, 2, "test", -3)
        self.assertEqual(test_league, { 2: { 2: { "test": 0 } } })

    def test_migrate_player7(self):
        bpg = BasePlayerGenerator(1)
        btl = BaseTieredLeague(bpg)
        test_league = { 0: { 0: {} } }
        btl.migrate_player(test_league, 0, 0, "test", 12)
        self.assertEqual(test_league, { 0: { 0: { "test": 12 } } })

    def test_apply_tier_adjustments(self):
        bpg = BasePlayerGenerator(1)
        btl = BaseTieredLeague(bpg)
        btl.tiered_league = {
            0: {
                0: { "a": 13 },
                1: { "b": 14 },
                2: { "c": -4 },
            },
            1: {
                0: { "d": 15 },
                1: { "e": -5 },
                2: { "f": 0 },
            },
            2: {
                0: { "g": 1 },
                1: { "h": 9 },
                2: { "i": -6 },
            },
        }
        btl.apply_tier_adjustments()
        expected_league = {
            0: {
                0: { "a": 13, "b": 0 },
                1: {},
                2: { "d": 0 },
            },
            1: {
                0: { "c": 10 },
                1: {},
                2: { "e": 10, "f": 0 },
            },
            2: {
                0: { "g": 1 },
                1: { "h": 9 },
                2: { "i": 0 },
            },
        }
        self.assertEqual(btl.tiered_league, expected_league)

if __name__ == '__main__':
    unittest.main()
