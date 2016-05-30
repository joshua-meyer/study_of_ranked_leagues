import unittest
from hypothesis import given, assume, note
from hypothesis.strategies import integers

from lib.player_generators.base_player_generator import BasePlayerGenerator

class TestBasePlayerGenerator(unittest.TestCase):

    def test_calculate_needed_length_of_player_names(self):
        bpg = BasePlayerGenerator(0)
        self.assertEqual(bpg.calculate_needed_length_of_player_names(0), 0)
        self.assertEqual(bpg.calculate_needed_length_of_player_names(1), 1)
        self.assertEqual(bpg.calculate_needed_length_of_player_names(26), 1)
        self.assertEqual(bpg.calculate_needed_length_of_player_names(27), 2)

    def test_map_integer_to_string(self):
        bpg = BasePlayerGenerator(0)
        self.assertEqual(bpg.map_integer_to_string(0, 0), "")
        self.assertEqual(bpg.map_integer_to_string(0, 1), "a")
        self.assertEqual(bpg.map_integer_to_string(1, 1), "b")
        self.assertEqual(bpg.map_integer_to_string(10, 1), "k")
        self.assertEqual(bpg.map_integer_to_string(25, 1), "z")
        self.assertEqual(bpg.map_integer_to_string(0, 2), "aa")
        self.assertEqual(bpg.map_integer_to_string(1, 2), "ba")
        self.assertEqual(bpg.map_integer_to_string(10, 2), "ka")
        self.assertEqual(bpg.map_integer_to_string(25, 2), "za")
        self.assertEqual(bpg.map_integer_to_string(26, 2), "ab")
        self.assertEqual(bpg.map_integer_to_string(36, 2), "kb")
        self.assertEqual(bpg.map_integer_to_string(51, 2), "zb")
        self.assertEqual(bpg.map_integer_to_string(52, 2), "ac")
        self.assertEqual(bpg.map_integer_to_string(0, 3), "aaa")
        self.assertEqual(bpg.map_integer_to_string(1, 3), "baa")
        self.assertEqual(bpg.map_integer_to_string(10, 3), "kaa")
        self.assertEqual(bpg.map_integer_to_string(25, 3), "zaa")
        self.assertEqual(bpg.map_integer_to_string(26, 3), "aba")
        self.assertEqual(bpg.map_integer_to_string(36, 3), "kba")
        self.assertEqual(bpg.map_integer_to_string(51, 3), "zba")
        self.assertEqual(bpg.map_integer_to_string(52, 3), "aca")
        self.assertEqual(bpg.map_integer_to_string(17575, 3), "zzz")

    # @given(integers(min_value = 0, max_value = 141167095653375),
    #     integers(min_value = 0, max_value = 141167095653375),
    #     integers(min_value = 0, max_value = 10))
    # def test_map_integer_to_string_is_unique(self, x, y, z):
    #     assume(x != y)
    #     assume(x < 26**z)
    #     assume(y < 26**z)
    #     note("x==" + str(x) + " y==" + str(y) + " z==" + str(z))
    #     bpg = BasePlayerBaseGenerator(0)
    #     a = bpg.map_integer_to_string(x, z)
    #     b = bpg.map_integer_to_string(y, z)
    #     self.assertNotEqual(a, b)

if __name__ == '__main__':
    unittest.main()
