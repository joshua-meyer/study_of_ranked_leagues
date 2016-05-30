import math
import string

from lib.base import *

class BasePlayerGenerator():
    def __init__(self, number_of_players, baseline = 0):
        self.number_of_players = number_of_players
        self.baseline = baseline
        self.player_base = self.generate_player_base(number_of_players, baseline)

    def generate_player_base(self, number_of_players, baseline = 0):
        player_base = {}
        length_of_player_names = self.calculate_needed_length_of_player_names(number_of_players)
        for i in range(baseline, number_of_players + baseline):
            player_name = self.map_integer_to_string(i, length_of_player_names)
            player_base[player_name] = i
        return player_base

    def calculate_needed_length_of_player_names(self, number_of_players):
        if number_of_players < 0: raise ValueError("you can't have a negative number of players")
        if number_of_players == 0: return 0
        if number_of_players == 1: return 1
        raw_number = math.log(number_of_players, 26)
        return int(math.ceil(raw_number))

    def map_integer_to_string(self, some_integer, string_length):
        modulus = 26
        result = ""
        while len(result) < string_length:
            this_digit = some_integer % modulus
            while this_digit > 25:
                this_digit -= 25
                some_integer -= 26
            if some_integer >= this_digit: some_integer -= this_digit
            this_letter = string.lowercase[this_digit]
            result += this_letter
            modulus *= 26
        return result
