from random import random

from lib.matches.base_match import BaseMatch

class WeakestProportionalChanceMatch(BaseMatch):

    def determine_winner(self):
        weakest1 = min(self.team1.values())
        weakest2 = min(self.team2.values())
        if random() < float(weakest1) / float(weakest1 + weakest2):
            return 1
        else:
            return 2
